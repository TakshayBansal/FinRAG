# 🌳 FinRAG Tree Management Guide

## Overview

FinRAG now uses a **pre-built tree approach** for efficiency. Instead of rebuilding the tree every time you run code, you:

1. **Build once** from all PDFs in `data/` folder
2. **Load instantly** in any example or application
3. **Rebuild only** when PDFs change

This saves time, reduces API costs, and ensures consistency across all queries.

---

## 🚀 Quick Start

### Step 1: Add Your PDFs

Place all your annual reports and financial documents in the `data/` folder:

```
FinRAG/
└── data/
    ├── TCS_2023.pdf
    ├── TCS_2024.pdf
    ├── Wipro_2024.pdf
    └── ... (add more PDFs)
```

### Step 2: Build the Tree (One Time)

Run the build script:

```bash
python scripts/build_tree.py
```

This will:
- Process all PDFs in `data/` folder
- Extract metadata (sector, company, year)
- Build hierarchical RAPTOR tree
- Save to `finrag_tree/` directory

**Expected time**: 2-5 minutes for 3-5 documents

### Step 3: Use the Tree (Every Time)

Now all examples and applications load the pre-built tree instantly:

```bash
# Run main example
python examples/main.py

# Run stock scoring
python examples/stock_scoring_example.py

# Run any other example
python examples/example.py
```

**No rebuilding needed!** The tree loads in seconds.

---

## 📊 How It Works

### Before (Old Approach)
```
Run main.py
  ↓
Load 1 PDF
  ↓
Build tree (3-5 minutes)
  ↓
Query
  ↓
Exit (tree lost)

Run again = rebuild everything! ❌
```

### Now (New Approach)
```
Build tree once (5 minutes)
  ↓
finrag_tree/ saved ✓
  ↓
Run main.py → Load tree (10 seconds) → Query ✓
Run scoring.py → Load tree (10 seconds) → Query ✓
Run example.py → Load tree (10 seconds) → Query ✓

Same tree, instant loading! ✅
```

---

## 🔧 Usage Examples

### Build Tree

```bash
# Basic build (uses data/ folder)
python scripts/build_tree.py

# Build with custom directory
python scripts/manage_tree.py build --data-dir ./my_pdfs --output-dir ./my_tree

# Build without filtering (not recommended, higher costs)
python scripts/manage_tree.py build --no-filtering
```

### View Statistics

```bash
# Show tree stats
python scripts/manage_tree.py stats

# Output:
# Tree Statistics:
#   total_nodes: 312
#   max_depth: 4
#   total_clusters: 67
```

### Query Tree Directly

```bash
# Quick query from command line
python scripts/manage_tree.py query "What is TCS' revenue in 2024?"

# With specific retrieval method
python scripts/manage_tree.py query "Compare TCS and Wipro" --method collapsed_tree
```

### Use in Your Code

```python
from finrag import FinRAG, FinRAGConfig
from pathlib import Path

# Initialize
config = FinRAGConfig()
finrag = FinRAG(config)

# Load pre-built tree
tree_path = Path("finrag_tree")
finrag.load(str(tree_path))

# Query immediately!
result = finrag.query("Your question here")
print(result['answer'])
```

---

## 🗂️ Directory Structure

```
FinRAG/
├── data/                      # 📁 Place PDFs here
│   ├── TCS_2023.pdf
│   ├── TCS_2024.pdf
│   └── Wipro_2024.pdf
│
├── finrag_tree/              # 🌳 Pre-built tree (auto-generated)
│   ├── tree_structure.pkl    # Tree nodes and structure
│   ├── embeddings.npy        # Node embeddings
│   └── config.json           # Config used to build
│
├── scripts/                   # 🛠️ Management tools
│   ├── build_tree.py         # Build tree from PDFs
│   ├── manage_tree.py        # CLI tool for tree management
│   └── README.md             # Scripts documentation
│
└── examples/                  # 📚 All examples load pre-built tree
    ├── main.py               # ✓ Uses finrag_tree/
    ├── stock_scoring_example.py  # ✓ Uses finrag_tree/
    ├── example.py            # ✓ Uses finrag_tree/
    └── ...
```

---

## 🔄 Updating the Tree

### When to Rebuild

Rebuild the tree when:
- ✅ You add new PDF files to `data/`
- ✅ You remove PDF files from `data/`
- ✅ You update existing PDFs
- ✅ You change parsing configuration (e.g., enable/disable filtering)

