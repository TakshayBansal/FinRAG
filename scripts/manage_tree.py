"""
FinRAG Tree Management CLI

Simple command-line tool to manage FinRAG trees.
"""
import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from finrag.utils import load_env_file
load_env_file()

from finrag import FinRAG, FinRAGConfig


def build_tree(data_dir: str = None, output_dir: str = None, use_filtering: bool = True):
    """Build tree from PDFs in data directory."""
    if data_dir is None:
        data_dir = Path(__file__).parent.parent / "data"
    else:
        data_dir = Path(data_dir)
    
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "finrag_tree"
    else:
        output_dir = Path(output_dir)
    
    print("="*80)
    print("BUILDING FINRAG TREE")
    print("="*80)
    print(f"\nData directory: {data_dir}")
    print(f"Output directory: {output_dir}")
    print(f"Filtered parsing: {use_filtering}")
    
    # Get PDFs
    pdf_files = list(data_dir.glob("*.pdf"))
    if not pdf_files:
        print(f"\n❌ No PDF files found in {data_dir}")
        return False
    
    print(f"\n✓ Found {len(pdf_files)} PDF files")
    
    # Initialize FinRAG
    config = FinRAGConfig()
    config.use_filtered_parsing = use_filtering
    config.use_metadata_clustering = True
    
    finrag = FinRAG(config)
    
    # Process PDFs
    all_documents = []
    for i, pdf_path in enumerate(pdf_files, 1):
        print(f"\n[{i}/{len(pdf_files)}] Processing: {pdf_path.name}")
        try:
            text = finrag.load_pdf(str(pdf_path))
            all_documents.append(text)
            print(f"  ✓ Loaded {len(text):,} characters")
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    if not all_documents:
        print("\n❌ No documents were successfully processed")
        return False
    
    # Build tree
    print(f"\n✓ Successfully processed {len(all_documents)}/{len(pdf_files)} PDFs")
    print("\nBuilding tree...")
    
    try:
        finrag.add_documents(all_documents)
        print("✓ Tree built successfully")
    except Exception as e:
        print(f"❌ Error building tree: {e}")
        return False
    
    # Save tree
    print(f"\nSaving to: {output_dir}")
    try:
        finrag.save(str(output_dir))
        print(f"✓ Tree saved successfully")
    except Exception as e:
        print(f"❌ Error saving tree: {e}")
        return False
    
    # Stats
    stats = finrag.get_statistics()
    print("\nTree Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n" + "="*80)
    print("BUILD COMPLETE!")
    print("="*80)
    return True


def show_stats(tree_dir: str = None):
    """Show statistics for a saved tree."""
    if tree_dir is None:
        tree_dir = Path(__file__).parent.parent / "finrag_tree"
    else:
        tree_dir = Path(tree_dir)
    
    if not tree_dir.exists():
        print(f"❌ Tree not found at: {tree_dir}")
        return False
    
    print("="*80)
    print("TREE STATISTICS")
    print("="*80)
    print(f"\nTree location: {tree_dir}")
    
    # Load tree
    config = FinRAGConfig()
    finrag = FinRAG(config)
    
    try:
        print("\nLoading tree...")
        finrag.load(str(tree_dir))
        print("✓ Tree loaded successfully")
    except Exception as e:
        print(f"❌ Error loading tree: {e}")
        return False
    
    # Show stats
    stats = finrag.get_statistics()
    print("\nStatistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    return True


def query_tree(question: str, tree_dir: str = None, method: str = "tree_traversal"):
    """Query a saved tree."""
    if tree_dir is None:
        tree_dir = Path(__file__).parent.parent / "finrag_tree"
    else:
        tree_dir = Path(tree_dir)
    
    if not tree_dir.exists():
        print(f"❌ Tree not found at: {tree_dir}")
        return False
    
    print("="*80)
    print("QUERYING TREE")
    print("="*80)
    print(f"\nTree location: {tree_dir}")
    print(f"Question: {question}")
    print(f"Method: {method}")
    
    # Load tree
    config = FinRAGConfig()
    finrag = FinRAG(config)
    
    try:
        print("\nLoading tree...")
        finrag.load(str(tree_dir))
        print("✓ Tree loaded")
    except Exception as e:
        print(f"❌ Error loading tree: {e}")
        return False
    
    # Query
    try:
        print("\nGenerating answer...")
        result = finrag.query(question, retrieval_method=method)
        
        print("\n" + "="*80)
        print("ANSWER")
        print("="*80)
        print(f"\n{result['answer']}")
        
        print("\n" + "="*80)
        print("RETRIEVAL INFO")
        print("="*80)
        print(f"Retrieved {len(result['retrieved_nodes'])} nodes")
        print(f"Method: {result['retrieval_method']}")
        
        print("\nTop 3 nodes:")
        for i, node in enumerate(result['retrieved_nodes'][:3], 1):
            print(f"  {i}. Level {node['level']} (score: {node['score']:.3f})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error querying: {e}")
        return False


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="FinRAG Tree Management CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Build tree from data/ folder
  python manage_tree.py build
  
  # Build with custom directories
  python manage_tree.py build --data-dir ./my_pdfs --output-dir ./my_tree
  
  # Show tree statistics
  python manage_tree.py stats
  
  # Query the tree
  python manage_tree.py query "What is the revenue?"
  
  # Query with specific method
  python manage_tree.py query "What is the revenue?" --method collapsed_tree
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Build command
    build_parser = subparsers.add_parser('build', help='Build tree from PDFs')
    build_parser.add_argument('--data-dir', help='Directory containing PDF files')
    build_parser.add_argument('--output-dir', help='Directory to save tree')
    build_parser.add_argument('--no-filtering', action='store_true', 
                             help='Disable filtered parsing')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show tree statistics')
    stats_parser.add_argument('--tree-dir', help='Tree directory')
    
    # Query command
    query_parser = subparsers.add_parser('query', help='Query the tree')
    query_parser.add_argument('question', help='Question to ask')
    query_parser.add_argument('--tree-dir', help='Tree directory')
    query_parser.add_argument('--method', default='tree_traversal',
                             choices=['tree_traversal', 'collapsed_tree', 'top_k'],
                             help='Retrieval method')
    
    args = parser.parse_args()
    
    if args.command == 'build':
        success = build_tree(
            data_dir=args.data_dir,
            output_dir=args.output_dir,
            use_filtering=not args.no_filtering
        )
        sys.exit(0 if success else 1)
        
    elif args.command == 'stats':
        success = show_stats(tree_dir=args.tree_dir)
        sys.exit(0 if success else 1)
        
    elif args.command == 'query':
        success = query_tree(
            question=args.question,
            tree_dir=args.tree_dir,
            method=args.method
        )
        sys.exit(0 if success else 1)
        
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
