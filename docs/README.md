# FinRAG: Financial Retrieval-Augmented Generation

A sophisticated implementation of Retrieval-Augmented Generation (RAG) for financial documents, built on top of RAPTOR's hierarchical tree structure for improved context retrieval and question answering.

## Overview

FinRAG combines the power of RAPTOR (Recursive Abstractive Processing for Tree-Organized Retrieval) with financial domain-specific optimizations to create a state-of-the-art system for querying financial documents.

### Key Features

- **Hierarchical Tree Structure**: Uses RAPTOR's recursive clustering to build multi-level document representations
- **Advanced PDF Parsing**: Integrated LlamaParse for superior table/layout extraction (with PyPDF2 fallback)
- **Financial Context Awareness**: Specialized chunking and summarization for financial documents
- **Multiple Retrieval Strategies**: 
  - Tree Traversal: Navigate from high-level summaries to detailed information
  - Collapsed Tree: Search across all abstraction levels simultaneously
- **Semantic Search**: Leverages OpenAI embeddings for accurate document retrieval
- **Extensible Architecture**: Easy to swap models (embeddings, LLMs, summarization)

## Architecture

```
FinRAG Architecture:
┌─────────────────────────────────────────────────────────────┐
│                    Financial Documents                       │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  Document Chunking                           │
│              (Financial-aware chunking)                      │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  Embedding Generation                        │
│              (OpenAI text-embedding-3-small)                 │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   RAPTOR Tree Building                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         Level 2: High-level summaries               │   │
│  │                     /  |  \                          │   │
│  │         Level 1: Mid-level summaries                │   │
│  │                 /   |   |   \                        │   │
│  │         Level 0: Original chunks                    │   │
│  └─────────────────────────────────────────────────────┘   │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              Query Processing & Retrieval                    │
│  • Tree Traversal: Top-down navigation                      │
│  • Collapsed Tree: Cross-level search                       │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                Question Answering                            │
│              (GPT-4 with retrieved context)                  │
└─────────────────────────────────────────────────────────────┘
```

## Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Setup

1. Clone or download this repository:
```bash
cd FinRAG
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set your OpenAI API key:

**Option 1: Environment Variable**
```bash
# Windows PowerShell
$env:OPENAI_API_KEY="your-api-key-here"
$env:LLAMA_CLOUD_API_KEY="your-llama-key-here"  # Optional but recommended

# Linux/Mac
export OPENAI_API_KEY="your-api-key-here"
export LLAMA_CLOUD_API_KEY="your-llama-key-here"  # Optional but recommended
```

**Option 2: In Code**
```python
from config import FinRAGConfig

config = FinRAGConfig(
    openai_api_key="your-api-key-here",
    llamaparse_api_key="your-llama-key-here"  # Optional but recommended
)
```

**Note**: LlamaParse API key is optional but **highly recommended** for financial documents with tables and complex layouts. See [LLAMAPARSE.md](LLAMAPARSE.md) for details.

## Quick Start

### Basic Usage

```python
import os
from config import FinRAGConfig
from finrag import FinRAG

# Initialize FinRAG
config = FinRAGConfig(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    chunk_size=512,
    top_k=10,
    tree_depth=3
)

finrag = FinRAG(config)

# Load a financial document
text = finrag.load_pdf("financial_report.pdf")

# Build the RAPTOR tree
finrag.add_documents([text])

# Query the system
result = finrag.query("What is the revenue growth rate?")
print(result['answer'])
```

### Running the Demo

```bash
python main.py
```

This will:
1. Load the included PDF document
2. Build a RAPTOR tree structure
3. Run example queries
4. Save and reload the system

## Detailed Usage

### Configuration

Customize FinRAG behavior through `FinRAGConfig`:

```python
config = FinRAGConfig(
    # API Configuration
    openai_api_key="your-key",
    
    # Model Selection
    embedding_model="text-embedding-3-small",
    llm_model="gpt-4-turbo-preview",
    summarization_model="gpt-4-turbo-preview",
    
    # Chunking Parameters
    chunk_size=512,           # Tokens per chunk
    chunk_overlap=50,         # Overlap between chunks
    
    # Tree Parameters
    tree_depth=3,             # Maximum tree depth
    max_cluster_size=100,     # Maximum nodes per cluster
    min_cluster_size=5,       # Minimum nodes per cluster
    
    # Retrieval Parameters
    top_k=10,                 # Number of documents to retrieve
    similarity_threshold=0.7, # Minimum similarity score
    traversal_method="tree_traversal"  # or "collapsed_tree"
)
```

### Loading Documents

**From PDF:**
```python
text = finrag.load_pdf("report.pdf")
finrag.add_documents([text])
```

**From Text File:**
```python
text = finrag.load_text("document.txt")
finrag.add_documents([text])
```

**Multiple Documents:**
```python
docs = [
    finrag.load_pdf("q1_report.pdf"),
    finrag.load_pdf("q2_report.pdf"),
    finrag.load_text("analysis.txt")
]
finrag.add_documents(docs)
```

### Querying

**Basic Query:**
```python
result = finrag.query("What are the key financial metrics?")
print(result['answer'])
```

**Custom Retrieval:**
```python
result = finrag.query(
    question="What is the profit margin?",
    retrieval_method="collapsed_tree",
    top_k=15
)
```

**Access Retrieved Documents:**
```python
result = finrag.query("What are the risk factors?")

