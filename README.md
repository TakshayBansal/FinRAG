
---

# FinRAG — Financial Retrieval-Augmented Generation

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

FinRAG is a domain-aware RAG system for financial documents, built on the RAPTOR (Recursive Abstractive Processing for Tree-Organized Retrieval) architecture. It adds financial-specific parsing, chunking, and retrieval strategies for accurate, grounded Q&A over long, complex reports.

---

## 🌟 Key Features

* 🌳 **Hierarchical RAG (RAPTOR):** Multi-level representations (chunks → cluster summaries → document summaries).
* 📊 **Financial Context Awareness:** Financial-aware chunking and summarization.
* 🧾 **Advanced PDF Parsing:** LlamaParse integration with PyPDF2 fallback.
* 🔍 **Multiple Retrieval Strategies:** Tree traversal and collapsed-tree search.
* 🎯 **Semantic Search:** OpenAI embeddings.
* 🧠 **Extensible Architecture:** Swap models for embeddings/LLMs/summarizers.
* 💾 **Caching:** Save and load processed indices.

---

## 📁 Project Structure

```
FinRAG/
├── docs/                 # Documentation
├── examples/             # Ready-to-run examples
├── scripts/              # Utilities
├── tests/                # Test scripts
├── src/finrag/
│   ├── core/             # Core algorithms (clustering, tree, retrieval)
│   ├── models/           # Model wrappers (OpenAI, etc.)
│   └── utils/            # Env loader, helpers
├── requirements.txt      # Python dependencies
└── README.md
```

*For a deeper breakdown, see `docs/PROJECT_STRUCTURE.md` (optional).*

---

## 🚀 Quick Start

### 1) Install

```bash
# clone your repo first, then:
pip install -r requirements.txt

# or editable install during development
pip install -e .
```

### 2) Configure API keys

Create a `.env` from the template and edit it:

```bash
cp .env.example .env
```

```bash
# .env (required)
OPENAI_API_KEY=sk-your-key-here

# optional but recommended for better PDFs
LLAMA_CLOUD_API_KEY=llx-your-key-here
```

### 3) Run examples

```bash
# simple example (sample data)
python examples/example.py

# full PDF demo
python examples/main.py

# interactive CLI
python examples/cli.py
```

---

## 💻 Usage

### Basic usage

```python
from finrag import FinRAG, FinRAGConfig

config = FinRAGConfig()             # loads keys from .env by default
finrag = FinRAG(config)

# Add raw text documents
finrag.add_documents(["Your financial text here..."])

# Ask a question
result = finrag.query("What is the revenue trend?")
print(result["answer"])
```

### PDFs

```python
from finrag import FinRAG, FinRAGConfig

finrag = FinRAG(FinRAGConfig())
finrag.load_pdf("financial_report.pdf")
result = finrag.query("What are the key financial metrics?")
print(result["answer"])
```

### Custom configuration

```python
from finrag import FinRAG, FinRAGConfig

config = FinRAGConfig(
    chunk_size=1024,
    top_k=20,
    tree_depth=4,
    summarization_model="gpt-4-turbo-preview"
)
finrag = FinRAG(config)
```

### Saving & loading

```python
finrag.save("./my_index")          # save
finrag2 = FinRAG(FinRAGConfig())   # new instance
finrag2.load("./my_index")         # load without rebuilding
```

### Access retrieved context

```python
res = finrag.query("What are the risk factors?")
print("Answer:", res["answer"])
print("Retrieved nodes:", len(res["retrieved_nodes"]))
for n in res["retrieved_nodes"][:5]:
    print(f"- Level {n['level']}  Score {n['score']:.3f}")
```

---

## 🏗️ Architecture (RAPTOR)

