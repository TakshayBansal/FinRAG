"""
Quick verification that the fixed hierarchy is working.
This script confirms the configuration and shows what will happen.
"""

from finrag.config import FinRAGConfig

def verify_fixed_hierarchy_config():
    """Verify that the default configuration uses fixed hierarchy."""
    
    print("="*80)
    print("FIXED HIERARCHY CONFIGURATION VERIFICATION")
    print("="*80)
    print()
    
    # Create default config
    config = FinRAGConfig()
    
    print("Default Configuration Settings:")
    print(f"  tree_depth: {config.tree_depth}")
    print(f"  use_metadata_clustering: {config.use_metadata_clustering}")
    print(f"  metadata_keys: {config.metadata_keys}")
    print()
    
    # Verify it's correct for fixed hierarchy
    if config.tree_depth == 4 and config.use_metadata_clustering:
        print("✅ CONFIRMED: Fixed hierarchy is ENABLED by default")
        print()
        print("When you run metadata_clustering_example.py, you will get:")
        print("  - 5 layers (0-4)")
        print("  - Layer 0: (sector, company, year)")
        print("  - Layer 1: (sector, company, year)")
        print("  - Layer 2: (sector, company, all)")
        print("  - Layer 3: (sector, all, all)")
        print("  - Layer 4: (all, all, all)")
        print()
        print("Expected console output:")
        print("  Level 1 grouping by ['sector', 'company', 'year']: X groups")
        print("  Level 2 grouping by ['sector', 'company']: X groups")
        print("  Level 3 grouping by ['sector']: X groups")
        print("  Level 4 grouping by []: 1 groups")
        print()
        print("="*80)
        print("✅ Ready to run: python examples/metadata_clustering_example.py")
        print("="*80)
    else:
        print("⚠️ WARNING: Fixed hierarchy may not be enabled")
        print(f"  Expected: tree_depth=4, use_metadata_clustering=True")
        print(f"  Got: tree_depth={config.tree_depth}, use_metadata_clustering={config.use_metadata_clustering}")

if __name__ == "__main__":
    verify_fixed_hierarchy_config()
