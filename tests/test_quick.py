"""Quick test to verify the example works."""

from examples.metadata_clustering_example import get_tree_depth
from finrag import FinRAG
from finrag.config import FinRAGConfig

# Simple test document
test_docs = [
    "Apple Inc. 2023 Annual Report - Technology Sector. Revenue was $383 billion."
]

print("Testing metadata clustering example fix...")
print()

# Test with metadata clustering
config = FinRAGConfig()
config.use_metadata_clustering = True

finrag = FinRAG(config=config)
finrag.add_documents(test_docs)

# Test the helper function
num_layers = get_tree_depth(finrag.tree)
print(f"✓ Tree depth calculation works: {num_layers} layer(s)")

# Test accessing nodes by level
for level in range(num_layers):
    nodes_at_level = [n for n in finrag.tree.all_nodes.values() if n.level == level]
    print(f"✓ Level {level}: {len(nodes_at_level)} node(s)")

print()
print("✓ All tests passed! The example file should work now.")
