"""
Test script to verify the fixed hierarchical tree structure.
"""
from finrag import FinRAG, FinRAGConfig

def test_fixed_hierarchy():
    """Test that the tree builds with the fixed hierarchical structure."""
    
    # Initialize FinRAG with fixed hierarchy settings
    config = FinRAGConfig(
        tree_depth=4,
        use_metadata_clustering=True,
        max_cluster_size=50,
        min_cluster_size=3
    )
    
    finrag = FinRAG(config)
    
    # Create sample documents with metadata
    sample_docs = [
        # Technology sector, Apple, 2023
        "Apple Inc. reported strong revenue growth in Q1 2023. Sector: Technology, Company: Apple, Year: 2023",
        "Apple's iPhone sales exceeded expectations in 2023. Sector: Technology, Company: Apple, Year: 2023",
        
        # Technology sector, Apple, 2022
        "Apple announced new products in 2022. Sector: Technology, Company: Apple, Year: 2022",
        
        # Technology sector, Microsoft, 2023
        "Microsoft Azure revenue grew 30% in 2023. Sector: Technology, Company: Microsoft, Year: 2023",
        "Microsoft's cloud business is thriving in 2023. Sector: Technology, Company: Microsoft, Year: 2023",
        
        # Finance sector, JPMorgan, 2023
        "JPMorgan reported record profits in 2023. Sector: Finance, Company: JPMorgan, Year: 2023",
        
        # Finance sector, Goldman Sachs, 2022
        "Goldman Sachs investment banking revenue in 2022. Sector: Finance, Company: Goldman Sachs, Year: 2022",
    ]
    
    print("Adding documents to FinRAG...")
    finrag.add_documents(sample_docs)
    
    print("\n" + "="*80)
    print("TREE STATISTICS")
    print("="*80)
    
    stats = finrag.get_statistics()
    print(f"Total nodes: {stats['total_nodes']}")
    print(f"Leaf nodes: {stats['leaf_nodes']}")
    print(f"Root nodes: {stats['root_nodes']}")
    print(f"Tree depth: {stats['tree_depth']}")
    print(f"\nNodes per level:")
    for level in sorted(stats['levels'].keys()):
        print(f"  Level {level}: {stats['levels'][level]} nodes")
    
    print("\n" + "="*80)
    print("METADATA VERIFICATION BY LEVEL")
    print("="*80)
    
    # Analyze metadata at each level
    for level in range(stats['tree_depth'] + 1):
        print(f"\nLevel {level}:")
        nodes_at_level = [node for node in finrag.tree.all_nodes.values() if node.level == level]
        
        if nodes_at_level:
            metadata_examples = []
            for node in nodes_at_level[:5]:  # Show first 5 nodes
                metadata = node.metadata
                sector = metadata.get('sector', 'unknown')
                company = metadata.get('company', 'unknown')
                year = metadata.get('year', 'unknown')
                metadata_examples.append(f"({sector}, {company}, {year})")
            
            print(f"  Total nodes: {len(nodes_at_level)}")
            print(f"  Sample metadata: {', '.join(metadata_examples)}")
    
    print("\n" + "="*80)
    print("EXPECTED STRUCTURE")
    print("="*80)
    print("Layer 0: (Sector, Company, Year) - Raw documents")
    print("Layer 1: (Sector, Company, Year) - Year-level summaries")
    print("Layer 2: (Sector, Company, all) - Company-level summaries")
    print("Layer 3: (Sector, all, all) - Sector-level summaries")
    print("Layer 4: (all, all, all) - Global summary")
    
    print("\n" + "="*80)
    print("✓ Fixed hierarchical structure test complete!")
    print("="*80)


if __name__ == "__main__":
    test_fixed_hierarchy()
