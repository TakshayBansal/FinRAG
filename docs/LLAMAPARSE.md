# LlamaParse Integration Guide

## What is LlamaParse?

LlamaParse is an advanced document parsing service that uses LLMs to intelligently extract content from PDFs. It's **significantly better** than traditional parsers like PyPDF2, especially for:

- 📊 **Tables and structured data**
- 📈 **Charts and figures** (with descriptions)
- 📄 **Complex layouts** (multi-column, headers/footers)
- 🔢 **Financial statements** (preserves structure)
- 📋 **Forms and formatted documents**

## Why Use LlamaParse with FinRAG?

Financial documents often contain:
- Complex tables (balance sheets, income statements)
- Multi-column layouts
- Charts and graphs
- Structured financial data

**PyPDF2** extracts text but loses structure → Poor context for RAG  
**LlamaParse** preserves structure in Markdown → Better context for RAG

## Setup

### 1. Get API Key

1. Go to https://cloud.llamaindex.ai/
2. Sign up for an account
3. Get your API key from the dashboard
4. Free tier includes 1,000 pages/day

### 2. Set Environment Variable

**Windows PowerShell:**
```powershell
$env:LLAMA_CLOUD_API_KEY="llx-your-api-key-here"
```

**Linux/Mac:**
```bash
export LLAMA_CLOUD_API_KEY="llx-your-api-key-here"
```

**Permanent (Windows):**
```powershell
[System.Environment]::SetEnvironmentVariable('LLAMA_CLOUD_API_KEY', 'llx-your-key', 'User')
```

### 3. Install Package

```bash
pip install llama-parse llama-cloud-services
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

## Usage in FinRAG

### Automatic (Recommended)

FinRAG will automatically use LlamaParse if the API key is set:

```python
from finrag import FinRAG
from config import FinRAGConfig
import os

# API key from environment
config = FinRAGConfig(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    llamaparse_api_key=os.getenv("LLAMA_CLOUD_API_KEY"),
    use_llamaparse=True  # Default is True
)

finrag = FinRAG(config)

# This will use LlamaParse automatically
text = finrag.load_pdf("financial_report.pdf")
finrag.add_documents([text])
```

### Manual Control

Force LlamaParse or PyPDF2:

```python
# Force LlamaParse
text = finrag.load_pdf("report.pdf", use_llamaparse=True)

# Force PyPDF2 (fallback)
text = finrag.load_pdf("report.pdf", use_llamaparse=False)
```

### Configuration Options

```python
config = FinRAGConfig(
    # LlamaParse settings
    use_llamaparse=True,
    llamaparse_mode="parse_page_with_llm",  # High-quality (slower)
    # llamaparse_mode="fast",  # Basic parsing (faster)
    llamaparse_num_workers=4,  # Parallel processing
    llamaparse_language="en",  # Document language
)
```

## Parsing Modes

### 1. `parse_page_with_llm` (Recommended for Financial Docs)
- Uses LLM to understand document structure
- Best quality, preserves tables and layouts
- Slower, uses more credits
- **Best for**: Financial reports, complex documents

### 2. `fast` (Basic Mode)
- Fast text extraction
- Better than PyPDF2, not as good as full LLM mode
- Fewer credits used
- **Best for**: Simple documents, high volume

## Example: Financial Report Parsing

### Without LlamaParse (PyPDF2)
```
Q4 2024 Revenue $500M Net Income $125M Operating 
Margin 25% Assets Liabilities Equity Cash $100M 
Debt $200M Retained $400M
```
❌ Structure lost, hard to understand

### With LlamaParse
```markdown
## Q4 2024 Financial Highlights

| Metric | Value |
|--------|-------|
| Revenue | $500M |
| Net Income | $125M |
| Operating Margin | 25% |

## Balance Sheet

