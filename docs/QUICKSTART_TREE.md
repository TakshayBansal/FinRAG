# 🚀 FinRAG Quick Start - Pre-built Tree Approach

## ⚡ 3-Step Quick Start

### Step 1: Add PDFs (30 seconds)
```bash
# Place your PDFs in the data folder
FinRAG/data/
├── TCS_2023.pdf
├── TCS_2024.pdf
└── Wipro_2024.pdf
```

### Step 2: Build Tree (5 minutes, ONE TIME)
```bash
cd FinRAG
python scripts/build_tree.py
```

**Wait for completion**:
```
================================================================================
BUILD COMPLETE!
================================================================================

✓ Processed 3 documents
✓ Built RAPTOR tree with 312 nodes
✓ Tree saved to: finrag_tree
```

### Step 3: Use FinRAG (10 seconds, EVERY TIME)
```bash
# All examples now load instantly!
python examples/main.py
python examples/stock_scoring_example.py
python examples/example.py
```

**That's it!** 🎉

---

## 📊 What You Get

### Before (Old Way) ❌
```
Every run:
- Load 1 PDF only
- Build tree: 5 minutes
- Query: works
- Exit: tree lost
- Next run: build again (5 minutes) 😫
```

### After (New Way) ✅
```
First time:
- Build tree from ALL PDFs: 5 minutes
- Save to finrag_tree/

Every run after:
- Load tree: 10 seconds ⚡
- Query: works
- Can query any company in tree
- No rebuilding needed! 😊
```

---

## 💡 Usage Examples

### Example 1: Basic Query
```python
from finrag import FinRAG, FinRAGConfig
from pathlib import Path

# Load pre-built tree
config = FinRAGConfig()
finrag = FinRAG(config)
finrag.load("finrag_tree")

# Query any company in the tree
result = finrag.query("What is TCS' revenue in 2024?")
print(result['answer'])
```

### Example 2: Compare Companies
```python
# Works because all companies are in the same tree!
result = finrag.query("Compare TCS and Wipro's profitability")
print(result['answer'])
```

### Example 3: Stock Scoring
```python
from finrag.scoring import EnsembleScorer, ScoringConfig

# Load tree
finrag = FinRAG(FinRAGConfig())
finrag.load("finrag_tree")

# Score any company
scorer = EnsembleScorer(ScoringConfig())
score = scorer.score_company(
    ticker="TCS.NS",
    company_name="TCS",
    finrag=finrag
)

print(f"Score: {score.score}/100")
print(f"Direction: {score.direction}")
```

---

## 🔄 Common Operations

### Add New PDFs
```bash
# 1. Add PDFs to data folder
cp new_company.pdf FinRAG/data/

# 2. Rebuild tree
python scripts/build_tree.py

# 3. Done! New PDFs are now in the tree
```

### Check Tree Stats
```bash
python scripts/manage_tree.py stats

# Output:
# Tree Statistics:
#   total_nodes: 312
#   max_depth: 4
#   total_clusters: 67
```

### Quick Query from CLI
```bash
python scripts/manage_tree.py query "What is the revenue?"
```

---

## 🎯 Key Points

### ✅ DO
- Build tree once from all PDFs
- Load tree in your code
- Query any company in the tree
- Rebuild when PDFs change

### ❌ DON'T
- Build tree every time you run code
- Load individual PDFs per query
- Worry about rebuilding (it's automatic)

---

## 📂 File Structure

```
FinRAG/
│
├── data/                     📁 Your PDFs here
│   ├── company1.pdf
│   └── company2.pdf
│
├── finrag_tree/             🌳 Auto-generated
│   ├── tree_structure.pkl
│   ├── embeddings.npy
│   └── config.json
│
├── scripts/
│   └── build_tree.py        ⭐ Run this once
│
└── examples/
    ├── main.py              ✅ Loads tree
    └── stock_scoring_example.py  ✅ Loads tree
```

---

## 🆘 Troubleshooting

### Error: Tree not found
```
❌ Tree not found at: finrag_tree
```
**Fix**: `python scripts/build_tree.py`

### Error: No PDFs
```
❌ No PDF files found in data/
```
**Fix**: Add PDFs to `data/` folder

---

## 🚀 Next Steps

1. ✅ Run `python scripts/build_tree.py`
2. ✅ Run `python examples/main.py` to test
3. ✅ Start building your application!

**Questions?** Check `TREE_MANAGEMENT_GUIDE.md` for detailed docs.

---

## 📈 Performance

| Operation | Time |
|-----------|------|
| Build tree (first time) | 5 min |
| Load tree (every time) | 10 sec |
| Query tree | 5-10 sec |

**Speed improvement: 30x faster after first build!** ⚡
