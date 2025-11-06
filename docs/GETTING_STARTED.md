# 🚀 Getting Started with FinRAG

Welcome to FinRAG! This guide will help you get up and running in 5 minutes.

## Step 1: Install Dependencies (2 minutes)

Open PowerShell and navigate to the FinRAG directory:

```powershell
cd "c:\Users\Takshay\Desktop\Coding\Pathway\RAG\FinRAG"
```

Install required packages:

```powershell
pip install -r requirements.txt
```

## Step 2: Set Your API Keys (1 minute)

### Recommended: Use .env file (persistent)

1. Copy the example file:
```powershell
Copy-Item .env.example .env
```

2. Open `.env` in a text editor and add your keys:
```bash
OPENAI_API_KEY=sk-your-actual-openai-key-here
LLAMA_CLOUD_API_KEY=llx-your-actual-llamaparse-key-here
```

That's it! The keys will load automatically when you run FinRAG.

### Alternative: Set environment variables (temporary)

**Windows PowerShell:**
```powershell
$env:OPENAI_API_KEY="sk-your-actual-api-key-here"
$env:LLAMA_CLOUD_API_KEY="llx-your-actual-api-key-here"
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY="sk-your-actual-api-key-here"
export LLAMA_CLOUD_API_KEY="llx-your-actual-api-key-here"
```

### Getting API Keys

- **OpenAI** (required): https://platform.openai.com/api-keys
- **LlamaParse** (recommended): https://cloud.llamaindex.ai/

**Note**: LlamaParse is **highly recommended** for financial documents. It preserves tables and complex layouts. PyPDF2 will be used as fallback if not available. See [LLAMAPARSE.md](LLAMAPARSE.md) and [ENV_SETUP.md](ENV_SETUP.md) for details.

## Step 3: Verify Installation (1 minute)

Run the test script:

```powershell
python test_installation.py
```

You should see all tests pass with ✅ marks.

## Step 4: Run Your First Example (1 minute)

### Option A: Use Sample Data

```powershell
python example.py
```

This will:
- Create sample financial documents
- Build a RAPTOR tree
- Run example queries
- Show you how it works

### Option B: Use Your PDF

```powershell
python main.py
```

This will:
- Load the included PDF (256911814.pdf)
- Build a hierarchical tree
- Answer financial questions
- Save the system for later use

### Option C: Interactive Mode

```powershell
python cli.py
```

This gives you an interactive menu where you can:
1. Load your own documents
2. Ask questions
3. Save/load the system
4. View statistics

## Step 5: Try It Yourself

Create a simple script:

```python
# my_first_finrag.py
import os
from config import FinRAGConfig
from finrag import FinRAG

# Initialize
config = FinRAGConfig(
    openai_api_key=os.getenv("OPENAI_API_KEY")
)
finrag = FinRAG(config)

# Add a sample document
sample_text = """
Tech Company Q4 2024 Financial Results:
- Revenue: $100M (up 50% YoY)
- Net Income: $25M (up 60% YoY)
- Operating Margin: 25%

The company saw strong growth in cloud services,
which now represents 70% of total revenue.
"""

finrag.add_documents([sample_text])

# Ask questions
questions = [
    "What was the revenue?",
    "What is the main source of revenue?",
    "How much did net income grow?"
]

for q in questions:
    result = finrag.query(q)
    print(f"\nQ: {q}")
    print(f"A: {result['answer']}\n")
```

Run it:

```powershell
python my_first_finrag.py
```

## Common Use Cases

### 1. Analyze a Financial Report

```python
finrag = FinRAG(config)
text = finrag.load_pdf("annual_report.pdf")
finrag.add_documents([text])

# Ask questions
result = finrag.query("What are the key financial metrics?")
print(result['answer'])
```

### 2. Compare Multiple Documents

```python
finrag = FinRAG(config)

docs = [
    finrag.load_pdf("Q1_report.pdf"),
    finrag.load_pdf("Q2_report.pdf"),
    finrag.load_pdf("Q3_report.pdf")
]

finrag.add_documents(docs)

result = finrag.query("How did performance change across quarters?")
print(result['answer'])
```

### 3. Build a Persistent Index