print(f"Answer: {result['answer']}")
print(f"\nRetrieved {len(result['retrieved_nodes'])} nodes:")

for i, node in enumerate(result['retrieved_nodes'][:5], 1):
    print(f"{i}. Level {node['level']} (Score: {node['score']:.3f})")
    print(f"   {node['text_preview']}\n")
```

### Saving and Loading

**Save the System:**
```python
finrag.save("./my_finrag_index")
```

**Load a Saved System:**
```python
finrag_new = FinRAG(config)
finrag_new.load("./my_finrag_index")

# Now you can query without rebuilding
result = finrag_new.query("Summary of financial performance")
```

### Statistics

```python
stats = finrag.get_statistics()
print(f"Total nodes: {stats['total_nodes']}")
print(f"Tree depth: {stats['tree_depth']}")
print(f"Nodes per level: {stats['levels']}")
```

## Advanced Features

### Custom Models

FinRAG supports custom implementations for all components:

```python
from base_models import BaseEmbeddingModel, BaseSummarizationModel, BaseQAModel

class CustomEmbedding(BaseEmbeddingModel):
    def create_embedding(self, text):
        # Your embedding logic
        return embedding_vector

class CustomSummarizer(BaseSummarizationModel):
    def summarize(self, texts, max_tokens=200):
        # Your summarization logic
        return summary

class CustomQA(BaseQAModel):
    def answer_question(self, context, question):
        # Your QA logic
        return {"answer": answer}

# Use custom models
from tree import RAPTORTree, TreeConfig

tree = RAPTORTree(
    embedding_model=CustomEmbedding(),
    summarization_model=CustomSummarizer(),
    config=TreeConfig()
)
```

### Retrieval Methods

**Tree Traversal (Default):**
- Starts from high-level summaries
- Progressively drills down to details
- Better for broad questions

**Collapsed Tree:**
- Searches all levels simultaneously
- Better for specific, detailed queries

```python
# Tree traversal
result = finrag.query(
    "Give me an overview of the company's performance",
    retrieval_method="tree_traversal"
)

# Collapsed tree
result = finrag.query(
    "What was the exact revenue in Q3 2024?",
    retrieval_method="collapsed_tree"
)
```

## Performance Tips

1. **Chunk Size**: Smaller chunks (256-512) work better for precise queries; larger chunks (512-1024) for broader context

2. **Tree Depth**: 
   - Depth 2-3: Good for most documents
   - Depth 4+: Large document collections
   
3. **Top-K**: 
   - 5-10: Focused, specific answers
   - 15-20: Comprehensive answers with more context

4. **Caching**: Enable caching for repeated queries on the same documents

## Project Structure

```
FinRAG/
├── config.py              # Configuration settings
├── base_models.py         # Abstract base classes
├── models.py              # OpenAI model implementations
├── clustering.py          # RAPTOR clustering algorithm
├── tree.py               # RAPTOR tree structure
├── retrieval.py          # Retrieval strategies
├── finrag.py             # Main FinRAG class
├── utils.py              # Utility functions
├── main.py               # Example usage
├── requirements.txt      # Dependencies
└── README.md            # This file
```

## How It Works

### 1. Document Processing

Documents are chunked into manageable pieces with financial-aware boundaries (preserving tables, lists, etc.)

### 2. Tree Building

RAPTOR recursively:
1. Embeds all chunks
2. Clusters similar chunks using Gaussian Mixture Models
3. Summarizes each cluster
4. Repeats for multiple levels

### 3. Retrieval

When you query:
1. Query is embedded
2. Most relevant nodes are found (tree traversal or collapsed tree)
3. Context is gathered from retrieved nodes and their children

### 4. Answer Generation

Retrieved context is fed to GPT-4 to generate accurate, grounded answers

## Comparison with Standard RAG

| Feature | Standard RAG | FinRAG (RAPTOR-based) |
|---------|-------------|----------------------|
| Document Representation | Flat chunks | Hierarchical tree |
| Retrieval | Single-level | Multi-level |
| Context | Fixed-size chunks | Adaptive (summaries + details) |
| Long Documents | May miss context | Better at handling long docs |
| Performance | Good for simple queries | Better for complex queries |

## References

- **RAPTOR Paper**: [Recursive Abstractive Processing for Tree-Organized Retrieval](https://arxiv.org/abs/2401.18059)
- **RAPTOR GitHub**: [parthsarthi03/raptor](https://github.com/parthsarthi03/raptor)

## License

MIT License

## Contributing

Contributions welcome! Areas for improvement:
- Support for more embedding models (e.g., Cohere, Voyage)
- Custom financial entity extraction
- Table and chart processing
- Multi-modal document support
- Query optimization

## Troubleshooting

**Issue: Out of memory during tree building**
- Reduce `chunk_size` or `max_cluster_size`
- Process documents in batches

**Issue: Slow retrieval**
- Reduce `top_k`
- Use `collapsed_tree` method
- Enable caching

**Issue: Poor answer quality**
- Increase `top_k` for more context
- Try different `retrieval_method`
- Adjust `chunk_size` and `chunk_overlap`

## Support

For issues and questions, please refer to:
- Original RAPTOR repository: https://github.com/parthsarthi03/raptor
- OpenAI Documentation: https://platform.openai.com/docs
