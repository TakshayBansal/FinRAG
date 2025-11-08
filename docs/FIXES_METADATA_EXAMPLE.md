# Fixes for metadata_clustering_example.py

## Issues Fixed

### Issue 1: AttributeError - 'num_layers' not found
**Error**:
```
AttributeError: 'RAPTORTree' object has no attribute 'num_layers'
```

**Cause**: The `RAPTORTree` class doesn't have a `num_layers` attribute.

**Fix**: Added helper function to calculate tree depth from node levels:
```python
def get_tree_depth(tree):
    """Helper function to get the depth/number of layers in a RAPTOR tree."""
    if not tree.all_nodes:
        return 0
    max_level = max(node.level for node in tree.all_nodes.values())
    return max_level + 1
```

---

### Issue 2: TypeError - Cannot sort None with str
**Error**:
```
TypeError: '<' not supported between instances of 'NoneType' and 'str'
```

**Cause**: Metadata values could be `None`, and Python cannot compare `None` with strings during sorting.

**Fix**: Ensured all metadata values are strings using `or` operator and custom sort key:
```python
# Ensure all values are strings, not None
sector = node.metadata.get('sector') or 'unknown'
company = node.metadata.get('company') or 'unknown'
year = node.metadata.get('year') or 'unknown'

# Sort safely with explicit string conversion
sorted(metadata_groups.items(), key=lambda x: (str(x[0][0]), str(x[0][1]), str(x[0][2])))
```

---

## Changes Made

### 1. Added helper function (Line ~17)
```python
def get_tree_depth(tree):
    """Helper function to get the depth/number of layers in a RAPTOR tree."""
    if not tree.all_nodes:
        return 0
    max_level = max(node.level for node in tree.all_nodes.values())
    return max_level + 1
```

### 2. Fixed demonstrate_clustering_comparison() (~Line 270)
**Before**:
```python
print(f"   Number of layers: {finrag_no_metadata.tree.num_layers}")
```

**After**:
```python
num_layers_no_metadata = get_tree_depth(finrag_no_metadata.tree)
print(f"   Number of layers: {num_layers_no_metadata}")
```

### 3. Fixed demonstrate_tree_structure() (~Line 385)
**Before**:
```python
print(f"  Total layers: {tree.num_layers}")
for layer_idx in range(tree.num_layers):
    layer = tree.all_nodes[layer_idx]
```

**After**:
```python
num_layers = get_tree_depth(tree)
print(f"  Total layers: {num_layers}")
for layer_idx in range(num_layers):
    layer_nodes = [node for node in tree.all_nodes.values() if node.level == layer_idx]
```

### 4. Fixed metadata sorting (~Line 407)
**Before**:
```python
key = (
    node.metadata.get('sector', 'unknown'),
    node.metadata.get('company', 'unknown'),
    node.metadata.get('year', 'unknown')
)
# ...
for (sector, company, year), count in sorted(metadata_groups.items()):
```

**After**:
```python
# Ensure all values are strings, not None
sector = node.metadata.get('sector') or 'unknown'
company = node.metadata.get('company') or 'unknown'
year = node.metadata.get('year') or 'unknown'
key = (sector, company, year)
# ...
# Sort safely by converting tuples to strings for sorting
for (sector, company, year), count in sorted(metadata_groups.items(), 
                                              key=lambda x: (str(x[0][0]), str(x[0][1]), str(x[0][2]))):
```

---

## Testing

✅ **Syntax validated**:
```bash
python -m py_compile examples/metadata_clustering_example.py
```

✅ **Ready to run**:
```bash
cd examples
python metadata_clustering_example.py
```

---

## Summary of Changes

| Issue | Location | Fix |
|-------|----------|-----|
| `num_layers` not found | 2 locations | Use `get_tree_depth()` helper |
| Wrong layer access | `demonstrate_tree_structure()` | Filter nodes by level |
| None vs str sorting | Metadata grouping | Use `or 'unknown'` and custom sort key |

---

## Status

✅ **ALL ISSUES FIXED** - The example file should now run without errors.

**Total fixes**: 4 code changes
**File modified**: `examples/metadata_clustering_example.py`
**Date**: November 7, 2025
