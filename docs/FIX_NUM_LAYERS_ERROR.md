# Fix for AttributeError: 'RAPTORTree' object has no attribute 'num_layers'

## Issue

The example file `metadata_clustering_example.py` was trying to access `tree.num_layers` which doesn't exist in the `RAPTORTree` class.

**Error**:
```
AttributeError: 'RAPTORTree' object has no attribute 'num_layers'
```

## Root Cause

The `RAPTORTree` class stores nodes with a `level` attribute but doesn't have a `num_layers` property. The tree structure is stored in `all_nodes` dictionary where each node has its level.

## Solution

Added a helper function `get_tree_depth()` that calculates the number of layers by finding the maximum level among all nodes:

```python
def get_tree_depth(tree):
    """Helper function to get the depth/number of layers in a RAPTOR tree."""
    if not tree.all_nodes:
        return 0
    max_level = max(node.level for node in tree.all_nodes.values())
    return max_level + 1
```

## Changes Made

### File: `examples/metadata_clustering_example.py`

**1. Added helper function at the top** (after imports):
```python
def get_tree_depth(tree):
    """Helper function to get the depth/number of layers in a RAPTOR tree."""
    if not tree.all_nodes:
        return 0
    max_level = max(node.level for node in tree.all_nodes.values())
    return max_level + 1
```

**2. Fixed `demonstrate_clustering_comparison()` function**:

Before:
```python
print(f"   Number of layers: {finrag_no_metadata.tree.num_layers}")
```

After:
```python
num_layers_no_metadata = get_tree_depth(finrag_no_metadata.tree)
print(f"   Number of layers: {num_layers_no_metadata}")
```

**3. Fixed `demonstrate_tree_structure()` function**:

Before:
```python
print(f"  Total layers: {tree.num_layers}")
for layer_idx in range(tree.num_layers):
    layer = tree.all_nodes[layer_idx]
```

After:
```python
num_layers = get_tree_depth(tree)
print(f"  Total layers: {num_layers}")
for layer_idx in range(num_layers):
    # Get all nodes at this layer
    layer_nodes = [node for node in tree.all_nodes.values() if node.level == layer_idx]
    layer = layer_nodes
```

## How It Works

The `RAPTORTree` class structure:
- **Level 0**: Leaf nodes (original chunks)
- **Level 1**: First layer of summaries
- **Level 2**: Second layer of summaries (if tree is deep enough)
- etc.

The helper function:
1. Checks if tree has any nodes
2. Finds the maximum level value among all nodes
3. Returns `max_level + 1` (since levels are 0-indexed)

## Testing

**Syntax check**: ✅ Passed
```bash
python -m py_compile examples/metadata_clustering_example.py
```

## Usage

Now the example file should work correctly:

```bash
cd examples
python metadata_clustering_example.py
```

## Alternative Solutions Considered

### Option 1: Add `num_layers` property to RAPTORTree
- Pros: More elegant, matches API expectations
- Cons: Requires modifying core code, needs to be maintained

### Option 2: Use helper function (chosen)
- Pros: No core code changes, easy to understand
- Cons: Extra function needed

We chose Option 2 to avoid modifying the core tree implementation.

## Files Modified

- ✅ `examples/metadata_clustering_example.py` - Added helper function and fixed 2 occurrences

## Status

✅ **FIXED** - The example file should now run without errors.
