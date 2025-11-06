# FinRAG - Financial Retrieval-Augmented Generation# FinRAG - Financial Retrieval-Augmented Generation# FinRAG: Financial Retrieval-Augmented Generation



[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful Financial RAG system based on the RAPTOR (Recursive Abstractive Processing for Tree-Organized Retrieval) architecture, optimized for financial documents and analysis.A sophisticated implementation of Retrieval-Augmented Generation (RAG) for financial documents, built on top of RAPTOR's hierarchical tree structure for improved context retrieval and question answering.

A sophisticated implementation of Retrieval-Augmented Generation (RAG) for financial documents, built on RAPTOR's hierarchical tree structure for improved context retrieval and question answering.



## 🌟 Overview

## 📁 Project Structure## Overview

FinRAG combines the power of RAPTOR (Recursive Abstractive Processing for Tree-Organized Retrieval) with financial domain-specific optimizations to create a state-of-the-art system for querying financial documents.



### Key Features

```FinRAG combines the power of RAPTOR (Recursive Abstractive Processing for Tree-Organized Retrieval) with financial domain-specific optimizations to create a state-of-the-art system for querying financial documents.

- 🌳 **Hierarchical Tree Structure** - Multi-level document representation using RAPTOR

- 📊 **Financial Context Awareness** - Specialized processing for financial documentsFinRAG/

- 📄 **Advanced PDF Parsing** - LlamaParse integration with PyPDF2 fallback

- 🔍 **Multiple Retrieval Strategies** - Tree traversal and collapsed tree search├── src/finrag/              # Source code (organized by functionality)### Key Features

- 🎯 **Semantic Search** - Powered by OpenAI embeddings

- ⚡ **Caching Support** - Save and load processed indices├── examples/                # Ready-to-run examples

- 🔧 **Extensible Architecture** - Easy to customize and extend

├── tests/                   # Testing scripts- **Hierarchical Tree Structure**: Uses RAPTOR's recursive clustering to build multi-level document representations

## 📁 Project Structure

├── docs/                    # Comprehensive documentation- **Advanced PDF Parsing**: Integrated LlamaParse for superior table/layout extraction (with PyPDF2 fallback)

```

FinRAG/├── scripts/                 # Utility scripts- **Financial Context Awareness**: Specialized chunking and summarization for financial documents

├── src/finrag/              # Source code

│   ├── core/               # Core algorithms├── data/                    # Data files and samples- **Multiple Retrieval Strategies**: 

│   ├── models/             # Model implementations

│   └── utils/              # Utilities└── requirements.txt         # Python dependencies  - Tree Traversal: Navigate from high-level summaries to detailed information

├── examples/               # Usage examples

├── tests/                  # Testing scripts```  - Collapsed Tree: Search across all abstraction levels simultaneously

├── docs/                   # Documentation

└── requirements.txt        # Dependencies- **Semantic Search**: Leverages OpenAI embeddings for accurate document retrieval

```

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed organization.- **Extensible Architecture**: Easy to swap models (embeddings, LLMs, summarization)

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed organization.



## 🚀 Quick Start

## 🚀 Quick Start## Architecture

### 1. Install Dependencies



```bash

pip install -r requirements.txt### 1. Install Dependencies```

```

FinRAG Architecture:

Or install as a package:

```powershell┌─────────────────────────────────────────────────────────────┐

```bash

pip install -e .pip install -r requirements.txt│                    Financial Documents                       │

```

```└───────────────────────┬─────────────────────────────────────┘

### 2. Configure API Keys

                        │

Create a `.env` file from the template:

Or install as a package:                        ▼

```bash

cp .env.example .env┌─────────────────────────────────────────────────────────────┐

```

```powershell│                  Document Chunking                           │

Add your API keys:

pip install -e .│              (Financial-aware chunking)                      │

```bash

OPENAI_API_KEY=sk-your-key-here```└───────────────────────┬─────────────────────────────────────┘

LLAMA_CLOUD_API_KEY=llx-your-key-here  # Optional but recommended

```                        │



### 3. Run Examples### 2. Configure API Keys                        ▼



```bash┌─────────────────────────────────────────────────────────────┐

# Simple example with sample data

python examples/example.py```powershell│                  Embedding Generation                        │



# Full PDF example# Copy the template│              (OpenAI text-embedding-3-small)                 │

python examples/main.py

Copy-Item .env.example .env└───────────────────────┬─────────────────────────────────────┘

# Interactive CLI

python examples/cli.py                        │

```

# Edit .env and add your keys                        ▼

## 💻 Usage

notepad .env┌─────────────────────────────────────────────────────────────┐

### Basic Usage

```│                   RAPTOR Tree Building                       │

```python

from finrag import FinRAG, FinRAGConfig│  ┌─────────────────────────────────────────────────────┐   │



# Initialize (automatically loads from .env)Add your API keys to `.env`:│  │         Level 2: High-level summaries               │   │

config = FinRAGConfig()

finrag = FinRAG(config)```bash│  │                     /  |  \                          │   │



# Add documentsOPENAI_API_KEY=sk-your-key-here│  │         Level 1: Mid-level summaries                │   │

documents = ["Your financial text here..."]

finrag.add_documents(documents)LLAMA_CLOUD_API_KEY=llx-your-key-here  # Optional but recommended│  │                 /   |   |   \                        │   │



# Query```│  │         Level 0: Original chunks                    │   │

result = finrag.query("What is the revenue trend?")

print(result['answer'])│  └─────────────────────────────────────────────────────┘   │

```

### 3. Run Examples└───────────────────────┬─────────────────────────────────────┘

### With PDF

                        │

```python

# Load PDF```powershell                        ▼

finrag.load_pdf("financial_report.pdf")

# Simple example with sample data┌─────────────────────────────────────────────────────────────┐

# Query

result = finrag.query("What are the key financial metrics?")python examples/example.py│              Query Processing & Retrieval                    │

print(result['answer'])

```│  • Tree Traversal: Top-down navigation                      │



### Custom Configuration# Full PDF example│  • Collapsed Tree: Cross-level search                       │



```pythonpython examples/main.py└───────────────────────┬─────────────────────────────────────┘

config = FinRAGConfig(

    chunk_size=1024,                        │

    top_k=20,

    tree_depth=4,# Interactive CLI                        ▼

    summarization_model="gpt-4-turbo-preview"

)python examples/cli.py┌─────────────────────────────────────────────────────────────┐

finrag = FinRAG(config)

``````│                Question Answering                            │



## 🏗️ Architecture│              (GPT-4 with retrieved context)                  │



```## 📚 Documentation└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────┐

│     Financial Documents             │```

└─────────────┬───────────────────────┘

              │Comprehensive documentation is available in the [`docs/`](docs/) folder:

              ▼

┌─────────────────────────────────────┐## Installation

│     Document Chunking               │

│  (Financial-aware chunking)         │- **[README.md](docs/README.md)** - Complete system documentation

└─────────────┬───────────────────────┘

              │- **[GETTING_STARTED.md](docs/GETTING_STARTED.md)** - Quick start guide### Prerequisites

              ▼

┌─────────────────────────────────────┐- **[IMPLEMENTATION.md](docs/IMPLEMENTATION.md)** - Technical implementation details

│     Embedding Generation            │

│  (OpenAI text-embedding-3-small)    │- **[SETUP.md](docs/SETUP.md)** - Detailed setup instructions- Python 3.8 or higher

└─────────────┬───────────────────────┘

              │- **[ENV_SETUP.md](docs/ENV_SETUP.md)** - Environment variables guide- OpenAI API key

              ▼

┌─────────────────────────────────────┐- **[QUICKREF.md](docs/QUICKREF.md)** - Quick reference guide

│     RAPTOR Tree Building            │

│  ┌─────────────────────────────┐   │- **[LLAMAPARSE.md](docs/LLAMAPARSE.md)** - LlamaParse integration guide### Setup

│  │  Level 2: High-level        │   │

│  │  Level 1: Mid-level         │   │

│  │  Level 0: Original chunks   │   │

│  └─────────────────────────────┘   │## 🏗️ Architecture1. Clone or download this repository:

└─────────────┬───────────────────────┘

              │```bash

              ▼

┌─────────────────────────────────────┐FinRAG uses a hierarchical tree structure (RAPTOR) to organize and retrieve information:cd FinRAG

│  Query Processing & Retrieval       │

│  • Tree Traversal                   │```

│  • Collapsed Tree Search            │

└─────────────┬───────────────────────┘```

              │

              ▼Level 2: High-level summaries (Root)2. Install dependencies:

┌─────────────────────────────────────┐

│     Question Answering              │         ↓```bash

│  (GPT-4 with context)               │

└─────────────────────────────────────┘Level 1: Mid-level summaries (Clusters)pip install -r requirements.txt

```

         ↓```

### Core Components

Level 0: Original chunks (Leaves)

- **Core** (`src/finrag/core/`)

  - `base_models.py` - Abstract base classes```3. Set your OpenAI API key:

  - `clustering.py` - RAPTOR clustering algorithm

  - `tree.py` - Hierarchical tree structure

  - `retrieval.py` - Tree traversal and retrieval

### Key Components**Option 1: Environment Variable**

- **Models** (`src/finrag/models/`)

  - `models.py` - OpenAI implementations```bash



- **Utils** (`src/finrag/utils/`)- **Core** (`src/finrag/core/`)# Windows PowerShell

  - `env_loader.py` - Environment variable management

  - `utils.py` - General utilities  - `base_models.py` - Abstract base classes$env:OPENAI_API_KEY="your-api-key-here"



## 🔧 Configuration  - `clustering.py` - RAPTOR clustering algorithm$env:LLAMA_CLOUD_API_KEY="your-llama-key-here"  # Optional but recommended



Configure via `.env` file or environment variables:  - `tree.py` - Hierarchical tree structure



```bash  - `retrieval.py` - Tree traversal and retrieval# Linux/Mac

# Required

OPENAI_API_KEY=sk-...export OPENAI_API_KEY="your-api-key-here"



# Recommended- **Models** (`src/finrag/models/`)export LLAMA_CLOUD_API_KEY="your-llama-key-here"  # Optional but recommended

LLAMA_CLOUD_API_KEY=llx-...

  - `models.py` - OpenAI implementations (embeddings, QA, summarization)```

# Optional customization

FINRAG_CHUNK_SIZE=512

FINRAG_TOP_K=10

FINRAG_TREE_DEPTH=3- **Utils** (`src/finrag/utils/`)**Option 2: In Code**

FINRAG_SUMMARIZATION_MODEL=gpt-3.5-turbo

FINRAG_EMBEDDING_MODEL=text-embedding-3-small  - `env_loader.py` - Environment variable management```python

FINRAG_LLM_MODEL=gpt-4-turbo-preview

```  - `utils.py` - General utilitiesfrom config import FinRAGConfig



See [docs/ENV_SETUP.md](docs/ENV_SETUP.md) for all available options.



## 📚 Documentation## 💻 Usage Examplesconfig = FinRAGConfig(



Comprehensive documentation available in [`docs/`](docs/):    openai_api_key="your-api-key-here",



- **[README.md](docs/README.md)** - Complete documentation### Basic Usage    llamaparse_api_key="your-llama-key-here"  # Optional but recommended

- **[GETTING_STARTED.md](docs/GETTING_STARTED.md)** - Quick start guide

- **[IMPLEMENTATION.md](docs/IMPLEMENTATION.md)** - Technical details)