```
┌───────────────────────────────────────────────────────┐
│                 Financial Documents                    │
└───────────────┬───────────────────────────────────────┘
                │  (financial-aware chunking)
                ▼
┌───────────────────────────────────────────────────────┐
│                Document Chunking                       │
└───────────────┬───────────────────────────────────────┘
                │  (OpenAI embeddings)
                ▼
┌───────────────────────────────────────────────────────┐
│               Embedding Generation                     │
└───────────────┬───────────────────────────────────────┘
                │  (recursive clustering + summaries)
                ▼
┌───────────────────────────────────────────────────────┐
│                 RAPTOR Tree Building                   │
│  Level 2: High-level summaries (root)                  │
│  Level 1: Mid-level summaries (clusters)               │
│  Level 0: Original chunks (leaves)                     │
└───────────────┬───────────────────────────────────────┘
                │  (tree traversal / collapsed search)
                ▼
┌───────────────────────────────────────────────────────┐
│           Query Processing & Retrieval                 │
└───────────────┬───────────────────────────────────────┘
                │  (GPT-4/selected LLM with context)
                ▼
┌───────────────────────────────────────────────────────┐
│                 Question Answering                     │
└───────────────────────────────────────────────────────┘
```

---

## 🔧 Configuration

### Via `.env`

```bash
# required
OPENAI_API_KEY=sk-...

# recommended (better tables/layout)
LLAMA_CLOUD_API_KEY=llx-...

# optional tunables
FINRAG_CHUNK_SIZE=512
FINRAG_TOP_K=10
FINRAG_TREE_DEPTH=3
FINRAG_SUMMARIZATION_MODEL=gpt-4-turbo-preview
FINRAG_EMBEDDING_MODEL=text-embedding-3-small
FINRAG_LLM_MODEL=gpt-4-turbo-preview
```

### In code

```python
from finrag import FinRAGConfig
cfg = FinRAGConfig(
    openai_api_key="...",
    llamaparse_api_key="...",
    chunk_size=512,
    top_k=10,
    tree_depth=3,
)
```

---

## 🔍 Retrieval Methods

```python
# Tree traversal (default) — broad questions
finrag.query("Give me an overview", retrieval_method="tree_traversal")

# Collapsed tree — precise facts
finrag.query("What was the exact revenue in Q3 2024?",
             retrieval_method="collapsed_tree")
```

---

## 📊 Helpful APIs

```python
stats = finrag.get_statistics()
print("Total nodes:", stats["total_nodes"])
print("Tree depth:", stats["tree_depth"])
print("Nodes per level:", stats["levels"])
```

---

## 🧪 Testing

```bash
python tests/test_installation.py
python tests/test_openai_key.py
```

---

## 📦 Using as a Package

```bash
# development
pip install -e .

# production
pip install .
```

Then:

```python
from finrag import FinRAG, FinRAGConfig
```

---

## 🧰 Advanced (Custom Models)

```python
from base_models import BaseEmbeddingModel, BaseSummarizationModel, BaseQAModel
from tree import RAPTORTree, TreeConfig

class CustomEmbedding(BaseEmbeddingModel):
    def create_embedding(self, text): ...
class CustomSummarizer(BaseSummarizationModel):
    def summarize(self, texts, max_tokens=200): ...
class CustomQA(BaseQAModel):
    def answer_question(self, context, question): ...

tree = RAPTORTree(
    embedding_model=CustomEmbedding(),
    summarization_model=CustomSummarizer(),
    config=TreeConfig()
)
```

---

## ⚙️ Performance Tips

1. **Chunk size:** 256–512 for precise facts; 512–1024 for broad summaries.
2. **Tree depth:** 2–3 for single docs; 4+ for large corpora.
3. **Top-K:** 5–10 for focused answers; 15–20 for comprehensive context.
4. **Caching:** Save/load the tree for repeat queries.

---

## 🧯 Troubleshooting

* **OOM while building tree:** Lower `chunk_size` or `max_cluster_size`; process in batches.
* **Slow retrieval:** Lower `top_k`; try `collapsed_tree`; enable caching.
* **Weak answers:** Increase `top_k`; adjust `chunk_size`; switch retrieval method.
* **PDF tables lost:** Use LlamaParse (set `LLAMA_CLOUD_API_KEY`).

---

## 📚 References

* RAPTOR paper: [https://arxiv.org/abs/2401.18059](https://arxiv.org/abs/2401.18059)
* RAPTOR GitHub: [https://github.com/parthsarthi03/raptor](https://github.com/parthsarthi03/raptor)
* OpenAI API docs: [https://platform.openai.com/docs](https://platform.openai.com/docs)

---

## 📄 License

MIT — see `LICENSE`.

---

## 🤝 Contributing

1. Fork
2. Create a feature branch
3. Implement & add tests
4. Update docs
5. Open a PR

---
