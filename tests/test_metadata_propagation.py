"""
Test to verify metadata propagation up the tree.
"""

from finrag import FinRAG
from finrag.config import FinRAGConfig

# Test document with clear metadata
test_doc = """
Apple Inc. 2023 Annual Report - Technology Sector

Financial Performance:
Apple Inc. reported strong results for fiscal year 2023. Revenue reached $383 billion,
with iPhone sales driving the majority of growth. Services revenue also expanded significantly.

The technology sector leader continues to innovate with new products including the iPhone 15,
Apple Watch Series 9, and Vision Pro. The company maintains its position as a technology
sector pioneer with continued investment in research and development.
""" * 5  # Repeat to create enough content for multiple chunks

print("Testing metadata propagation in RAPTOR tree...")
print("=" * 80)

# Initialize with metadata clustering
config = FinRAGConfig()
config.use_metadata_clustering = True

finrag = FinRAG(config=config)
finrag.add_documents([test_doc])

# Check metadata at each layer
tree = finrag.tree

# Helper to get tree depth
def get_tree_depth(tree):
    if not tree.all_nodes:
        return 0
    max_level = max(node.level for node in tree.all_nodes.values())
    return max_level + 1

num_layers = get_tree_depth(tree)

print(f"\nTree has {num_layers} layers")
print("\nMetadata at each layer:")
print("-" * 80)

for level in range(num_layers):
    nodes_at_level = [n for n in tree.all_nodes.values() if n.level == level]
    print(f"\nLayer {level}: {len(nodes_at_level)} nodes")
    
    # Sample a few nodes to check metadata
    sample_size = min(3, len(nodes_at_level))
    for i, node in enumerate(nodes_at_level[:sample_size]):
        print(f"  Node {i+1}:")
        print(f"    - Text preview: {node.text[:80]}...")
        if hasattr(node, 'metadata') and node.metadata:
            print(f"    - Sector: {node.metadata.get('sector', 'NOT SET')}")
            print(f"    - Company: {node.metadata.get('company', 'NOT SET')}")
            print(f"    - Year: {node.metadata.get('year', 'NOT SET')}")
        else:
            print(f"    - Metadata: None or empty")

print("\n" + "=" * 80)
print("✓ Test completed!")
print("\nExpected result:")
print("  - Layer 0: Should have sector='technology', company='Apple Inc', year='2023'")
print("  - Layer 1+: Should INHERIT sector='technology', company='Apple Inc', year='2023'")
print("\nIf higher layers show 'NOT SET' or 'unknown', metadata propagation failed.")