- **[ENV_SETUP.md](docs/ENV_SETUP.md)** - Configuration guide

- **[QUICKREF.md](docs/QUICKREF.md)** - Quick reference```python```

- **[LLAMAPARSE.md](docs/LLAMAPARSE.md)** - PDF parsing guide

from finrag import FinRAG, FinRAGConfig

## 🧪 Testing

**Note**: LlamaParse API key is optional but **highly recommended** for financial documents with tables and complex layouts. See [LLAMAPARSE.md](LLAMAPARSE.md) for details.

```bash

# Test installation# Initialize (automatically loads from .env)

python tests/test_installation.py

config = FinRAGConfig()## Quick Start

# Test API keys

python tests/test_openai_key.pyfinrag = FinRAG(config)

```

### Basic Usage

## 📦 Package Installation

# Add documents

Install as a package for use in other projects:

documents = ["Your financial text here..."]```python

```bash

# Development mode (editable)finrag.add_documents(documents)import os

pip install -e .

from config import FinRAGConfig

# Production mode

pip install .# Queryfrom finrag import FinRAG

```

result = finrag.query("What is the revenue trend?")

Then import anywhere:

print(result['answer'])# Initialize FinRAG

```python

from finrag import FinRAG, FinRAGConfig```config = FinRAGConfig(

```

    openai_api_key=os.getenv("OPENAI_API_KEY"),

