"""
Metadata Clustering Example for FinRAG

This example demonstrates how FinRAG's metadata clustering works with financial documents.
It shows how documents are automatically grouped by sector, company, and year before
performing embedding-based clustering within each group.

This implements the two-stage clustering approach from the FinRAG paper:
1. Stage 1: Group by metadata (sector, company, year)
2. Stage 2: Cluster by embeddings within metadata groups
"""

from finrag import FinRAG
from finrag.config import FinRAGConfig
import json


def get_tree_depth(tree):
    """Helper function to get the depth/number of layers in a RAPTOR tree."""
    if not tree.all_nodes:
        return 0
    max_level = max(node.level for node in tree.all_nodes.values())
    return max_level + 1


# Sample financial documents with clear metadata
SAMPLE_DOCUMENTS = [
    # JPMorgan Finance Documents - 2023
    """
    JPMorgan Chase & Co. 2023 Annual Report - Finance Sector
    
    Financial Performance Overview:
    Total revenue for 2023 reached $158.1 billion, representing a 22% increase 
    year-over-year. Net income was $48.3 billion, with return on equity of 16%.
    
    Investment Banking:
    Investment banking fees totaled $7.4 billion, driven by strong M&A advisory 
    and debt underwriting activities. The commercial banking segment saw deposits 
    grow by 8% to $1.3 trillion.
    
    Risk Management:
    Credit loss provisions decreased to $8.9 billion as economic conditions 
    improved. The firm maintained strong capital ratios with CET1 at 14.3%.
    """,
    
    """
    JPMorgan Chase 2023 Q4 Earnings Report - Finance
    
    Fourth Quarter Highlights:
    Q4 2023 revenue: $39.9 billion, up 12% YoY
    Net income: $9.3 billion, EPS of $3.04
    
    Consumer & Community Banking:
    Consumer banking deposits grew to $954 billion. Credit card sales volume 
    reached $238 billion in Q4, showing strong consumer spending patterns.
    
    Commercial Banking:
    Commercial banking revenue was $3.5 billion with loan growth of 5% YoY.
    Middle market lending expanded across all regions.
    """,
    
    # Apple Technology Documents - 2023
    """
    Apple Inc. 2023 Annual Report - Technology Sector
    
    Company Overview:
    Apple Inc. designs, manufactures, and markets smartphones, personal computers,
    tablets, wearables, and accessories worldwide.
    
    Financial Results 2023:
    Net sales: $383.3 billion, down 3% from 2022
    Net income: $97.0 billion
    Products revenue: $298.1 billion
    Services revenue: $85.2 billion
    
    iPhone Performance:
    iPhone remains the largest revenue driver at $200.6 billion. The iPhone 15 
    launch in September 2023 drove strong upgrade cycles.
    
    Services Growth:
    Services segment grew 9% YoY driven by App Store, Apple Music, iCloud, 
    and Apple TV+ subscriptions reaching 1 billion paid subscriptions.
    """,
    
    """
    Apple Inc. Technology Sector - 2023 Product Innovation Report
    
    Research & Development:
    R&D expenses reached $29.9 billion in 2023, representing 7.8% of revenue.
    Major investments in artificial intelligence, AR/VR, and custom silicon.
    
    Product Launches 2023:
    - iPhone 15 Pro with A17 Pro chip (3nm technology)
    - Apple Watch Series 9 with double tap gesture
    - MacBook Pro with M3, M3 Pro, and M3 Max chips
    - Vision Pro announcement for 2024 launch
    
    Sustainability:
    100% carbon neutral for corporate operations. Committed to carbon neutral 
    products by 2030. Increased use of recycled materials in all products.
    """,
    
    # Goldman Sachs Finance - 2023
    """
    Goldman Sachs Group Inc. 2023 Annual Report - Finance Sector
    
    Business Overview:
    Goldman Sachs is a leading global investment banking, securities, and 
    investment management firm.
    
    2023 Financial Performance:
    Net revenues: $46.2 billion, up 6% from 2022
    Net earnings: $8.5 billion
    Return on equity: 7.5%
    
    Investment Banking:
    Advisory revenues: $2.9 billion
    Equity underwriting: $1.8 billion
    Debt underwriting: $2.1 billion
    
    Asset & Wealth Management:
    Assets under supervision: $2.8 trillion
    Management fees and other revenues: $8.1 billion
    """,
    
    # Tesla Technology - 2023
    """
    Tesla Inc. 2023 Annual Report - Technology & Manufacturing Sector
    
    Company Profile:
    Tesla designs, develops, manufactures, and sells electric vehicles and 
    energy generation and storage systems.
    
    2023 Performance Metrics:
    Total revenue: $96.8 billion, up 19% YoY
    Automotive revenue: $82.4 billion
    Energy generation and storage: $6.0 billion
    Services and other: $8.3 billion
    
    Vehicle Production & Delivery:
    Total production: 1.85 million vehicles
    Total deliveries: 1.81 million vehicles
    Model Y became the best-selling vehicle globally in Q1 2023
    
    Technology Innovation:
    Full Self-Driving (FSD) Beta expanded to over 400,000 customers
    4680 battery cell production ramped at Giga Texas
    Cybertruck production started in Q4 2023
    """,
    
    # Microsoft Technology - 2022
    """
    Microsoft Corporation 2022 Annual Report - Technology Sector
    
    Business Segments:
    Microsoft develops, licenses, and supports software, services, devices, 
    and solutions worldwide.
    
    Fiscal Year 2022 Results:
    Revenue: $198.3 billion, up 18% YoY
    Net income: $72.7 billion
    Operating income: $83.4 billion
    
    Segment Performance:
    Productivity and Business Processes: $63.4 billion
    Intelligent Cloud: $75.3 billion (includes Azure)
    More Personal Computing: $59.6 billion
    
    Cloud Growth:
    Azure and cloud services revenue grew 40% YoY
    Microsoft 365 commercial seats surpassed 382 million
    """,
]