```python
# First time - build the index
finrag = FinRAG(config)
finrag.add_documents(your_documents)
finrag.save("./my_company_index")

# Later - instant loading
finrag = FinRAG(config)
finrag.load("./my_company_index")
result = finrag.query("Quick question")
```

## Understanding the Output

When you query the system, you get:

```python
result = {
    'answer': "The detailed answer to your question...",
    'context': "The retrieved context used to answer...",
    'question': "Your original question",
    'retrieved_nodes': [
        {
            'node_id': 'level_1_cluster_0',
            'level': 1,  # 0=original, 1=summary, 2=high-level
            'score': 0.95,  # Relevance score
            'text_preview': "Preview of the text..."
        },
        # ... more nodes
    ],
    'retrieval_method': 'tree_traversal'
}
```

Access specific parts:

```python
print(result['answer'])  # Just the answer
print(result['retrieved_nodes'][0]['score'])  # Top relevance score
print(len(result['retrieved_nodes']))  # Number of sources
```

## Configuration Tips

### For Quick Answers (Fast)
```python
config = FinRAGConfig(
    chunk_size=256,
    top_k=5,
    tree_depth=2
)
```

### For Comprehensive Answers (Thorough)
```python
config = FinRAGConfig(
    chunk_size=512,
    top_k=20,
    tree_depth=4
)
```

### For Large Documents
```python
config = FinRAGConfig(
    chunk_size=1024,
    max_cluster_size=150,
    tree_depth=4
)
```

## Troubleshooting

### "No module named 'openai'"
```powershell
pip install openai
```

### "OPENAI_API_KEY environment variable not set"
```powershell
$env:OPENAI_API_KEY="your-key-here"
```

### Out of Memory
Use smaller chunk size:
```python
config = FinRAGConfig(chunk_size=256)
```

### Slow Performance
Reduce top_k:
```python
result = finrag.query(question, top_k=5)
```

### Poor Answers
Try different retrieval method:
```python
result = finrag.query(question, retrieval_method="collapsed_tree")
```

## Next Steps

1. **Read the full documentation**: `README.md`
2. **Understand the architecture**: `IMPLEMENTATION.md`
3. **Quick reference**: `QUICKREF.md`
4. **Run examples**: `example.py`, `main.py`, `cli.py`

## Example Workflows

### Workflow 1: One-Time Analysis
```powershell
python example.py  # Modify to use your data
```

### Workflow 2: Interactive Exploration
```powershell
python cli.py
# Then: Load documents → Query → Repeat
```

### Workflow 3: Production Use
```python
# build_index.py
finrag = FinRAG(config)
finrag.add_documents(all_your_docs)
finrag.save("./production_index")

# query_api.py
finrag = FinRAG(config)
finrag.load("./production_index")
# Handle user queries...
```

## Key Concepts

### 🌳 Tree Structure
- **Level 0**: Original text chunks
- **Level 1**: Summaries of similar chunks
- **Level 2**: High-level overview

### 🔍 Retrieval Methods
- **tree_traversal**: Start broad, drill down (good for "What are the highlights?")
- **collapsed_tree**: Search everything (good for "What was Q3 revenue?")

### 📊 Parameters
- **chunk_size**: Bigger = more context, smaller = more precise
- **top_k**: More = comprehensive, fewer = focused
- **tree_depth**: Deeper = better for long documents

## Quick Tips

1. **Start small**: Test with one document first
2. **Save your index**: Don't rebuild every time
3. **Experiment**: Try different retrieval methods
4. **Monitor**: Check `get_statistics()` to understand your tree
5. **Iterate**: Adjust config based on answer quality

## Resources

- **Full Documentation**: README.md
- **Architecture Details**: IMPLEMENTATION.md
- **Quick Reference**: QUICKREF.md
- **RAPTOR Paper**: https://arxiv.org/abs/2401.18059
- **OpenAI Docs**: https://platform.openai.com/docs

## Get Help

If something isn't working:

1. Run `python test_installation.py`
2. Check your API key is set
3. Make sure all packages are installed
4. Read the error message carefully
5. Check the documentation

## You're Ready!

You now have everything you need to use FinRAG. Start with:

```powershell
python example.py
```

Then explore the other examples and customize for your needs.

Happy querying! 🎉
