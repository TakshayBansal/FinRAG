# Metadata Clustering - Quick Reference

## Files Created

### 1. Example File
**Location**: `examples/metadata_clustering_example.py`

**What it does**:
- Demonstrates metadata extraction from financial documents
- Shows 5 complete examples with interactive prompts
- Includes sample financial documents (JPMorgan, Apple, Tesla, etc.)
- Compares clustering with and without metadata
- Visualizes tree structure

**Run it**:
```bash
cd examples
python metadata_clustering_example.py
```

**Features**:
- 6 sample financial documents with metadata
- 5 demonstration functions
- Interactive (press Enter between examples)
- Comprehensive output with explanations

---

### 2. Test File
**Location**: `tests/test_metadata_clustering.py`

**What it tests**:
- Metadata extraction (year, company, sector)
- Metadata grouping logic
- Two-stage clustering process
- Configuration options
- Edge cases and error handling

**Run it**:
```bash
cd tests
python test_metadata_clustering.py
```

**Test coverage**:
- 20+ unit tests
- 5 test classes
- All metadata functionality

---

### 3. Documentation
**Location**: `docs/METADATA_CLUSTERING.md`

**Contents**:
- Overview of two-stage clustering
- Quick start guide
- Configuration options
- Advanced usage
- Troubleshooting
- Implementation details

---

### 4. Examples README
**Location**: `examples/README.md`

**Contents**:
- Overview of all examples
- Quick start instructions
- Troubleshooting guide
- Customization tips

---

## Quick Test

### 1. Run the example (interactive):
```bash
cd c:\Users\Takshay\Desktop\Coding\Pathway\RAG\FinRAG\examples
python metadata_clustering_example.py
```

### 2. Run the tests (automated):
```bash
cd c:\Users\Takshay\Desktop\Coding\Pathway\RAG\FinRAG\tests
python test_metadata_clustering.py
```

## What You'll See

### Example Output Preview:
```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    FinRAG METADATA CLUSTERING EXAMPLES                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

METADATA EXTRACTION DEMONSTRATION
================================================================================

Document 1:
Preview: JPMorgan Chase & Co. 2023 Annual Report - Finance Sector...

Extracted Metadata:
  - Sector: finance
  - Company: JPMorgan Chase & Co.
  - Year: 2023

Created 3 chunks, each with metadata:
  Sample chunk metadata: {'sector': 'finance', 'company': 'JPMorgan Chase & Co.', 'year': '2023'}
```

### Test Output Preview:
```
test_extract_year (__main__.TestMetadataExtraction) ... ok
test_extract_company_inc (__main__.TestMetadataExtraction) ... ok
test_extract_company_corp (__main__.TestMetadataExtraction) ... ok
test_extract_sector_finance (__main__.TestMetadataExtraction) ... ok
test_extract_sector_technology (__main__.TestMetadataExtraction) ... ok
...

----------------------------------------------------------------------
Ran 20 tests in 0.234s

OK
```

## Code Examples

### Basic Usage:
```python
from finrag import FinRAG

# Metadata clustering enabled by default
finrag = FinRAG()

# Add financial documents
documents = [
    "JPMorgan Chase & Co. 2023 Annual Report - Finance Sector..."
]

finrag.add_documents(documents)
result = finrag.query("What were JPMorgan's 2023 earnings?")
```

### Custom Configuration:
```python
from finrag.config import FinRAGConfig

config = FinRAGConfig()
config.use_metadata_clustering = True
config.metadata_keys = ["sector", "year"]  # Only sector and year

finrag = FinRAG(config=config)
```

### Disable Metadata Clustering:
```python
config = FinRAGConfig()
config.use_metadata_clustering = False

finrag = FinRAG(config=config)  # Uses standard clustering
```

## Sample Documents Included

The example file includes 6 realistic financial documents:

1. **JPMorgan Chase 2023 Annual Report** (Finance)
2. **JPMorgan Chase 2023 Q4 Earnings** (Finance)
3. **Apple Inc. 2023 Annual Report** (Technology)
4. **Apple Inc. 2023 Innovation Report** (Technology)
5. **Goldman Sachs 2023 Annual Report** (Finance)
6. **Tesla Inc. 2023 Annual Report** (Technology/Manufacturing)

Each document contains realistic financial data to demonstrate metadata extraction.

## Next Steps

1. ✅ **Run the example**: See metadata clustering in action
2. ✅ **Run the tests**: Verify everything works
3. ✅ **Read the docs**: Understand implementation details
4. ✅ **Try your own data**: Use your financial documents

## Troubleshooting

**No metadata extracted?**
- Check document format includes sector keywords
- Include company suffix (Inc, Corp, Ltd)
- Use 4-digit years (2023, not '23)

**Import errors?**
- Run `pip install -e .` from project root
- Ensure .env file has OPENAI_API_KEY

**Tests failing?**
- Check API key is set
- Ensure all dependencies installed
- Run `pip install -r requirements.txt`