def demonstrate_basic_metadata_clustering():
    """Basic example showing metadata clustering in action."""
    print("=" * 80)
    print("BASIC METADATA CLUSTERING EXAMPLE")
    print("=" * 80)
    print()
    
    # Initialize FinRAG with metadata clustering enabled (default)
    print("1. Initializing FinRAG with metadata clustering enabled...")
    config = FinRAGConfig()
    config.use_metadata_clustering = True  # Enabled by default
    config.metadata_keys = ["sector", "company", "year"]  # Default keys
    
    finrag = FinRAG(config=config)
    print(f"   ✓ Metadata clustering: {config.use_metadata_clustering}")
    print(f"   ✓ Metadata keys: {config.metadata_keys}")
    print()
    
    # Add documents
    print("2. Adding financial documents with metadata...")
    print(f"   Adding {len(SAMPLE_DOCUMENTS)} documents...")
    finrag.add_documents(SAMPLE_DOCUMENTS)
    print()
    
    # Query examples
    print("3. Running queries to test metadata-aware retrieval...")
    print()
    
    queries = [
        "What were JPMorgan's financial results in 2023?",
        "How did Apple's iPhone perform in 2023?",
        "What was Tesla's vehicle production in 2023?",
        "Compare investment banking performance across firms in 2023",
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"   Query {i}: {query}")
        result = finrag.query(query, retrieval_method="tree_traversal")
        print(f"   Answer: {result['answer'][:200]}...")
        print(f"   Retrieved {len(result['retrieved_nodes'])} nodes")
        print()
    
    print("✓ Basic example completed!")
    print()


