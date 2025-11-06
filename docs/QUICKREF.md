# FinRAG Quick Reference

## Installation
```bash
pip install -r requirements.txt
$env:OPENAI_API_KEY="your-key"  # Windows PowerShell
```

## Basic Usage
```python
from finrag import FinRAG
from config import FinRAGConfig

# Initialize
config = FinRAGConfig(openai_api_key="your-key")
finrag = FinRAG(config)

# Add documents
text = finrag.load_pdf("report.pdf")
finrag.add_documents([text])

# Query
result = finrag.query("What is the revenue?")
print(result['answer'])
```

## Configuration Options
```python
config = FinRAGConfig(
    openai_api_key="key",
    chunk_size=512,          # Tokens per chunk
    chunk_overlap=50,        # Overlap between chunks
    top_k=10,               # Documents to retrieve
    tree_depth=3,           # Tree levels
    traversal_method="tree_traversal"  # or "collapsed_tree"
)
```

## Main Commands

### Load Documents
```python
# PDF
text = finrag.load_pdf("file.pdf")

# Text
text = finrag.load_text("file.txt")

# Multiple
finrag.add_documents([text1, text2, text3])
```

### Query
```python
# Basic
result = finrag.query("question")

# Advanced
result = finrag.query(
    question="question",
    retrieval_method="collapsed_tree",
    top_k=15
)
```

### Save/Load
```python
# Save
finrag.save("./index")

# Load
finrag.load("./index")
```

### Statistics
```python
stats = finrag.get_statistics()
print(stats)
```

## CLI Usage
```bash
python cli.py
```

## Retrieval Methods

### Tree Traversal (Default)
- Best for: Broad, high-level questions
- Example: "What are the main highlights?"

### Collapsed Tree
- Best for: Specific, detailed questions  
- Example: "What was the exact revenue in Q3?"

## Result Structure
```python
result = {
    'answer': "The answer text...",
    'context': "Retrieved context...",
    'question': "Original question",
    'retrieved_nodes': [
        {
            'node_id': 'level_1_cluster_0',
            'level': 1,
            'score': 0.95,
            'text_preview': "Preview..."
        },
        ...
    ],
    'retrieval_method': 'tree_traversal'
}
```

## Common Patterns

### Single Document Analysis
```python
finrag = FinRAG(config)
text = finrag.load_pdf("report.pdf")
finrag.add_documents([text])
result = finrag.query("Summarize key points")
```

### Multi-Document Comparison
```python
docs = [
    finrag.load_pdf("2023_report.pdf"),
    finrag.load_pdf("2024_report.pdf")
]
finrag.add_documents(docs)
result = finrag.query("Compare 2023 vs 2024 performance")
```

### Persistent Index
```python
# First time
finrag.add_documents(docs)
finrag.save("./index")

# Later sessions
finrag.load("./index")
result = finrag.query("question")
```

## Troubleshooting

### Out of Memory
Reduce chunk_size and max_cluster_size:
```python
config = FinRAGConfig(
    chunk_size=256,
    max_cluster_size=50
)
```

### Slow Performance
Reduce top_k:
```python
result = finrag.query(question, top_k=5)
```

### Poor Answers
Increase top_k or try different retrieval method:
```python
result = finrag.query(
    question,
    retrieval_method="collapsed_tree",
    top_k=20
)
```

## Key Files

- `finrag.py` - Main API
- `config.py` - Configuration
- `example.py` - Quick example
- `cli.py` - Interactive mode
- `README.md` - Full docs

## Examples

### Run Built-in Examples
```bash
python example.py      # Sample data
python main.py         # With your PDF
python cli.py          # Interactive
```

## API Reference

### FinRAG Class
```python
finrag = FinRAG(config)
finrag.load_pdf(path) -> str
finrag.load_text(path) -> str
finrag.add_documents(docs: List[str])
finrag.query(question, retrieval_method, top_k) -> dict
finrag.save(path)
finrag.load(path)
finrag.get_statistics() -> dict
```

### Config Class
```python
config = FinRAGConfig(
    openai_api_key: str,
    embedding_model: str = "text-embedding-3-small",
    llm_model: str = "gpt-4-turbo-preview",
    chunk_size: int = 512,
    top_k: int = 10,
    tree_depth: int = 3,
    ...
)
```

## Performance Tips

1. **Chunk Size**: 256-512 for precise, 512-1024 for broad
2. **Tree Depth**: 2-3 normal, 4+ for large docs
3. **Top-K**: 5-10 focused, 15-20 comprehensive
4. **Method**: tree_traversal for summaries, collapsed_tree for details

## Support

- README.md - Full documentation
- IMPLEMENTATION.md - Architecture details
- SETUP.md - Installation guide
- RAPTOR paper: https://arxiv.org/abs/2401.18059