## 🎯 Advanced Features

### With PDF    chunk_size=512,

### Saving and Loading

    top_k=10,

```python

# Save processed index```python    tree_depth=3

finrag.save("./my_index")

# Load PDF)

# Load later

finrag_new = FinRAG(config)finrag.load_pdf("path/to/financial_report.pdf")

finrag_new.load("./my_index")

```finrag = FinRAG(config)



### Custom Retrieval# Query



```pythonresult = finrag.query("What are the key financial metrics?")# Load a financial document

# Tree traversal (default)

result = finrag.query(```text = finrag.load_pdf("financial_report.pdf")

    "Give me an overview",

    retrieval_method="tree_traversal"

)

### Custom Configuration# Build the RAPTOR tree

# Collapsed tree (for specific queries)

result = finrag.query(finrag.add_documents([text])

    "What was the exact revenue?",

    retrieval_method="collapsed_tree"```python

)

```config = FinRAGConfig(# Query the system



### Access Retrieved Context    chunk_size=1024,result = finrag.query("What is the revenue growth rate?")



```python    top_k=20,print(result['answer'])

result = finrag.query("What are the risk factors?")

print(f"Answer: {result['answer']}")    tree_depth=4,```

print(f"\nRetrieved {len(result['retrieved_nodes'])} nodes:")

    summarization_model="gpt-4-turbo-preview"

for node in result['retrieved_nodes'][:5]:

    print(f"- Level {node['level']} (Score: {node['score']:.3f})"))### Running the Demo

```

