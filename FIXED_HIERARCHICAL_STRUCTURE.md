# Fixed Hierarchical Tree Structure

## Overview
The FinRAG system now implements a **fixed hierarchical clustering structure** based on metadata fields (Sector, Company, Year). This ensures predictable and interpretable tree organization.

## Tree Structure

```
Layer 4: Final Summary
├── Metadata: (all, all, all)
└── 1 node summarizing everything
    │
    ├─── Layer 3: Sector-level Summaries
    │    ├── Metadata: (Sector, all, all)
    │    └── Nodes grouped by Sector only
    │        │
    │        ├─── Layer 2: Company-level Summaries
    │        │    ├── Metadata: (Sector, Company, all)
    │        │    └── Nodes grouped by Sector + Company
    │        │        │
    │        │        ├─── Layer 1: Year-level Summaries
    │        │        │    ├── Metadata: (Sector, Company, Year)
    │        │        │    └── Nodes grouped by Sector + Company + Year
    │        │        │        │
    │        │        │        └─── Layer 0: Raw Documents
    │        │        │             ├── Metadata: (Sector, Company, Year)
    │        │        │             └── Original document chunks
```

## Layer Definitions

### Layer 0: Raw Documents
- **Description**: Original document chunks with full metadata
- **Metadata**: `(Sector, Company, Year)`
- **Example**: `(Technology, Apple, 2023)`
- **Purpose**: Store all raw financial data with complete metadata

### Layer 1: Year-level Clusters
- **Description**: Cluster documents by unique (Sector, Company, Year) combinations
- **Metadata**: `(Sector, Company, Year)`
- **Example**: `(Technology, Apple, 2023)`
- **Purpose**: Summarize all documents for a specific company in a specific year
- **Grouping**: Group by all three metadata fields

### Layer 2: Company-level Clusters
- **Description**: Squash years - cluster by (Sector, Company)
- **Metadata**: `(Sector, Company, "all")`
- **Example**: `(Technology, Apple, all)`
- **Purpose**: Summarize all years of data for a specific company
- **Grouping**: Group by Sector + Company only

### Layer 3: Sector-level Clusters
- **Description**: Squash companies - cluster by Sector only
- **Metadata**: `(Sector, "all", "all")`
- **Example**: `(Technology, all, all)`
- **Purpose**: Summarize all companies in a sector
- **Grouping**: Group by Sector only

### Layer 4: Global Summary
- **Description**: Final summary of all data
- **Metadata**: `("all", "all", "all")`
- **Example**: `(all, all, all)`
- **Purpose**: Provide a high-level overview of the entire dataset
- **Grouping**: Single cluster containing everything

## Implementation Details

### Clustering Logic
The fixed hierarchical clustering is implemented in `clustering.py`:

```python
def perform_fixed_hierarchical_clustering(
    self, nodes, embeddings, current_level, dim=10, threshold=0.5
):
    level_grouping = {
        1: ["sector", "company", "year"],  # Layer 1
        2: ["sector", "company"],          # Layer 2
        3: ["sector"],                     # Layer 3
        4: []                              # Layer 4 (all)
    }
```

### Metadata Inheritance
The metadata inheritance logic in `tree.py` ensures proper metadata propagation:

- **Level 1**: Inherit most common `(Sector, Company, Year)`
- **Level 2**: Inherit most common `(Sector, Company)`, set Year = "all"
- **Level 3**: Inherit most common `Sector`, set Company = "all", Year = "all"
- **Level 4**: Set all to "all"

### Configuration
The default configuration in `config.py` is set to:
- `tree_depth = 4` (to create 5 layers: 0-4)
- `use_metadata_clustering = True` (to enable fixed hierarchy)

## Benefits

1. **Predictability**: Each layer has a well-defined structure
2. **Interpretability**: Easy to understand what each layer represents
3. **Consistency**: Same structure across different datasets
4. **Hierarchical Navigation**: Natural drill-down from global to specific
5. **Metadata Preservation**: Metadata is systematically aggregated at each level

## Example Usage

```python
from finrag import FinRAG, FinRAGConfig

# Initialize with fixed hierarchical structure
config = FinRAGConfig(
    tree_depth=4,
    use_metadata_clustering=True
)

finrag = FinRAG(config)

# Add documents (they will be organized into the fixed hierarchy)
finrag.add_documents(["document1.txt", "document2.txt"])

# Query will traverse the hierarchy intelligently
result = finrag.query("What is Apple's revenue in 2023?")
```

## Retrieval Strategy

The fixed hierarchy enables efficient retrieval:
1. Start at Layer 4 for global context
2. Drill down to Layer 3 for sector-specific information
3. Continue to Layer 2 for company-specific data
4. Reach Layer 1 for year-specific details
5. Access Layer 0 for raw document chunks

This structure allows the system to provide context at multiple granularity levels.
