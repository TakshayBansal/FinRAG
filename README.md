# FinRAG - Financial Retrieval-Augmented Generation# FinRAG: Financial Retrieval-Augmented Generation



A powerful Financial RAG system based on the RAPTOR (Recursive Abstractive Processing for Tree-Organized Retrieval) architecture, optimized for financial documents and analysis.A sophisticated implementation of Retrieval-Augmented Generation (RAG) for financial documents, built on top of RAPTOR's hierarchical tree structure for improved context retrieval and question answering.



## 📁 Project Structure## Overview



```FinRAG combines the power of RAPTOR (Recursive Abstractive Processing for Tree-Organized Retrieval) with financial domain-specific optimizations to create a state-of-the-art system for querying financial documents.

FinRAG/

├── src/finrag/              # Source code (organized by functionality)### Key Features

├── examples/                # Ready-to-run examples

├── tests/                   # Testing scripts- **Hierarchical Tree Structure**: Uses RAPTOR's recursive clustering to build multi-level document representations

├── docs/                    # Comprehensive documentation- **Advanced PDF Parsing**: Integrated LlamaParse for superior table/layout extraction (with PyPDF2 fallback)

├── scripts/                 # Utility scripts- **Financial Context Awareness**: Specialized chunking and summarization for financial documents

├── data/                    # Data files and samples- **Multiple Retrieval Strategies**: 

└── requirements.txt         # Python dependencies  - Tree Traversal: Navigate from high-level summaries to detailed information

```  - Collapsed Tree: Search across all abstraction levels simultaneously

- **Semantic Search**: Leverages OpenAI embeddings for accurate document retrieval

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed organization.- **Extensible Architecture**: Easy to swap models (embeddings, LLMs, summarization)



## 🚀 Quick Start## Architecture



### 1. Install Dependencies```

FinRAG Architecture:

```powershell┌─────────────────────────────────────────────────────────────┐

pip install -r requirements.txt│                    Financial Documents                       │

```└───────────────────────┬─────────────────────────────────────┘

                        │

Or install as a package:                        ▼

┌─────────────────────────────────────────────────────────────┐

```powershell│                  Document Chunking                           │

pip install -e .│              (Financial-aware chunking)                      │

```└───────────────────────┬─────────────────────────────────────┘

                        │

### 2. Configure API Keys                        ▼

┌─────────────────────────────────────────────────────────────┐

```powershell│                  Embedding Generation                        │

# Copy the template│              (OpenAI text-embedding-3-small)                 │

Copy-Item .env.example .env└───────────────────────┬─────────────────────────────────────┘

                        │

# Edit .env and add your keys                        ▼

notepad .env┌─────────────────────────────────────────────────────────────┐

```│                   RAPTOR Tree Building                       │

│  ┌─────────────────────────────────────────────────────┐   │

Add your API keys to `.env`:│  │         Level 2: High-level summaries               │   │

```bash│  │                     /  |  \                          │   │

OPENAI_API_KEY=sk-your-key-here│  │         Level 1: Mid-level summaries                │   │

LLAMA_CLOUD_API_KEY=llx-your-key-here  # Optional but recommended│  │                 /   |   |   \                        │   │

```│  │         Level 0: Original chunks                    │   │

│  └─────────────────────────────────────────────────────┘   │

### 3. Run Examples└───────────────────────┬─────────────────────────────────────┘

                        │

```powershell                        ▼

# Simple example with sample data┌─────────────────────────────────────────────────────────────┐

python examples/example.py│              Query Processing & Retrieval                    │

│  • Tree Traversal: Top-down navigation                      │

# Full PDF example│  • Collapsed Tree: Cross-level search                       │

python examples/main.py└───────────────────────┬─────────────────────────────────────┘

                        │

# Interactive CLI                        ▼

python examples/cli.py┌─────────────────────────────────────────────────────────────┐

```│                Question Answering                            │

│              (GPT-4 with retrieved context)                  │

## 📚 Documentation└─────────────────────────────────────────────────────────────┘