finrag = FinRAG(config)

## 🔍 How It Works

``````bash

### 1. Document Processing

Documents are chunked with financial-aware boundaries (preserving tables, lists, etc.)python main.py



### 2. Tree Building## 🔧 Configuration```

RAPTOR recursively:

1. Embeds all chunks

2. Clusters similar chunks using GMM

3. Summarizes each clusterConfigure via `.env` file or environment variables:This will:

4. Repeats for multiple levels

1. Load the included PDF document

### 3. Retrieval

When querying:```bash2. Build a RAPTOR tree structure

1. Query is embedded

2. Most relevant nodes are found# Required3. Run example queries

3. Context is gathered from nodes and children

OPENAI_API_KEY=sk-...4. Save and reload the system

### 4. Answer Generation

Retrieved context is fed to GPT-4 for accurate answers



## 📊 Comparison with Standard RAG# Recommended## Detailed Usage



| Feature | Standard RAG | FinRAG (RAPTOR) |LLAMA_CLOUD_API_KEY=llx-...

|---------|-------------|-----------------|

| Document Representation | Flat chunks | Hierarchical tree |### Configuration

| Retrieval | Single-level | Multi-level |

| Context | Fixed chunks | Adaptive summaries |# Optional customization

| Long Documents | May miss context | Better handling |

| Complex Queries | Limited | Improved performance |FINRAG_CHUNK_SIZE=512Customize FinRAG behavior through `FinRAGConfig`:



## 🛠️ DevelopmentFINRAG_TOP_K=10



### Adding New FeaturesFINRAG_TREE_DEPTH=3```python



1. Add core logic to `src/finrag/core/`FINRAG_SUMMARIZATION_MODEL=gpt-3.5-turboconfig = FinRAGConfig(

2. Add model implementations to `src/finrag/models/`

3. Add utilities to `src/finrag/utils/````    # API Configuration

4. Update `__init__.py` files

5. Add examples to `examples/`    openai_api_key="your-key",

6. Update documentation in `docs/`

See [docs/ENV_SETUP.md](docs/ENV_SETUP.md) for all available options.    

## 🤝 Contributing

    # Model Selection

Contributions welcome! Please:

## 🧪 Testing    embedding_model="text-embedding-3-small",

1. Fork the repository

2. Create a feature branch    llm_model="gpt-4-turbo-preview",

3. Make your changes

4. Add tests if applicable```powershell    summarization_model="gpt-4-turbo-preview",

5. Update documentation

6. Submit a pull request# Test installation    



## 📝 Referencespython tests/test_installation.py    # Chunking Parameters



- **RAPTOR Paper**: [Recursive Abstractive Processing for Tree-Organized Retrieval](https://arxiv.org/abs/2401.18059)    chunk_size=512,           # Tokens per chunk

- **RAPTOR GitHub**: [parthsarthi03/raptor](https://github.com/parthsarthi03/raptor)

# Test API keys    chunk_overlap=50,         # Overlap between chunks

## 📄 License

python tests/test_openai_key.py    

MIT License - See LICENSE file for details

```    # Tree Parameters

## 📞 Support

    tree_depth=3,             # Maximum tree depth

- **Documentation**: See `docs/` folder

- **Issues**: Report on GitHub## 📦 Package Installation    max_cluster_size=100,     # Maximum nodes per cluster

- **Questions**: Check `docs/QUICKREF.md`

    min_cluster_size=5,       # Minimum nodes per cluster

## 🙏 Acknowledgments

Install as a package for use in other projects:    

- Based on [RAPTOR](https://github.com/parthsarthi03/raptor) architecture

- Uses OpenAI API for embeddings and language models    # Retrieval Parameters

- LlamaParse for advanced PDF parsing

```powershell    top_k=10,                 # Number of documents to retrieve

---

# Development mode (editable)    similarity_threshold=0.7, # Minimum similarity score

**Happy Financial Analysis! 🚀📊**

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
