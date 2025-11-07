"""
Visual representation of the fixed hierarchical tree structure.
This script prints a visual diagram showing how the tree is organized.
"""

def print_tree_diagram():
    """Print a visual representation of the fixed hierarchical structure."""
    
    diagram = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    FINRAG FIXED HIERARCHICAL TREE STRUCTURE                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────────────────────┐
│ LAYER 4: GLOBAL SUMMARY                                                      │
│ ────────────────────────────────────────────────────────────────────────     │
│ Metadata: (all, all, all)                                                    │
│ Nodes: 1 (single root node)                                                  │
│ Purpose: High-level overview of entire dataset                               │
│                                                                               │
│   Example:                                                                    │
│   ┌─────────────────────────────────────────────────────────────┐            │
│   │ Sum 1: all / all / all                                      │            │
│   │ "Financial markets showed mixed performance across          │            │
│   │  technology and finance sectors in 2022-2023..."            │            │
│   └─────────────────────────────────────────────────────────────┘            │
└──────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ Summarize (squash all)
                                      ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ LAYER 3: SECTOR SUMMARIES                                                    │
│ ────────────────────────────────────────────────────────────────────────     │
│ Metadata: (Sector, all, all)                                                 │
│ Nodes: ~9 (one per sector)                                                   │
│ Purpose: Sector-level insights                                               │
│ Action: Squash Sectors                                                       │
│                                                                               │
│   Examples:                                                                   │
│   ┌──────────────────────────┐  ┌──────────────────────────┐                │
│   │ Sum 1: Technology/all/all│  │ Sum 2: Finance/all/all   │                │
│   │ "Tech sector showed..."  │  │ "Finance sector grew..." │                │
│   └──────────────────────────┘  └──────────────────────────┘                │
└──────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ Summarize (squash companies)
                                      ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ LAYER 2: COMPANY SUMMARIES                                                   │
│ ────────────────────────────────────────────────────────────────────────     │
│ Metadata: (Sector, Company, all)                                             │
│ Nodes: ~135 (one per sector-company pair)                                    │
│ Purpose: Company-level performance across all years                          │
│ Action: Squash Companies                                                     │
│                                                                               │
│   Examples:                                                                   │
│   ┌─────────────────────────┐  ┌─────────────────────────┐                  │
│   │ Sum 1: Tech/Apple/all   │  │ Sum 2: Tech/Microsoft/  │                  │
│   │ "Apple's performance    │  │ all                     │                  │
│   │  across 2022-2023..."   │  │ "Microsoft Azure grew..."│                 │
│   └─────────────────────────┘  └─────────────────────────┘                  │
└──────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ Summarize (squash years)
                                      ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ LAYER 1: YEAR SUMMARIES                                                      │
│ ────────────────────────────────────────────────────────────────────────     │
│ Metadata: (Sector, Company, Year)                                            │
│ Nodes: ~741 (one per sector-company-year triplet)                            │
│ Purpose: Specific company performance in specific year                       │
│ Action: Squash Years                                                         │
│                                                                               │
│   Examples:                                                                   │
│   ┌───────────────────────┐  ┌───────────────────────┐                      │
│   │ Sum 1: Tech/Apple/2023│  │ Sum 2: Tech/Apple/2022│                      │
│   │ "In 2023, Apple's     │  │ "In 2022, Apple..."   │                      │
│   │  iPhone sales..."     │  │                       │                      │
│   └───────────────────────┘  └───────────────────────┘                      │
└──────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ Cluster by metadata
                                      ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ LAYER 0: RAW DOCUMENTS                                                       │
│ ────────────────────────────────────────────────────────────────────────     │
│ Metadata: (Sector, Company, Year)                                            │
│ Nodes: ~6251 (all document chunks)                                           │
│ Purpose: Original source material                                            │
│ Action: Cluster all metadata                                                 │
│                                                                               │
│   Examples:                                                                   │
│   ┌──────────────────────┐  ┌──────────────────────┐                        │
│   │ Doc 1: Tech/Apple/   │  │ Doc 2: Tech/Apple/   │                        │
│   │ 2023                 │  │ 2023                 │                        │
│   │ "Apple Inc. reported"│  │ "iPhone 15 sales..." │                        │
│   └──────────────────────┘  └──────────────────────┘                        │
└──────────────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════════════╗
║                            METADATA TRANSFORMATION                            ║
╚══════════════════════════════════════════════════════════════════════════════╝

Layer 0 → 1: (Technology, Apple, 2023)  →  (Technology, Apple, 2023)
             Group by all three fields

Layer 1 → 2: (Technology, Apple, 2023)  →  (Technology, Apple, all)
             (Technology, Apple, 2022)  →  (Technology, Apple, all)
             Merge all years for same company

Layer 2 → 3: (Technology, Apple, all)    →  (Technology, all, all)
             (Technology, Microsoft, all) →  (Technology, all, all)
             Merge all companies in same sector

Layer 3 → 4: (Technology, all, all)     →  (all, all, all)
             (Finance, all, all)        →  (all, all, all)
             Merge all sectors into final summary

╔══════════════════════════════════════════════════════════════════════════════╗
║                              RETRIEVAL FLOW                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

Query: "What was Apple's revenue in 2023?"

Step 1: Start at Layer 4 (all/all/all)
        Check if query needs global context → No

Step 2: Move to Layer 3 (Technology/all/all)
        Find relevant sector → Technology

Step 3: Move to Layer 2 (Technology/Apple/all)
        Find relevant company → Apple

Step 4: Move to Layer 1 (Technology/Apple/2023)
        Find relevant year → 2023

Step 5: Retrieve from Layer 0 (raw documents)
        Get specific document chunks about Apple 2023

Result: Documents retrieved with multi-level context
        - Global context from Layer 4
        - Sector context from Layer 3
        - Company context from Layer 2
        - Year-specific from Layer 1
        - Detailed data from Layer 0

╔══════════════════════════════════════════════════════════════════════════════╗
║                               KEY BENEFITS                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

✓ Predictable Structure: Same hierarchy for every dataset
✓ Interpretable Layers: Each layer has clear semantic meaning
✓ Multi-Granularity: Answer queries at different detail levels
✓ Efficient Retrieval: Navigate directly to relevant parts
✓ Metadata Preservation: Financial context maintained throughout
✓ Scalable: Handles large datasets with sub-clustering
"""
    
    print(diagram)


if __name__ == "__main__":
    print_tree_diagram()
