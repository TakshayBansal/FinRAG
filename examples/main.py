"""
Main entry point for FinRAG system with example usage.
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


def main():
    """Main function demonstrating FinRAG usage."""
    
    # API keys are loaded from .env file automatically
    # Or you can override them here if needed
    
    # Initialize config (reads from environment variables and .env file)
    config = FinRAGConfig()
    
    # Or override specific values:
    # config = FinRAGConfig(
    #     openai_api_key="your-key",  # Override .env value
    #     chunk_size=1024,            # Override default
    # )
    
    # Initialize FinRAG
    print("Initializing FinRAG system...")
    finrag = FinRAG(config)
    
    # Load pre-built tree (built from all PDFs in data folder)
    tree_path = Path(__file__).parent.parent / "finrag_tree"
    
    if tree_path.exists():
        print(f"\n✓ Loading pre-built tree from: {tree_path}")
        finrag.load(str(tree_path))
        
        # Print statistics
        stats = finrag.get_statistics()
        print("\n✓ Tree loaded successfully!")
        print("\nTree Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        # Example queries
        questions = [
            "What is the name of the company and its sector name?"
        ]
        
        print("\n" + "="*80)
        print("QUERYING THE SYSTEM")
        print("="*80)
        
        for question in questions:
            print(f"\nQuestion: {question}")
            print("-" * 80)
            
            result = finrag.query(question)
            
            print(f"Answer:\n{result['answer']}")
            print(f"\nRetrieved {len(result['retrieved_nodes'])} relevant nodes")
            print(f"Retrieval method: {result['retrieval_method']}")
            
            # Show top 3 retrieved nodes
            print("\nTop retrieved nodes:")
            for i, node_info in enumerate(result['retrieved_nodes'][:3], 1):
                print(f"  {i}. Level {node_info['level']} "
                      f"(score: {node_info['score']:.3f})")
                print(f"     {node_info['text_preview']}")
            
            print()
        
    else:
        print(f"\n❌ Tree not found at: {tree_path}")
        print("\nPlease build the tree first by running:")
        print("  python scripts/build_tree.py")
        print("\nThis will process all PDFs in the data folder and create a reusable tree.")
        # print("\nExample usage without PDF:")
        # print("="*80)
        
        # # Example with text documents
        # sample_docs = [
        #     """
        #     Company XYZ Financial Report Q4 2024
            
        #     Revenue: $150M (up 25% YoY)
        #     Net Income: $45M (up 30% YoY)
        #     Operating Margin: 30%
            
        #     Key Highlights:
        #     - Strong growth in cloud services segment
        #     - Successful product launch in Asian markets
        #     - Improved operational efficiency
        #     """,
        #     """
        #     Risk Factors:
            
        #     1. Market Competition: Intense competition from established players
        #     2. Regulatory Changes: Potential new regulations in key markets
        #     3. Currency Fluctuations: Exposure to foreign exchange risk
        #     4. Technology Disruption: Rapid changes in technology landscape
        #     """,
        #     """
        #     Future Outlook:
            
        #     The company expects continued growth in 2025 with projected revenue
        #     of $180-200M. Key focus areas include:
        #     - Expansion into new geographic markets
        #     - Investment in R&D for next-generation products
        #     - Strategic acquisitions to enhance market position
        #     """
        # ]
        
        # print("Processing sample financial documents...")
        # finrag.add_documents(sample_docs)
        
        # stats = finrag.get_statistics()
        # print("\nTree Statistics:")
        # for key, value in stats.items():
        #     print(f"  {key}: {value}")
        
        # # Query the system
        # question = "What is the revenue and growth rate?"
        # print(f"\nQuestion: {question}")
        # result = finrag.query(question)
        # print(f"Answer: {result['answer']}")


if __name__ == "__main__":
    main()
