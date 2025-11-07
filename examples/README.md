# FinRAG Examples

This directory contains example scripts demonstrating various features of FinRAG.

## Available Examples

### 1. Basic Usage (`example.py`)
Basic example showing how to use FinRAG for question answering.

```bash
python example.py
```

### 2. Metadata Clustering (`metadata_clustering_example.py`) ⭐ NEW
Comprehensive demonstration of metadata clustering features.

```bash
python metadata_clustering_example.py
```

**What it covers:**
- ✅ Metadata extraction from financial documents
- ✅ Basic metadata clustering workflow
- ✅ Comparison: with vs without metadata clustering
- ✅ Custom metadata keys configuration
- ✅ Tree structure visualization

**Sample financial documents included:**
- JPMorgan Chase 2023 Annual Reports (Finance Sector)
- Apple Inc. 2023 Annual Reports (Technology Sector)
- Goldman Sachs 2023 Reports (Finance Sector)
- Tesla 2023 Reports (Technology/Manufacturing)
- Microsoft 2022 Reports (Technology Sector)

### 3. Command Line Interface (`cli.py`)
Interactive CLI for querying documents.

```bash
python cli.py
```

### 4. Main Example (`main.py`)
Complete workflow example.

```bash
python main.py
```

## Quick Start

### Prerequisites

1. Install FinRAG package:
```bash
cd ..
pip install -e .
```

2. Set up environment variables:
```bash
# Create .env file in project root
echo OPENAI_API_KEY=your_api_key_here > ../.env
```

### Running Examples

```bash
# Run metadata clustering example (recommended first)
python metadata_clustering_example.py

# Run basic example
python example.py

# Run CLI
python cli.py
```

## Example Output

### Metadata Clustering Example

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    FinRAG METADATA CLUSTERING EXAMPLES                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

METADATA EXTRACTION DEMONSTRATION
================================================================================

Testing metadata extraction on sample documents...

Document 1:
Preview: JPMorgan Chase & Co. 2023 Annual Report - Finance Sector...

Extracted Metadata:
  - Sector: finance
  - Company: JPMorgan Chase & Co.
  - Year: 2023

Created 3 chunks, each with metadata:
  Sample chunk metadata: {'sector': 'finance', 'company': 'JPMorgan Chase & Co.', 'year': '2023'}

...
```

## Customization

### Using Your Own Documents

```python
# In any example file, replace SAMPLE_DOCUMENTS with your own:
from finrag import FinRAG

documents = [
    # Your financial documents here
    "Your Company Inc. 2023 Annual Report - Finance Sector...",
]

finrag = FinRAG()
finrag.add_documents(documents)
result = finrag.query("Your question here")
```

### Adjusting Configuration

```python
from finrag.config import FinRAGConfig

config = FinRAGConfig()
config.use_metadata_clustering = True
config.metadata_keys = ["sector", "company", "year"]
config.top_k = 10
config.reduction_dimension = 10

finrag = FinRAG(config=config)
```

## Troubleshooting

### API Key Issues
```
Error: OpenAI API key not found
```
**Solution**: Create `.env` file in project root with `OPENAI_API_KEY=your_key`

### Import Errors
```
ModuleNotFoundError: No module named 'finrag'
```
**Solution**: Install package with `pip install -e .` from project root

### No Metadata Extracted
```
Extracted Metadata:
  - Sector: Not found
  - Company: Not found
  - Year: Not found
```
**Solution**: Ensure documents include sector keywords, company names with suffixes (Inc/Corp/Ltd), and 4-digit years

## Next Steps

1. **Learn More**: Read `docs/METADATA_CLUSTERING.md` for detailed documentation
2. **Run Tests**: Try `tests/test_metadata_clustering.py` to validate installation
3. **Build Your Own**: Use examples as templates for your use case

## Support

- Documentation: `../docs/`
- Tests: `../tests/`
- Main README: `../README.md`
