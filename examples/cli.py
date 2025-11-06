"""
Interactive CLI for FinRAG system.
"""
import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Load environment variables from .env file
from finrag.utils import load_env_file
load_env_file()

from finrag import FinRAGConfig, FinRAG


class FinRAGCLI:
    """Command-line interface for FinRAG."""
    
    def __init__(self):
        self.finrag = None
        self.config = None
        
    def check_api_key(self) -> bool:
        """Check if OpenAI API key is set."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("\n❌ ERROR: OPENAI_API_KEY not found")
            print("\nPlease either:")
            print("  1. Add to .env file (recommended):")
            print("     OPENAI_API_KEY=sk-your-key")
            print("  2. Set environment variable:")
            print("     Windows: $env:OPENAI_API_KEY='your-key'")
            print("     Linux/Mac: export OPENAI_API_KEY='your-key'")
            return False
        return True
    
    def initialize_system(self):
        """Initialize FinRAG system."""
        print("\n🚀 Initializing FinRAG system...")
        
        # Config automatically loads from .env file
        self.config = FinRAGConfig()
        
        self.finrag = FinRAG(self.config)
        print("✅ System initialized")
    
    def load_documents(self):
        """Load documents interactively."""
        print("\n📄 Load Documents")
        print("-" * 60)
        print("Enter document paths (one per line, empty line to finish):")
        
        documents = []
        while True:
            path = input("  Path: ").strip()
            if not path:
                break
            
            path_obj = Path(path)
            if not path_obj.exists():
                print(f"  ❌ File not found: {path}")
                continue
            
            try:
                if path_obj.suffix.lower() == '.pdf':
                    text = self.finrag.load_pdf(str(path_obj))
                    print(f"  ✅ Loaded PDF: {len(text)} characters")
                else:
                    text = self.finrag.load_text(str(path_obj))
                    print(f"  ✅ Loaded text: {len(text)} characters")
                
                documents.append(text)
            except Exception as e:
                print(f"  ❌ Error loading {path}: {e}")
        
        if documents:
            print(f"\n🔨 Building tree from {len(documents)} document(s)...")
            self.finrag.add_documents(documents)
            
            stats = self.finrag.get_statistics()
            print("\n📊 Tree Statistics:")
            for key, value in stats.items():
                print(f"  {key}: {value}")
        else:
            print("  ⚠️  No documents loaded")
    
    def query_loop(self):
        """Interactive query loop."""
        if self.finrag.retriever is None:
            print("\n⚠️  No documents loaded. Please load documents first.")
            return
        
        print("\n💬 Query Mode")
        print("-" * 60)
        print("Enter your questions (type 'quit' to exit, 'stats' for statistics)")
        print()
        
        while True:
            question = input("❓ Question: ").strip()
            
            if not question:
                continue
            
            if question.lower() in ['quit', 'exit', 'q']:
                break
            
            if question.lower() == 'stats':
                stats = self.finrag.get_statistics()
                print("\n📊 Statistics:")
                for key, value in stats.items():
                    print(f"  {key}: {value}")
                print()
                continue
            
            try:
                print("\n🔍 Retrieving relevant documents...")
                result = self.finrag.query(question)
                
                print("\n💡 Answer:")
                print("-" * 60)
                print(result['answer'])
                print("-" * 60)
                
                print(f"\n📚 Retrieved {len(result['retrieved_nodes'])} nodes")
                print(f"   Method: {result['retrieval_method']}")
                
                show_sources = input("\nShow sources? (y/n): ").strip().lower()
                if show_sources == 'y':
                    print("\n📖 Top Sources:")
                    for i, node in enumerate(result['retrieved_nodes'][:5], 1):
                        print(f"\n  {i}. Level {node['level']} (Score: {node['score']:.3f})")
                        print(f"     {node['text_preview']}")
                
                print()
                
            except Exception as e:
                print(f"\n❌ Error: {e}\n")
    
    def save_system(self):
        """Save FinRAG system."""
        if self.finrag.retriever is None:
            print("\n⚠️  No documents loaded. Nothing to save.")
            return
        
        print("\n💾 Save System")
        print("-" * 60)
        default_path = "./finrag_saved"
        path = input(f"Save path (default: {default_path}): ").strip()
        
        if not path:
            path = default_path
        
        try:
            self.finrag.save(path)
            print(f"✅ Saved to: {path}")
        except Exception as e:
            print(f"❌ Error saving: {e}")
    
    def load_system(self):
        """Load saved FinRAG system."""
        print("\n📂 Load Saved System")
        print("-" * 60)
        path = input("Load path: ").strip()
        
        if not path or not Path(path).exists():
            print("❌ Path not found")
            return
        
        try:
            if self.finrag is None:
                self.initialize_system()
            
            self.finrag.load(path)
            print(f"✅ Loaded from: {path}")
            
            stats = self.finrag.get_statistics()
            print("\n📊 Tree Statistics:")
            for key, value in stats.items():
                print(f"  {key}: {value}")
        except Exception as e:
            print(f"❌ Error loading: {e}")
    
    def show_menu(self):
        """Show main menu."""
        print("\n" + "="*60)
        print("🌳 FinRAG - Financial RAG System")
        print("="*60)
        print("\n1. Load documents")
        print("2. Query system")
        print("3. Save system")
        print("4. Load saved system")
        print("5. Show statistics")
        print("6. Exit")
        print()
    
    def run(self):
        """Run the CLI."""
        if not self.check_api_key():
            return
        
        self.initialize_system()
        
        while True:
            self.show_menu()
            choice = input("Select option (1-6): ").strip()
            
            if choice == '1':
                self.load_documents()
            elif choice == '2':
                self.query_loop()
            elif choice == '3':
                self.save_system()
            elif choice == '4':
                self.load_system()
            elif choice == '5':
                if self.finrag.retriever:
                    stats = self.finrag.get_statistics()
                    print("\n📊 Statistics:")
                    for key, value in stats.items():
                        print(f"  {key}: {value}")
                else:
                    print("\n⚠️  No documents loaded")
            elif choice == '6':
                print("\n👋 Goodbye!")
                break
            else:
                print("\n❌ Invalid option")


def main():
    """Main entry point."""
    cli = FinRAGCLI()
    try:
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
