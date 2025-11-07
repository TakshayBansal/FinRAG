# Metadata Clustering in FinRAG

## Overview

FinRAG implements a two-stage clustering approach from the original FinRAG paper that leverages document metadata to improve retrieval quality for financial documents.

## How It Works

### Two-Stage Clustering Process

```
Stage 1: Metadata Grouping
├─ Extract metadata (sector, company, year)
├─ Group documents by metadata tuples
└─ Example: All "JPMorgan/Finance/2023" docs together

Stage 2: Embedding-Based Sub-Clustering
├─ Within each metadata group
├─ Perform UMAP + GMM clustering
└─ Create semantic sub-groups
```

### Benefits

1. **Better Organization**: Documents are first grouped by business context
2. **Improved Retrieval**: Similar business entities are clustered together
3. **Hierarchical Structure**: Maintains semantic relationships within business groups
4. **Financial Focus**: Optimized for financial documents with sector/company/year info

## Quick Start

### Basic Usage

```python
from finrag import FinRAG

# Initialize (metadata clustering enabled by default)
finrag = FinRAG()

# Add financial documents
documents = [
    """
    JPMorgan Chase & Co. 2023 Annual Report - Finance Sector
    Total revenue for 2023 reached $158.1 billion...
    """,
    """
    Apple Inc. 2023 Annual Report - Technology Sector
    Net sales: $383.3 billion...
    """
]

finrag.add_documents(documents)

# Query
result = finrag.query("What were JPMorgan's 2023 earnings?")
print(result['answer'])
```

### Configuration

```python
from finrag import FinRAG
from finrag.config import FinRAGConfig

# Customize metadata clustering
config = FinRAGConfig()
config.use_metadata_clustering = True  # Enable/disable
config.metadata_keys = ["sector", "company", "year"]  # Which keys to use

finrag = FinRAG(config=config)
```

## Metadata Extraction

### Automatic Extraction

The system automatically extracts metadata using pattern matching:

**Year Extraction:**
- Patterns: 4-digit years (1900-2099)
- Example: "2023 Annual Report" → `year: "2023"`

**Company Extraction:**
- Patterns: Company suffixes (Inc, Corp, Ltd, LLC, Co., Group, etc.)
- Example: "JPMorgan Chase & Co." → `company: "JPMorgan Chase & Co."`

**Sector Extraction:**
- Keywords: technology, finance, healthcare, energy, retail, manufacturing, real estate, telecom
- Example: "Technology Sector" → `sector: "technology"`

### Example Document Format

For best results, include metadata in your documents:

```text
[Company Name] [Year] Annual Report - [Sector]

Example:
Apple Inc. 2023 Annual Report - Technology Sector
...content...
```

## Advanced Usage

### Custom Metadata Keys

```python
# Group by sector and year only (ignore company)
config = FinRAGConfig()
config.metadata_keys = ["sector", "year"]

# Group by company only
config.metadata_keys = ["company"]

# All three (default)
config.metadata_keys = ["sector", "company", "year"]
```

### Disable Metadata Clustering

```python
# Use standard clustering without metadata
config = FinRAGConfig()
config.use_metadata_clustering = False

finrag = FinRAG(config=config)
```

## Clustering Parameters

### Metadata Clustering Threshold

```python
# In clustering.py
METADATA_THRESHOLD = 3  # Min nodes per group to sub-cluster
```

If a metadata group has fewer than 3 nodes, they're kept together without sub-clustering.

### Standard Clustering Parameters

```python
config = FinRAGConfig()
config.reduction_dimension = 10  # UMAP dimension
config.max_clusters = 5          # Max clusters per level
config.gaussian_random_state = 42 # Random seed
```

## Examples

### Full Example

See `examples/metadata_clustering_example.py` for comprehensive examples:

```bash
cd examples
python metadata_clustering_example.py
```

This demonstrates:
- Basic metadata clustering
- Metadata extraction
- Clustering comparison (with vs without metadata)
- Custom metadata keys
- Tree structure visualization

### Run Tests

```bash
cd tests
python test_metadata_clustering.py
```

## How Metadata Affects the Tree

### Without Metadata Clustering