| Assets | Liabilities | Equity |
|--------|-------------|--------|
| Cash: $100M | Debt: $200M | Retained: $400M |
```
✅ Structure preserved, easy to understand

## Fallback Behavior

FinRAG automatically falls back to PyPDF2 if:
1. LlamaParse API key not set
2. LlamaParse package not installed
3. LlamaParse API fails or times out
4. `use_llamaparse=False` in config

```python
# This will try LlamaParse, fallback to PyPDF2 if unavailable
text = finrag.load_pdf("report.pdf")
```

## Cost Considerations

### LlamaParse Pricing (as of 2024)
- **Free Tier**: 1,000 pages/day
- **Pro**: $49/month for 10,000 pages
- **Enterprise**: Custom pricing

### When to Use LlamaParse
✅ **Use for**:
- Financial reports with tables
- Earnings calls transcripts
- SEC filings
- Complex multi-column documents
- Documents with charts/figures

❌ **Skip for**:
- Simple plain text documents
- Pre-formatted markdown/text
- Very large batch processing (cost)
- Real-time applications (latency)

## Performance Comparison

### PyPDF2
- Speed: ⚡⚡⚡ Very fast
- Quality: ⭐⭐ Basic
- Tables: ❌ Lost
- Structure: ❌ Lost
- Cost: 💰 Free

### LlamaParse
- Speed: ⚡ Moderate (API call)
- Quality: ⭐⭐⭐⭐⭐ Excellent
- Tables: ✅ Preserved
- Structure: ✅ Preserved in Markdown
- Cost: 💰💰 Paid (free tier available)

## Troubleshooting

### "Module not found: llama_cloud_services"
```bash
pip install llama-parse llama-cloud-services
```

### "API key invalid"
- Check your key at https://cloud.llamaindex.ai/
- Make sure it starts with `llx-`
- Verify environment variable is set:
  ```powershell
  echo $env:LLAMA_CLOUD_API_KEY
  ```

### "Rate limit exceeded"
- Free tier: 1,000 pages/day
- Wait or upgrade to Pro plan
- Use `use_llamaparse=False` temporarily

### Slow parsing
- Use `llamaparse_mode="fast"` for faster parsing
- Increase `llamaparse_num_workers` for parallel processing
- Consider batching documents

## Complete Example

```python
import os
from config import FinRAGConfig
from finrag import FinRAG

# Setup with both API keys
config = FinRAGConfig(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    llamaparse_api_key=os.getenv("LLAMA_CLOUD_API_KEY"),
    
    # LlamaParse settings
    use_llamaparse=True,
    llamaparse_mode="parse_page_with_llm",  # Best quality
    llamaparse_num_workers=4,
    
    # FinRAG settings
    chunk_size=512,
    top_k=10,
    tree_depth=3
)

finrag = FinRAG(config)

# Load financial report (will use LlamaParse)
print("Loading financial report with LlamaParse...")
text = finrag.load_pdf("annual_report_2024.pdf")

# Build tree
finrag.add_documents([text])

# Query with better context thanks to preserved structure
result = finrag.query("What was the revenue breakdown by segment?")
print(result['answer'])

# Save for reuse
finrag.save("./financial_index")
```

## Best Practices

1. **Set API keys as environment variables** (don't hardcode)
2. **Enable LlamaParse for financial documents** (better quality)
3. **Use PyPDF2 fallback for simple docs** (save credits)
4. **Test with small docs first** (verify parsing quality)
5. **Monitor usage** (free tier limits)
6. **Cache parsed results** (save API calls)

## Additional Resources

- LlamaParse Docs: https://docs.llamaindex.ai/en/stable/llama_cloud/llama_parse/
- API Dashboard: https://cloud.llamaindex.ai/
- FinRAG Implementation: See `finrag.py` for code

## Summary

✅ **Recommended Setup**:
```powershell
# Install
pip install llama-parse llama-cloud-services

# Set keys
$env:OPENAI_API_KEY="sk-..."
$env:LLAMA_CLOUD_API_KEY="llx-..."

# Run
python example.py
```

LlamaParse integration is **optional but highly recommended** for financial documents. FinRAG will work with or without it, but document understanding will be significantly better with LlamaParse enabled.
