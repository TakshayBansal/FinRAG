# FinRAG Scripts

This folder contains utility scripts for FinRAG system management.

## 📋 Available Scripts

### 1. `build_tree.py` - Build Tree from All PDFs

**Purpose**: Build the RAPTOR tree once using all PDFs in the data folder. This creates a reusable index that can be loaded by all example files and applications.

**Usage**:
```bash
python scripts/build_tree.py
```

**What it does**:
1. Scans the `data/` folder for all PDF files
2. Processes each PDF (with optional filtered parsing)
3. Builds a single unified RAPTOR tree with metadata clustering
4. Saves the tree to `finrag_tree/` directory
5. Displays statistics about the built tree

**Configuration**:
The script uses settings from `.env` file and `FinRAGConfig`:
- `use_filtered_parsing`: Set to `True` to save 60-80% on embedding costs
- `use_metadata_clustering`: Set to `True` for hierarchical organization (Sector → Company → Year)

**Output**:
```
finrag_tree/
├── tree_structure.pkl     # Tree structure and nodes
├── embeddings.npy         # Node embeddings
└── config.json           # Configuration used
```

---

## 🔄 Workflow

### Initial Setup (Run Once)
1. Add all your PDF files to `data/` folder
2. Run `python scripts/build_tree.py`
3. Wait for tree building to complete (may take several minutes)
4. Tree is saved to `finrag_tree/`

### Using the Tree (Every Time)
All example files and applications now load the pre-built tree:

```python
from finrag import FinRAG, FinRAGConfig
from pathlib import Path

config = FinRAGConfig()
finrag = FinRAG(config)

# Load pre-built tree
tree_path = Path("finrag_tree")
finrag.load(str(tree_path))

# Now query immediately - no rebuilding needed!
result = finrag.query("Your question here")
```

### Updating the Tree
When you add/remove PDFs or want to rebuild:
1. Update PDFs in `data/` folder
2. Run `python scripts/build_tree.py` again
3. New tree replaces old one

---

## 📁 Directory Structure

```
FinRAG/
├── data/                   # Place all PDF files here
│   ├── company1_2023.pdf
│   ├── company1_2024.pdf
│   └── company2_2024.pdf
├── scripts/
│   └── build_tree.py      # Run this to build tree
├── finrag_tree/           # Generated tree (auto-created)
│   ├── tree_structure.pkl
│   ├── embeddings.npy
│   └── config.json
└── examples/              # All examples use pre-built tree
    ├── main.py
    ├── stock_scoring_example.py
    └── example.py
```

---

## ⚙️ Advanced Configuration

Edit `build_tree.py` to customize:

```python
# Enable/disable filtered parsing
config.use_filtered_parsing = True  # Saves 60-80% on costs

# Enable/disable metadata clustering
config.use_metadata_clustering = True  # Hierarchical organization

# Custom sections to extract (if filtered parsing enabled)
custom_sections = [
    "board_of_directors_changes",
    "financial_statements",
    "risk_factors",
    "investments_and_capex"
]
```

---

## 🚀 Benefits of Pre-built Tree

1. **Faster Development**: No rebuilding tree every time you run code
2. **Cost Savings**: Embeddings created once, reused many times
3. **Consistency**: Same tree across all queries and applications
4. **Easy Updates**: Just rebuild when data changes
5. **Multi-document**: Single tree from all PDFs for cross-document queries

---

## 🔍 Troubleshooting

### Tree not found error
```
❌ Tree not found at: finrag_tree
```
**Solution**: Run `python scripts/build_tree.py` first

### No PDFs found
```
❌ No PDF files found in data/
```
**Solution**: Add PDF files to `data/` folder

### Import errors
```
ModuleNotFoundError: No module named 'finrag'
```
**Solution**: Install FinRAG: `pip install -e .` from project root

### API key errors
```
OpenAI API key not found
```
**Solution**: Create `.env` file with API keys (copy from `.env.example`)

---

## 📊 Performance Tips

1. **Use Filtered Parsing**: Reduces embedding costs by 60-80%
   - Set `config.use_filtered_parsing = True`

2. **Metadata Clustering**: Better organization for financial documents
   - Set `config.use_metadata_clustering = True`

3. **Batch Processing**: The script processes PDFs in optimal batches

4. **Incremental Updates**: If you only changed 1 PDF, consider rebuilding only that section (advanced - requires custom code)

---

## 📝 Example Output

```
================================================================================
BUILDING FINRAG TREE FROM ALL PDFs
================================================================================

Initializing FinRAG system...

✓ Found 3 PDF files:
  - TCS_2023.pdf
  - TCS_2024.pdf
  - Wipro_2024.pdf

================================================================================
PROCESSING PDFs
================================================================================

[1/3] Processing: TCS_2023.pdf
--------------------------------------------------------------------------------
  Using filtered parsing to extract key sections...
  ✓ Loaded 125,430 characters

[2/3] Processing: TCS_2024.pdf
--------------------------------------------------------------------------------
  ✓ Loaded 132,156 characters

[3/3] Processing: Wipro_2024.pdf
--------------------------------------------------------------------------------
  ✓ Loaded 145,789 characters

✓ Successfully processed 3/3 PDFs

================================================================================
BUILDING RAPTOR TREE
================================================================================

This may take several minutes depending on the number of documents...
Chunking documents...
Created 245 chunks
Creating embeddings...
Created 245 embeddings
Building RAPTOR tree...

✓ Tree built successfully!

================================================================================
TREE STATISTICS
================================================================================

  total_nodes: 312
  max_depth: 4
  total_clusters: 67

================================================================================
SAVING TREE
================================================================================

Saving to: finrag_tree
✓ Tree saved successfully to finrag_tree

================================================================================
BUILD COMPLETE!
================================================================================

✓ Processed 3 documents
✓ Built RAPTOR tree with 312 nodes
✓ Tree saved to: finrag_tree

You can now use this tree in your applications by loading it:

    from finrag import FinRAG, FinRAGConfig
    
    config = FinRAGConfig()
    finrag = FinRAG(config)
    finrag.load("finrag_tree")
    
    # Now query the system
    result = finrag.query("Your question here")

To rebuild the tree with updated PDFs, run this script again:
    python scripts/build_tree.py
```
