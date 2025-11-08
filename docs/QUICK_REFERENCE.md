# Fixed Hierarchical Structure - Quick Reference

## Summary
The FinRAG RAPTOR tree now uses a **fixed 5-layer hierarchical structure** (Layers 0-4) based on metadata fields: Sector, Company, and Year.

## Layer Structure (Bottom to Top)

| Layer | Description | Metadata | Action |
|-------|-------------|----------|--------|
| **0** | Raw Documents | (Sector, Company, Year) | Cluster all metadata |
| **1** | Year Summaries | (Sector, Company, Year) | Squash Years |
| **2** | Company Summaries | (Sector, Company, **all**) | Squash Companies |
| **3** | Sector Summaries | (Sector, **all**, **all**) | Squash Sectors |
| **4** | Global Summary | (**all**, **all**, **all**) | Final summary |

## What Changed

### Before (Dynamic Clustering)
- Unpredictable number of layers
- Variable tree structure
- Metadata might be lost
- Hard to interpret

### After (Fixed Hierarchy)
- Always 5 layers (0-4)
- Predictable structure
- Metadata systematically preserved
- Easy to understand

## Key Files Modified

1. **`src/finrag/core/clustering.py`**
   - Added `perform_fixed_hierarchical_clustering()`
   - Routes clustering based on current level

2. **`src/finrag/core/tree.py`**
   - Updated `_inherit_metadata_from_children()` with level awareness
   - Modified `_build_level()` to pass current level
   - Changed default `max_depth` to 4

3. **`src/finrag/config.py`**
   - Updated default `tree_depth` to 4

## How to Use

### Default Behavior (Fixed Hierarchy Enabled)
```python
from finrag import FinRAG

# Uses fixed hierarchy by default
finrag = FinRAG()
finrag.add_documents(documents)
result = finrag.query("Your question")
```

### Custom Configuration
```python
from finrag import FinRAG, FinRAGConfig

config = FinRAGConfig(
    tree_depth=4,              # Layers 0-4
    use_metadata_clustering=True,  # Enable fixed hierarchy
    max_cluster_size=100,      # Max nodes per cluster
    min_cluster_size=5         # Min nodes per cluster
)

finrag = FinRAG(config)
```

### Disable Fixed Hierarchy (Use Old Dynamic Clustering)
```python
config = FinRAGConfig(
    use_metadata_clustering=False  # Disable fixed hierarchy
)
```

## Metadata Propagation

### Layer 0 → 1
- **Input**: (Technology, Apple, 2023)
- **Output**: (Technology, Apple, 2023)
- **Logic**: Keep all metadata

### Layer 1 → 2
- **Input**: (Technology, Apple, 2023), (Technology, Apple, 2022)
- **Output**: (Technology, Apple, **all**)
- **Logic**: Merge years for same company

### Layer 2 → 3
- **Input**: (Technology, Apple, all), (Technology, Microsoft, all)
- **Output**: (Technology, **all**, **all**)
- **Logic**: Merge companies in same sector

### Layer 3 → 4
- **Input**: (Technology, all, all), (Finance, all, all)
- **Output**: (**all**, **all**, **all**)
- **Logic**: Merge all sectors

## Testing

```bash
# Test the structure
python test_fixed_hierarchy.py

# Run examples
python examples/metadata_clustering_example.py

# Visualize structure
python visualize_structure.py
```

## Documentation Files

1. **`FIXED_HIERARCHICAL_STRUCTURE.md`** - Detailed explanation
2. **`IMPLEMENTATION_SUMMARY.md`** - Changes and overview
3. **`QUICK_REFERENCE.md`** - This file
4. **`visualize_structure.py`** - Visual diagram

## Common Questions

### Q: Do I need to change my code?
**A:** No, the fixed hierarchy is now the default. Your existing code will work.

### Q: Can I still use dynamic clustering?
**A:** Yes, set `use_metadata_clustering=False` in config.

### Q: What if my documents don't have metadata?
**A:** The system will extract metadata automatically or use "unknown" values.

### Q: How do I customize the layers?
**A:** You can adjust `tree_depth`, `max_cluster_size`, and `min_cluster_size` in config.

### Q: Will this work with my existing saved trees?
**A:** Old trees will still load, but new trees will use the fixed structure.

## Benefits

✅ **Predictable**: Same structure every time  
✅ **Interpretable**: Clear meaning for each layer  
✅ **Scalable**: Handles large datasets efficiently  
✅ **Metadata-aware**: Financial context preserved  
✅ **Multi-granularity**: Answer queries at different levels  

## Example Query Flow

**Query**: "What was Apple's revenue in 2023?"

1. **Layer 4** (all/all/all): Check global context
2. **Layer 3** (Technology/all/all): Identify sector
3. **Layer 2** (Technology/Apple/all): Focus on company
4. **Layer 1** (Technology/Apple/2023): Find specific year
5. **Layer 0**: Retrieve raw documents

**Result**: Context from all layers for comprehensive answer

---

**Status**: ✅ Implemented and Ready to Use

For more details, see `FIXED_HIERARCHICAL_STRUCTURE.md` and `IMPLEMENTATION_SUMMARY.md`.