def demonstrate_metadata_extraction():
    """Show how metadata is extracted from documents."""
    print("=" * 80)
    print("METADATA EXTRACTION DEMONSTRATION")
    print("=" * 80)
    print()
    
    from finrag.models import FinancialChunker
    
    chunker = FinancialChunker(chunk_size=1000, chunk_overlap=200)
    
    print("Testing metadata extraction on sample documents...")
    print()
    
    for i, doc in enumerate(SAMPLE_DOCUMENTS[:3], 1):  # Test first 3 docs
        print(f"Document {i}:")
        print(f"Preview: {doc[:100]}...")
        print()
        
        # Extract metadata
        metadata = chunker.extract_metadata(doc)
        
        print(f"Extracted Metadata:")
        print(f"  - Sector: {metadata.get('sector', 'Not found')}")
        print(f"  - Company: {metadata.get('company', 'Not found')}")
        print(f"  - Year: {metadata.get('year', 'Not found')}")
        print()
        
        # Show chunks with metadata
        chunks = chunker.chunk_text_with_metadata(doc)
        print(f"Created {len(chunks)} chunks, each with metadata:")
        if chunks:
            print(f"  Sample chunk metadata: {chunks[0].get('metadata', {})}")
        print()
        print("-" * 80)
        print()
    
    print("✓ Metadata extraction demonstration completed!")
    print()


def demonstrate_clustering_comparison():
    """Compare clustering with and without metadata."""
    print("=" * 80)
    print("CLUSTERING COMPARISON: WITH vs WITHOUT METADATA")
    print("=" * 80)
    print()
    
    # Without metadata clustering
    print("1. Building tree WITHOUT metadata clustering...")
    config_no_metadata = FinRAGConfig()
    config_no_metadata.use_metadata_clustering = False
    
    finrag_no_metadata = FinRAG(config=config_no_metadata)
    finrag_no_metadata.add_documents(SAMPLE_DOCUMENTS)
    
    num_layers_no_metadata = get_tree_depth(finrag_no_metadata.tree)
    print(f"   Tree built with standard clustering")
    print(f"   Number of layers: {num_layers_no_metadata}")
    print()
    
    # With metadata clustering
    print("2. Building tree WITH metadata clustering...")
    config_with_metadata = FinRAGConfig()
    config_with_metadata.use_metadata_clustering = True
    
    finrag_with_metadata = FinRAG(config=config_with_metadata)
    finrag_with_metadata.add_documents(SAMPLE_DOCUMENTS)
    
    num_layers_with_metadata = get_tree_depth(finrag_with_metadata.tree)
    print(f"   Tree built with metadata-aware clustering")
    print(f"   Number of layers: {num_layers_with_metadata}")
    print()
    
    # Compare retrieval
    print("3. Comparing retrieval quality...")
    test_query = "What were JPMorgan's 2023 financial results?"
    
    print(f"   Query: {test_query}")
    print()
    
    result_no_metadata = finrag_no_metadata.query(
        test_query, 
        retrieval_method="tree_traversal"
    )
    
    result_with_metadata = finrag_with_metadata.query(
        test_query,
        retrieval_method="tree_traversal"
    )
    
    print("   WITHOUT metadata clustering:")
    print(f"   - Retrieved {len(result_no_metadata['retrieved_nodes'])} nodes")
    print(f"   - Answer: {result_no_metadata['answer'][:150]}...")
    print()
    
    print("   WITH metadata clustering:")
    print(f"   - Retrieved {len(result_with_metadata['retrieved_nodes'])} nodes")
    print(f"   - Answer: {result_with_metadata['answer'][:150]}...")
    print()
    
    print("✓ Comparison completed!")
    print()