```
Level 0: [Doc1, Doc2, Doc3, Doc4, ...]
         ↓
         UMAP + GMM clustering
         ↓
Level 1: [Cluster1, Cluster2, Cluster3, ...]
```

### With Metadata Clustering

```
Level 0: [JPM-2023-1, JPM-2023-2, AAPL-2023-1, AAPL-2023-2, ...]
         ↓
         Group by metadata
         ↓
         JPMorgan/Finance/2023: [JPM-2023-1, JPM-2023-2]
         Apple/Technology/2023: [AAPL-2023-1, AAPL-2023-2]
         ↓
         UMAP + GMM within each group
         ↓
Level 1: [JPM-Cluster1, JPM-Cluster2, AAPL-Cluster1, ...]
```

## Metadata Structure

### ClusterNode Metadata

```python
{
    "sector": "finance",       # Sector classification
    "company": "JPMorgan",     # Company name
    "year": "2023"             # Document year
}
```

### Chunk Metadata

```python
{
    "text": "JPMorgan Chase revenue...",
    "metadata": {
        "sector": "finance",
        "company": "JPMorgan Chase & Co.",
        "year": "2023"
    }
}
```

## Best Practices

### 1. Document Formatting

Include clear metadata in document headers:
```text
[Company] [Year] [Document Type] - [Sector]
```

### 2. Consistent Naming

Use consistent company names across documents:
- ✅ "Apple Inc."
- ❌ "Apple", "Apple Inc", "Apple Incorporated"

### 3. Sector Keywords

Use standard sector keywords:
- technology
- finance
- healthcare
- energy
- retail
- manufacturing
- real estate
- telecom

### 4. Year Format

Use 4-digit years (1900-2099):
- ✅ "2023"
- ❌ "23", "'23"

## Troubleshooting

### Metadata Not Extracted

**Problem**: Documents don't have metadata after extraction.

**Solution**: 
- Check document format includes sector/company/year
- Use keywords from the predefined sector list
- Include company suffix (Inc, Corp, Ltd, etc.)

### Too Many Small Clusters

**Problem**: Many metadata groups with 1-2 nodes each.

**Solution**:
```python
# Use fewer metadata keys
config.metadata_keys = ["sector"]  # Group by sector only
```

### Poor Retrieval Quality

**Problem**: Metadata clustering doesn't improve retrieval.

**Solution**:
- Ensure documents have accurate metadata
- Try standard clustering for comparison
- Adjust clustering parameters

## Implementation Details

### File Structure

```
src/finrag/
├── core/
│   ├── clustering.py       # Metadata clustering logic
│   └── tree.py            # Integration with RAPTOR tree
├── models/
│   └── models.py          # Metadata extraction (FinancialChunker)
├── config.py              # Metadata configuration
└── finrag.py              # Main API
```

### Key Methods

**Metadata Extraction:**
```python
# In models.py
chunker.extract_metadata(text) → dict
chunker.chunk_text_with_metadata(text) → List[dict]
```

**Metadata Clustering:**
```python
# In clustering.py
clustering.extract_metadata_groups(nodes) → dict
clustering.perform_metadata_clustering(nodes, embeddings) → List
clustering.perform_clustering_with_nodes(nodes, embeddings) → List
```

## Performance Considerations

### Memory Usage

Metadata clustering adds minimal memory overhead:
- Each node stores a small metadata dict (~100 bytes)
- Grouping operation is O(n)

### Speed

Metadata clustering can be faster for large datasets:
- Groups documents before embedding clustering
- Smaller sub-clusters process faster
- Overall: Similar or better performance

### Scalability

Works well with:
- ✅ 100s of documents per metadata group
- ✅ 10-20 unique metadata groups
- ⚠️ May need tuning for 1000s of unique groups

## References

- **FinRAG Paper**: Metadata-aware clustering for financial documents
- **RAPTOR**: Recursive Abstractive Processing for Tree-Organized Retrieval
- **UMAP**: Uniform Manifold Approximation and Projection
- **GMM**: Gaussian Mixture Models

## Support

For issues or questions:
1. Check the examples: `examples/metadata_clustering_example.py`
2. Run the tests: `tests/test_metadata_clustering.py`
3. Review this guide
4. Open an issue on GitHub

## License

Same as FinRAG project license.