**No need to rebuild** when:
- ❌ Just running queries
- ❌ Changing retrieval methods
- ❌ Updating example code

### How to Rebuild

Simply run the build script again:

```bash
python scripts/build_tree.py
```

The new tree will replace the old one in `finrag_tree/`.

---

## ⚙️ Configuration

### Enable Filtered Parsing (Recommended)

Edit `scripts/build_tree.py`:

```python
config = FinRAGConfig()
config.use_filtered_parsing = True  # Saves 60-80% on embedding costs
config.use_metadata_clustering = True  # Hierarchical organization
```

**Filtered parsing**:
- Extracts only key sections (financials, risks, governance, etc.)
- Reduces tokens by 60-80%
- Maintains accuracy for financial queries
- **Recommended for production use**

### Custom Sections

To extract specific sections only:

```python
from finrag.utils import FilteredDocumentParser

custom_sections = [
    "financial_statements",
    "revenue_and_profitability", 
    "risk_factors",
    "investments_and_capex"
]

# In build_tree.py, pass sections_to_extract when loading PDFs
text = finrag.load_pdf(pdf_path, sections_to_extract=custom_sections)
```

---

## 🎯 Benefits

### 1. **Speed**
- Build once: 5 minutes
- Load anytime: 10 seconds
- 30x faster for repeated use

### 2. **Cost Savings**
- Embeddings created once
- Reused across all queries
- Filtered parsing saves 60-80% additional

### 3. **Consistency**
- Same tree for all applications
- Reproducible results
- Easy debugging

### 4. **Multi-Document Support**
- Single tree from all PDFs
- Cross-document queries work
- Compare companies easily

### 5. **Development Efficiency**
- No waiting during development
- Instant testing
- Faster iteration

---

## 🔍 Troubleshooting

### Error: Tree not found

```
❌ Tree not found at: finrag_tree
```

**Solution**: Build the tree first
```bash
python scripts/build_tree.py
```

### Error: No PDFs found

```
❌ No PDF files found in data/
```

**Solution**: Add PDF files to `data/` folder

### Error: Module not found

```
ModuleNotFoundError: No module named 'finrag'
```

**Solution**: Install FinRAG in development mode
```bash
pip install -e .
```

### Error: API key not set

```
Error: OPENAI_API_KEY not found
```

**Solution**: Create `.env` file with your API keys
```bash
cp .env.example .env
# Edit .env and add your keys
```

### Tree seems outdated

**Solution**: Rebuild the tree
```bash
python scripts/build_tree.py
```

---

## 📈 Performance Tips

### 1. Use Filtered Parsing
Reduces costs by 60-80% with minimal accuracy loss:
```python
config.use_filtered_parsing = True
```

### 2. Enable Metadata Clustering
Better organization for financial documents:
```python
config.use_metadata_clustering = True
```

### 3. Optimize Chunk Size
For financial documents, smaller chunks work better:
```python
config.chunk_size = 512
config.chunk_overlap = 100
```

### 4. Choose Right Retrieval Method
- `tree_traversal`: Best for broad questions
- `collapsed_tree`: Best for specific facts
- `top_k`: Fastest but less comprehensive

---

## 🔐 Security Notes

- `.env` file contains API keys - **never commit to git**
- `finrag_tree/` contains embeddings - safe to commit if desired
- PDFs in `data/` - check if they contain sensitive information

---

## 📚 Additional Resources

- **Main README**: `../README.md` - Overall FinRAG documentation
- **Scripts README**: `scripts/README.md` - Detailed script documentation
- **Stock Scoring Guide**: `STOCK_SCORING_GUIDE.md` - Ensemble scoring system
- **Filtered Parsing Guide**: `FILTERED_PARSING_GUIDE.md` - Content filtering

---

## 🤝 Contributing

When adding new features:
1. Maintain the pre-built tree pattern
2. Load from `finrag_tree/` by default
3. Document any new build options
4. Update this guide if workflow changes

---

## 📝 Summary

**Old Way**:
```bash
python main.py  # Builds tree every time (5 min)
python main.py  # Builds tree again (5 min) ❌
```

**New Way**:
```bash
python scripts/build_tree.py  # Once (5 min)
python main.py               # Instant ✅
python stock_scoring.py      # Instant ✅
python example.py            # Instant ✅
```

**Result**: Faster development, lower costs, better experience! 🚀