def demonstrate_custom_metadata_keys():
    """Show how to use custom metadata keys."""
    print("=" * 80)
    print("CUSTOM METADATA KEYS EXAMPLE")
    print("=" * 80)
    print()
    
    print("You can customize which metadata fields to use for clustering:")
    print()
    
    # Example 1: Only sector and year
    print("1. Clustering by SECTOR and YEAR only (ignoring company)...")
    config1 = FinRAGConfig()
    config1.use_metadata_clustering = True
    config1.metadata_keys = ["sector", "year"]
    
    print(f"   Metadata keys: {config1.metadata_keys}")
    print(f"   This groups all companies in same sector/year together")
    print()
    
    # Example 2: Only company
    print("2. Clustering by COMPANY only (ignoring sector and year)...")
    config2 = FinRAGConfig()
    config2.use_metadata_clustering = True
    config2.metadata_keys = ["company"]
    
    print(f"   Metadata keys: {config2.metadata_keys}")
    print(f"   This groups all documents from same company together")
    print()
    
    # Example 3: All three (default)
    print("3. Clustering by SECTOR, COMPANY, and YEAR (default)...")
    config3 = FinRAGConfig()
    config3.use_metadata_clustering = True
    config3.metadata_keys = ["sector", "company", "year"]
    
    print(f"   Metadata keys: {config3.metadata_keys}")
    print(f"   This creates most specific groupings")
    print()
    
    print("✓ Custom metadata keys example completed!")
    print()


def demonstrate_tree_structure():
    """Visualize how metadata affects tree structure."""
    print("=" * 80)
    print("TREE STRUCTURE VISUALIZATION")
    print("=" * 80)
    print()
    
    print("Building tree with metadata clustering...")
    config = FinRAGConfig()
    config.use_metadata_clustering = True
    
    finrag = FinRAG(config=config)
    finrag.add_documents(SAMPLE_DOCUMENTS)
    
    tree = finrag.tree
    num_layers = get_tree_depth(tree)
    
    print(f"Tree Structure:")
    print(f"  Total layers: {num_layers}")
    print()
    
    for layer_idx in range(num_layers):
        # Get all nodes at this layer
        layer_nodes = [node for node in tree.all_nodes.values() if node.level == layer_idx]
        layer = layer_nodes
        print(f"  Layer {layer_idx}:")
        print(f"    - Number of nodes: {len(layer)}")
        
        # Show metadata distribution in this layer
        if layer:
            metadata_groups = {}
            for node in layer:
                if hasattr(node, 'metadata') and node.metadata:
                    # Ensure all values are strings, not None
                    sector = node.metadata.get('sector') or 'unknown'
                    company = node.metadata.get('company') or 'unknown'
                    year = node.metadata.get('year') or 'unknown'
                    key = (sector, company, year)
                    metadata_groups[key] = metadata_groups.get(key, 0) + 1
            
            if metadata_groups:
                print(f"    - Metadata groups:")
                # Sort safely by converting tuples to strings for sorting
                for (sector, company, year), count in sorted(metadata_groups.items(), key=lambda x: (str(x[0][0]), str(x[0][1]), str(x[0][2]))):
                    print(f"      • {sector}/{company}/{year}: {count} nodes")
        print()
    
    print("✓ Tree structure visualization completed!")
    print()


def main():
    """Run all examples."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "FinRAG METADATA CLUSTERING EXAMPLES" + " " * 23 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    try:
        # Run examples
        # demonstrate_metadata_extraction()
        # input("Press Enter to continue to basic example...")
        
        # demonstrate_basic_metadata_clustering()
        # # input("Press Enter to continue to comparison...")
        
        # # demonstrate_clustering_comparison()
        # input("Press Enter to continue to custom metadata keys...")
        
        # demonstrate_custom_metadata_keys()
        input("Press Enter to continue to tree structure...")
        
        demonstrate_tree_structure()
        
        print()
        print("=" * 80)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print()
        print("Key Takeaways:")
        print("1. Metadata clustering groups documents by sector, company, and year")
        print("2. This improves retrieval quality for financial documents")
        print("3. You can customize which metadata fields to use")
        print("4. Metadata is automatically extracted using pattern matching")
        print("5. Two-stage clustering: metadata grouping → embedding clustering")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have:")
        print("1. Set OPENAI_API_KEY in .env file")
        print("2. Installed the package: pip install -e .")
        print("3. All dependencies installed: pip install -r requirements.txt")
        raise


if __name__ == "__main__":
    main()
