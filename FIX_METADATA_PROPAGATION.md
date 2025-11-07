# Fix: Metadata Propagation in RAPTOR Tree

## Problem

When building the RAPTOR tree, metadata (sector, company, year) was only present in **Layer 0** (leaf nodes - original chunks). Higher layers (Layer 1, Layer 2, etc.) showed `unknown/unknown/unknown` because parent nodes didn't inherit metadata from their children.

### Example Output (Before Fix):
```
Layer 0:
  - Metadata groups:
    • finance/JPMorgan Chase & Co/2023: 51 nodes
    • technology/Apple Inc/2023: 102 nodes

Layer 1:
  - Metadata groups:
    • unknown/unknown/unknown: 16 nodes  ← Problem!

Layer 2:
  - Metadata groups:
    • unknown/unknown/unknown: 1 nodes   ← Problem!
```

## Root Cause

In `src/finrag/core/tree.py`, when creating parent nodes (summaries), the metadata dictionary only contained:
```python
metadata={
    "num_children": len(cluster_nodes),
    "cluster_idx": cluster_idx
}
```

**Missing**: sector, company, year from the children nodes!

## Solution

Added metadata inheritance from children to parent nodes:

### 1. Created `_inherit_metadata_from_children()` method

This method:
- Collects metadata values from all children
- For each field (sector, company, year):
  - Filters out `None` and `'unknown'` values
  - Selects the **most common value** (majority vote)
- Returns inherited metadata dictionary

```python
def _inherit_metadata_from_children(self, children: List[ClusterNode]) -> Dict[str, Any]:
    """
    Inherit metadata from children nodes.
    Takes the most common value for each metadata field.
    """
    if not children:
        return {}
    
    metadata_fields = ['sector', 'company', 'year']
    inherited = {}
    
    for field in metadata_fields:
        # Get all non-None, non-'unknown' values
        values = []
        for child in children:
            if hasattr(child, 'metadata') and child.metadata:
                value = child.metadata.get(field)
                if value and value != 'unknown':
                    values.append(value)
        
        if values:
            # Use the most common value
            from collections import Counter
            most_common = Counter(values).most_common(1)[0][0]
            inherited[field] = most_common
    
    return inherited
```

### 2. Updated `_build_level()` to use inherited metadata

**Before**:
```python
parent_node = ClusterNode(
    node_id=f"level_{level}_cluster_{cluster_idx}",
    text=summary,
    embedding=summary_embedding,
    children=cluster_nodes,
    level=level,
    metadata={
        "num_children": len(cluster_nodes),
        "cluster_idx": cluster_idx
    }
)
```

**After**:
```python
# Inherit metadata from children
inherited_metadata = self._inherit_metadata_from_children(cluster_nodes)
inherited_metadata.update({
    "num_children": len(cluster_nodes),
    "cluster_idx": cluster_idx
})

parent_node = ClusterNode(
    node_id=f"level_{level}_cluster_{cluster_idx}",
    text=summary,
    embedding=summary_embedding,
    children=cluster_nodes,
    level=level,
    metadata=inherited_metadata  # Now includes sector/company/year!
)
```

## How It Works

### Example: Building Layer 1 from Layer 0

**Layer 0 Children** (in one cluster):
- Node 1: `{sector: 'technology', company: 'Apple Inc', year: '2023'}`
- Node 2: `{sector: 'technology', company: 'Apple Inc', year: '2023'}`
- Node 3: `{sector: 'technology', company: 'Apple Inc', year: '2023'}`

**Layer 1 Parent** (after inheritance):
- `{sector: 'technology', company: 'Apple Inc', year: '2023', num_children: 3, cluster_idx: 0}`

### Mixed Metadata Scenario

If a cluster has mixed metadata (shouldn't happen with metadata clustering, but possible):

**Children**:
- Node 1: `{sector: 'technology', company: 'Apple Inc', year: '2023'}`
- Node 2: `{sector: 'technology', company: 'Apple Inc', year: '2023'}`
- Node 3: `{sector: 'finance', company: 'JPMorgan', year: '2023'}`

**Parent** (majority vote):
- `{sector: 'technology', company: 'Apple Inc', year: '2023'}` ← Most common values

## Expected Output (After Fix)

```
Layer 0:
  - Metadata groups:
    • finance/JPMorgan Chase & Co/2023: 51 nodes
    • technology/Apple Inc/2023: 102 nodes

Layer 1:
  - Metadata groups:
    • finance/JPMorgan Chase & Co/2023: 2 nodes  ← Fixed!
    • technology/Apple Inc/2023: 4 nodes         ← Fixed!

Layer 2:
  - Metadata groups:
    • technology/Apple Inc/2023: 1 nodes         ← Fixed!
```

## Testing

### Run the test script:
```bash
python test_metadata_propagation.py
```

### Re-run the example:
```bash
cd examples
python metadata_clustering_example.py
```

**Look for**: The `demonstrate_tree_structure()` output should now show proper metadata at all layers, not just Layer 0.

## Files Modified

- ✅ `src/finrag/core/tree.py`
  - Added `_inherit_metadata_from_children()` method
  - Updated `_build_level()` to inherit metadata

## Benefits

1. **Consistent metadata throughout tree** - All layers maintain sector/company/year info
2. **Better visualization** - Can see which company/sector each summary represents
3. **Future retrieval improvements** - Could filter by metadata at any level
4. **Maintains clustering semantics** - Parent nodes reflect their children's business context

## Status

✅ **FIXED** - Metadata now propagates from children to parents using majority vote.

**Date**: November 7, 2025