```

Comprehensive documentation is available in the [`docs/`](docs/) folder:

## Installation

- **[README.md](docs/README.md)** - Complete system documentation

- **[GETTING_STARTED.md](docs/GETTING_STARTED.md)** - Quick start guide### Prerequisites

- **[IMPLEMENTATION.md](docs/IMPLEMENTATION.md)** - Technical implementation details

- **[SETUP.md](docs/SETUP.md)** - Detailed setup instructions- Python 3.8 or higher

- **[ENV_SETUP.md](docs/ENV_SETUP.md)** - Environment variables guide- OpenAI API key

- **[QUICKREF.md](docs/QUICKREF.md)** - Quick reference guide

- **[LLAMAPARSE.md](docs/LLAMAPARSE.md)** - LlamaParse integration guide### Setup



## 🏗️ Architecture1. Clone or download this repository:

```bash

FinRAG uses a hierarchical tree structure (RAPTOR) to organize and retrieve information:cd FinRAG

```

```

Level 2: High-level summaries (Root)2. Install dependencies:

         ↓```bash

Level 1: Mid-level summaries (Clusters)pip install -r requirements.txt

         ↓```

Level 0: Original chunks (Leaves)

```3. Set your OpenAI API key:



### Key Components**Option 1: Environment Variable**

```bash

- **Core** (`src/finrag/core/`)# Windows PowerShell

  - `base_models.py` - Abstract base classes$env:OPENAI_API_KEY="your-api-key-here"

  - `clustering.py` - RAPTOR clustering algorithm$env:LLAMA_CLOUD_API_KEY="your-llama-key-here"  # Optional but recommended

  - `tree.py` - Hierarchical tree structure

  - `retrieval.py` - Tree traversal and retrieval# Linux/Mac

export OPENAI_API_KEY="your-api-key-here"

- **Models** (`src/finrag/models/`)export LLAMA_CLOUD_API_KEY="your-llama-key-here"  # Optional but recommended

  - `models.py` - OpenAI implementations (embeddings, QA, summarization)```



- **Utils** (`src/finrag/utils/`)**Option 2: In Code**

  - `env_loader.py` - Environment variable management```python

  - `utils.py` - General utilitiesfrom config import FinRAGConfig



## 💻 Usage Examplesconfig = FinRAGConfig(

    openai_api_key="your-api-key-here",

### Basic Usage    llamaparse_api_key="your-llama-key-here"  # Optional but recommended

)

```python```

from finrag import FinRAG, FinRAGConfig

**Note**: LlamaParse API key is optional but **highly recommended** for financial documents with tables and complex layouts. See [LLAMAPARSE.md](LLAMAPARSE.md) for details.

# Initialize (automatically loads from .env)

config = FinRAGConfig()## Quick Start

finrag = FinRAG(config)

### Basic Usage

# Add documents

documents = ["Your financial text here..."]```python

finrag.add_documents(documents)import os

from config import FinRAGConfig

# Queryfrom finrag import FinRAG

result = finrag.query("What is the revenue trend?")

print(result['answer'])# Initialize FinRAG

```config = FinRAGConfig(

    openai_api_key=os.getenv("OPENAI_API_KEY"),

### With PDF    chunk_size=512,

    top_k=10,

```python    tree_depth=3

# Load PDF)

finrag.load_pdf("path/to/financial_report.pdf")

finrag = FinRAG(config)

# Query

result = finrag.query("What are the key financial metrics?")# Load a financial document

```text = finrag.load_pdf("financial_report.pdf")



### Custom Configuration# Build the RAPTOR tree

finrag.add_documents([text])

```python

config = FinRAGConfig(# Query the system

    chunk_size=1024,result = finrag.query("What is the revenue growth rate?")

    top_k=20,print(result['answer'])

    tree_depth=4,```

    summarization_model="gpt-4-turbo-preview"

)### Running the Demo

finrag = FinRAG(config)

``````bash

python main.py

## 🔧 Configuration```



Configure via `.env` file or environment variables:This will:

1. Load the included PDF document

```bash2. Build a RAPTOR tree structure

# Required3. Run example queries

OPENAI_API_KEY=sk-...4. Save and reload the system



# Recommended## Detailed Usage

LLAMA_CLOUD_API_KEY=llx-...

### Configuration

# Optional customization

FINRAG_CHUNK_SIZE=512Customize FinRAG behavior through `FinRAGConfig`:

FINRAG_TOP_K=10

FINRAG_TREE_DEPTH=3```python

