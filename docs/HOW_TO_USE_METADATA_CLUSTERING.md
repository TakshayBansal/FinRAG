# How to Use Metadata Clustering - Step by Step

## 🎯 Goal
This guide will walk you through using the metadata clustering feature in FinRAG.

---

## 📋 Prerequisites

### 1. Check Installation
```bash
cd "c:\Users\Takshay\Desktop\Coding\Pathway\RAG\FinRAG"
python -c "import finrag; print('✅ FinRAG installed')"
```

### 2. Verify API Key
```bash
# Check .env file exists
Get-Content .env | Select-String "OPENAI_API_KEY"
```

If not found, create `.env`:
```bash
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

---

## 🚀 Quick Start (5 minutes)

### Step 1: Run the Example

Open PowerShell and run:

```powershell
cd "c:\Users\Takshay\Desktop\Coding\Pathway\RAG\FinRAG\examples"
python metadata_clustering_example.py
```

### Step 2: Interact with Examples

The script will show you 5 demonstrations. Press **Enter** after each:

1. **Metadata Extraction** - See how sector/company/year are extracted
2. **Basic Clustering** - See metadata clustering in action
3. **Comparison** - See difference with/without metadata
4. **Custom Keys** - Learn to customize metadata fields
5. **Tree Structure** - Visualize the hierarchical tree

### Step 3: Review Output

You'll see detailed output like:

```
Document 1:
Preview: JPMorgan Chase & Co. 2023 Annual Report - Finance Sector...

Extracted Metadata:
  - Sector: finance
  - Company: JPMorgan Chase & Co.
  - Year: 2023

Created 3 chunks, each with metadata
```

---

## 🧪 Verify Installation (2 minutes)

### Run Tests

```powershell
cd "c:\Users\Takshay\Desktop\Coding\Pathway\RAG\FinRAG\tests"
python test_metadata_clustering.py
```

Expected output:
```
test_extract_year ... ok
test_extract_company_inc ... ok
test_extract_sector_finance ... ok
...
Ran 20 tests in 0.234s

OK
```

---

## 💻 Use in Your Code

### Basic Usage

Create a new file `my_test.py`:

```python
from finrag import FinRAG

# Initialize with metadata clustering (enabled by default)
finrag = FinRAG()

# Add your financial documents
documents = [
    """
    Apple Inc. 2023 Annual Report - Technology Sector
    
    Net sales for 2023 reached $383.3 billion...
    iPhone revenue was $200.6 billion...
    Services revenue grew to $85.2 billion...
    """,
    
    """
    JPMorgan Chase & Co. 2023 Annual Report - Finance Sector
    
    Total revenue for 2023 reached $158.1 billion...
    Investment banking fees totaled $7.4 billion...
    """,
]

# Add documents (metadata automatically extracted)
print("Adding documents...")
finrag.add_documents(documents)

# Query the system
print("\nQuerying...")
result = finrag.query("What were Apple's 2023 iPhone sales?")

print(f"\nAnswer: {result['answer']}")
print(f"Retrieved {len(result['retrieved_nodes'])} relevant chunks")
```

Run it:
```powershell
python my_test.py
```

---

## ⚙️ Customize Configuration

### Example: Different Metadata Keys

```python
from finrag import FinRAG
from finrag.config import FinRAGConfig

# Create custom config
config = FinRAGConfig()

# Option 1: Group by sector and year only (ignore company)
config.metadata_keys = ["sector", "year"]

# Option 2: Group by company only
config.metadata_keys = ["company"]

# Option 3: Disable metadata clustering
config.use_metadata_clustering = False

# Initialize with custom config
finrag = FinRAG(config=config)
```

---

## 📝 Document Format Best Practices

### ✅ Good Format (Metadata Will Be Extracted)

```
Apple Inc. 2023 Annual Report - Technology Sector

Financial Results:
Net sales: $383.3 billion
...
```

**Extracted**:
- Company: "Apple Inc."
- Year: "2023"
- Sector: "technology"

### ❌ Poor Format (Limited Metadata)

```
Annual Report

Sales were good this year.
```

**Extracted**: (empty or incomplete)

---

## 🎓 Understanding the Output

### Tree Structure

When you add documents, FinRAG builds a hierarchical tree:

```
Level 0 (Leaf Nodes - Your Chunks):
├─ JPMorgan/Finance/2023
│  ├─ Chunk 1: "Total revenue $158.1B..."
│  ├─ Chunk 2: "Investment banking $7.4B..."
│  └─ Chunk 3: "Credit loss $8.9B..."
│
└─ Apple/Technology/2023
   ├─ Chunk 1: "Net sales $383.3B..."
   └─ Chunk 2: "iPhone revenue $200.6B..."