FINRAG_SUMMARIZATION_MODEL=gpt-3.5-turboconfig = FinRAGConfig(

```    # API Configuration

    openai_api_key="your-key",

See [docs/ENV_SETUP.md](docs/ENV_SETUP.md) for all available options.    

    # Model Selection

## 🧪 Testing    embedding_model="text-embedding-3-small",

    llm_model="gpt-4-turbo-preview",

```powershell    summarization_model="gpt-4-turbo-preview",

# Test installation    

python tests/test_installation.py    # Chunking Parameters

    chunk_size=512,           # Tokens per chunk

# Test API keys    chunk_overlap=50,         # Overlap between chunks

python tests/test_openai_key.py    

```    # Tree Parameters

    tree_depth=3,             # Maximum tree depth

## 📦 Package Installation    max_cluster_size=100,     # Maximum nodes per cluster

    min_cluster_size=5,       # Minimum nodes per cluster

Install as a package for use in other projects:    

    # Retrieval Parameters

```powershell    top_k=10,                 # Number of documents to retrieve

# Development mode (editable)    similarity_threshold=0.7, # Minimum similarity score

pip install -e .    traversal_method="tree_traversal"  # or "collapsed_tree"

)

# Production mode```

pip install .

```### Loading Documents



Then import anywhere:**From PDF:**

```python

```pythontext = finrag.load_pdf("report.pdf")

from finrag import FinRAG, FinRAGConfigfinrag.add_documents([text])

``````



## 🔑 Features**From Text File:**

```python

- ✅ **Hierarchical RAG** - Multi-level document representation with RAPTORtext = finrag.load_text("document.txt")

- ✅ **Financial Focus** - Optimized for financial documents and analysisfinrag.add_documents([text])

- ✅ **LlamaParse Integration** - Advanced PDF parsing with table preservation```

- ✅ **Flexible Configuration** - Easy customization via .env or code

- ✅ **Multiple Retrieval Strategies** - Tree traversal and collapsed tree search**Multiple Documents:**

- ✅ **Caching** - Save and load processed indices```python

- ✅ **Progress Indicators** - Real-time feedback during processingdocs = [

- ✅ **Production Ready** - Proper error handling and validation    finrag.load_pdf("q1_report.pdf"),

    finrag.load_pdf("q2_report.pdf"),

## 🛠️ Development    finrag.load_text("analysis.txt")

]

### Project Structure Philosophyfinrag.add_documents(docs)

```

- **`src/finrag/`** - All source code organized by functionality

- **`examples/`** - Self-contained example scripts### Querying

- **`tests/`** - Testing and validation

- **`docs/`** - Comprehensive documentation**Basic Query:**

- **`scripts/`** - Setup and utility scripts```python

result = finrag.query("What are the key financial metrics?")

### Adding New Featuresprint(result['answer'])

```

1. Add core logic to `src/finrag/core/`

2. Add model implementations to `src/finrag/models/`**Custom Retrieval:**

3. Add utilities to `src/finrag/utils/````python

4. Update `__init__.py` files for exportsresult = finrag.query(

5. Add examples to `examples/`    question="What is the profit margin?",

6. Update documentation in `docs/`    retrieval_method="collapsed_tree",

    top_k=15

## 📄 License)

```

MIT License - See LICENSE file for details

**Access Retrieved Documents:**

## 🤝 Contributing```python

result = finrag.query("What are the risk factors?")

Contributions welcome! Please:

print(f"Answer: {result['answer']}")

1. Fork the repositoryprint(f"\nRetrieved {len(result['retrieved_nodes'])} nodes:")

2. Create a feature branch

3. Make your changesfor i, node in enumerate(result['retrieved_nodes'][:5], 1):

4. Add tests if applicable    print(f"{i}. Level {node['level']} (Score: {node['score']:.3f})")

5. Update documentation    print(f"   {node['text_preview']}\n")

6. Submit a pull request```



## 📞 Support### Saving and Loading



- **Documentation**: See `docs/` folder**Save the System:**

- **Issues**: Report on GitHub Issues```python

- **Questions**: Check `docs/QUICKREF.md` for quick answersfinrag.save("./my_finrag_index")

```

## 🙏 Acknowledgments

**Load a Saved System:**

- Based on [RAPTOR](https://github.com/parthsarthi03/raptor) architecture```python

- Uses OpenAI API for embeddings and language modelsfinrag_new = FinRAG(config)

- LlamaParse for advanced PDF parsingfinrag_new.load("./my_finrag_index")



---# Now you can query without rebuilding

result = finrag_new.query("Summary of financial performance")

**Happy Financial Analysis! 🚀📊**```


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