Level 1 (Summaries):
├─ JPMorgan 2023 Financial Summary
└─ Apple 2023 Performance Summary

Level 2 (Higher Level):
├─ Finance Sector 2023 Overview
└─ Technology Sector 2023 Overview
```

### Retrieval Process

When you query:

1. **Query Embedding Created**: "What were Apple's 2023 sales?"
2. **Tree Traversal**: Start at top, find most relevant path
3. **Retrieve Context**: Get Apple/Technology/2023 chunks
4. **Generate Answer**: Use GPT-4 with retrieved context

---

## 🔍 Troubleshooting

### Problem 1: No Metadata Extracted

**Symptom**: Metadata shows "Not found" for all fields

**Solution**:
- Ensure documents include company suffix (Inc, Corp, Ltd)
- Use 4-digit years (2023, not '23)
- Use sector keywords: technology, finance, healthcare, energy, retail, manufacturing, real estate, telecom

**Example Fix**:
```python
# ❌ Poor
"Annual report for 2023"

# ✅ Good
"Apple Inc. 2023 Annual Report - Technology Sector"
```

---

### Problem 2: Import Error

**Symptom**: `ModuleNotFoundError: No module named 'finrag'`

**Solution**:
```powershell
cd "c:\Users\Takshay\Desktop\Coding\Pathway\RAG\FinRAG"
pip install -e .
```

---

### Problem 3: API Key Error

**Symptom**: `Error: OpenAI API key not found`

**Solution**:
```powershell
# Create .env file
cd "c:\Users\Takshay\Desktop\Coding\Pathway\RAG\FinRAG"
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

---

### Problem 4: Example Runs But No Output

**Symptom**: Script runs but shows no answers

**Solution**: Check API quota and internet connection
```powershell
# Test API connection
python -c "from openai import OpenAI; client = OpenAI(); print(client.models.list())"
```

---

## 📚 Learn More

### Documentation Files (In Order of Importance)

1. **`METADATA_CLUSTERING_QUICK_REF.md`** - Quick lookup (5 min read)
2. **`METADATA_CLUSTERING_SUMMARY.md`** - Complete overview (10 min read)
3. **`docs/METADATA_CLUSTERING.md`** - User guide (15 min read)
4. **`docs/METADATA_CLUSTERING_ARCHITECTURE.md`** - Technical details (20 min read)

### Code Files

1. **`examples/metadata_clustering_example.py`** - Runnable examples
2. **`tests/test_metadata_clustering.py`** - Test suite
3. **`src/finrag/core/clustering.py`** - Clustering implementation
4. **`src/finrag/models/models.py`** - Metadata extraction

---

## 🎯 Common Use Cases

### Use Case 1: Compare Companies

```python
documents = [
    "Apple Inc. 2023 Annual Report - Technology Sector...",
    "Microsoft Corporation 2023 Annual Report - Technology Sector...",
]

finrag.add_documents(documents)
result = finrag.query("Compare Apple and Microsoft's 2023 revenue")
```

### Use Case 2: Year-over-Year Analysis

```python
documents = [
    "Company XYZ Inc. 2022 Annual Report - Finance Sector...",
    "Company XYZ Inc. 2023 Annual Report - Finance Sector...",
]

finrag.add_documents(documents)
result = finrag.query("How did Company XYZ's revenue change from 2022 to 2023?")
```

### Use Case 3: Sector Analysis

```python
config = FinRAGConfig()
config.metadata_keys = ["sector", "year"]  # Group by sector only

finrag = FinRAG(config=config)
# Now all companies in same sector are grouped together
```

---

## ✅ Success Checklist

After following this guide, you should be able to:

- [ ] Run the example file successfully
- [ ] See metadata extracted from documents
- [ ] Understand the two-stage clustering process
- [ ] Use metadata clustering in your own code
- [ ] Customize configuration options
- [ ] Format documents for optimal metadata extraction
- [ ] Troubleshoot common issues

---

## 🎓 Next Steps

1. **Try with Real Data**: Use your own financial documents
2. **Experiment**: Try different metadata keys configurations
3. **Optimize**: Adjust clustering parameters for your use case
4. **Extend**: Add new metadata fields or extraction patterns
5. **Integrate**: Use in your production workflows

---

## 💡 Pro Tips

1. **Consistent Naming**: Use same company names across documents
2. **Clear Metadata**: Put sector/company/year in document headers
3. **Batch Processing**: Add multiple documents at once for efficiency
4. **Cache Results**: Build tree once, query multiple times
5. **Monitor Quality**: Compare with/without metadata to see improvement

---

**You're all set! Start with the example file and experiment from there.** 🚀
