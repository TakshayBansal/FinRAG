# Environment Variables Setup Guide

## Quick Setup (Recommended)

### 1. Create .env file

Copy the example file:
```powershell
Copy-Item .env.example .env
```

### 2. Edit .env file

Open `.env` in your text editor and add your API keys:

```bash
# OpenAI API Key (Required)
OPENAI_API_KEY=sk-your-actual-openai-key-here

# LlamaParse API Key (Optional but Recommended)
LLAMA_CLOUD_API_KEY=llx-your-actual-llamaparse-key-here
```

### 3. Run FinRAG

That's it! Just run any script:
```powershell
python example.py
```

The `.env` file is automatically loaded when you run FinRAG.

---

## Environment Variables Reference

### Required Variables

#### `OPENAI_API_KEY`
- **Description**: OpenAI API key for embeddings and chat
- **Get it**: https://platform.openai.com/api-keys
- **Format**: `sk-...` (starts with sk-)
- **Example**: `OPENAI_API_KEY=sk-proj-abc123...`

### Recommended Variables

#### `LLAMA_CLOUD_API_KEY`
- **Description**: LlamaParse API key for enhanced PDF parsing
- **Get it**: https://cloud.llamaindex.ai/
- **Format**: `llx-...` (starts with llx-)
- **Example**: `LLAMA_CLOUD_API_KEY=llx-abc123...`
- **Note**: If not set, falls back to PyPDF2 (basic parsing)

### Optional Configuration Variables

All optional variables have sensible defaults. Only set them if you want to customize behavior.

#### General Settings

**`FINRAG_CHUNK_SIZE`**
- Chunk size in tokens
- Default: `512`
- Recommended: 256-1024
- Example: `FINRAG_CHUNK_SIZE=400`

**`FINRAG_CHUNK_OVERLAP`**
- Overlap between chunks in tokens
- Default: `50`
- Recommended: 20-100
- Example: `FINRAG_CHUNK_OVERLAP=30`

**`FINRAG_TOP_K`**
- Number of documents to retrieve
- Default: `10`
- Recommended: 5-20
- Example: `FINRAG_TOP_K=15`

**`FINRAG_TREE_DEPTH`**
- RAPTOR tree depth (levels)
- Default: `3`
- Recommended: 2-4
- Example: `FINRAG_TREE_DEPTH=4`

**`FINRAG_TRAVERSAL_METHOD`**
- Retrieval method
- Options: `tree_traversal`, `collapsed_tree`
- Default: `tree_traversal`
- Example: `FINRAG_TRAVERSAL_METHOD=collapsed_tree`

#### LlamaParse Settings

**`FINRAG_USE_LLAMAPARSE`**
- Enable/disable LlamaParse
- Options: `true`, `false`
- Default: `true`
- Example: `FINRAG_USE_LLAMAPARSE=false`

**`FINRAG_LLAMAPARSE_MODE`**
- Parsing quality mode
- Options: `parse_page_with_llm` (best), `fast` (good)
- Default: `parse_page_with_llm`
- Example: `FINRAG_LLAMAPARSE_MODE=fast`

**`FINRAG_LLAMAPARSE_WORKERS`**
- Number of parallel workers
- Default: `4`
- Recommended: 2-8
- Example: `FINRAG_LLAMAPARSE_WORKERS=6`

**`FINRAG_LLAMAPARSE_LANGUAGE`**
- Document language
- Default: `en`
- Example: `FINRAG_LLAMAPARSE_LANGUAGE=en`

#### Model Settings

**`FINRAG_EMBEDDING_MODEL`**
- OpenAI embedding model
- Default: `text-embedding-3-small`
- Options: `text-embedding-3-small`, `text-embedding-3-large`
- Example: `FINRAG_EMBEDDING_MODEL=text-embedding-3-large`

**`FINRAG_LLM_MODEL`**
- Chat/QA model
- Default: `gpt-4-turbo-preview`
- Options: `gpt-4-turbo-preview`, `gpt-4`, `gpt-3.5-turbo`
- Example: `FINRAG_LLM_MODEL=gpt-4`

**`FINRAG_SUMMARIZATION_MODEL`**
- Summarization model
- Default: `gpt-4-turbo-preview`
- Options: Same as LLM model
- Example: `FINRAG_SUMMARIZATION_MODEL=gpt-4`

#### Cache Settings

**`FINRAG_USE_CACHE`**
- Enable caching
- Options: `true`, `false`
- Default: `true`
- Example: `FINRAG_USE_CACHE=false`

**`FINRAG_CACHE_DIR`**
- Cache directory path
- Default: `./cache`
- Example: `FINRAG_CACHE_DIR=/tmp/finrag_cache`

---

## Setup Methods

### Method 1: .env File (Recommended)

**Advantages:**
- ✅ Persistent across sessions
- ✅ Easy to manage
- ✅ No command line needed
- ✅ Automatically loaded
- ✅ Can be version controlled (use .env.example)

**Steps:**
1. Copy `.env.example` to `.env`
2. Edit `.env` and add your keys
3. Run your script

### Method 2: Environment Variables

**Advantages:**
- ✅ Temporary (session only)
- ✅ Quick testing
- ✅ No file needed

**PowerShell:**
```powershell
$env:OPENAI_API_KEY="sk-..."
$env:LLAMA_CLOUD_API_KEY="llx-..."
python example.py
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY="sk-..."
export LLAMA_CLOUD_API_KEY="llx-..."
python example.py
```

### Method 3: Direct in Code

**Advantages:**
- ✅ Full control
- ✅ Dynamic configuration

**Example:**
```python
from config import FinRAGConfig

config = FinRAGConfig(
    openai_api_key="sk-...",
    llamaparse_api_key="llx-...",
    chunk_size=1024
)
```

---

## Complete .env Example

Here's a fully configured `.env` file:

```bash
# FinRAG Environment Variables

# Required
OPENAI_API_KEY=sk-proj-abc123def456...

# Recommended
LLAMA_CLOUD_API_KEY=llx-xyz789uvw012...

# General Configuration
FINRAG_CHUNK_SIZE=512
FINRAG_CHUNK_OVERLAP=50
FINRAG_TOP_K=10
FINRAG_TREE_DEPTH=3
FINRAG_TRAVERSAL_METHOD=tree_traversal

# LlamaParse Configuration
FINRAG_USE_LLAMAPARSE=true
FINRAG_LLAMAPARSE_MODE=parse_page_with_llm
FINRAG_LLAMAPARSE_WORKERS=4
FINRAG_LLAMAPARSE_LANGUAGE=en

# Model Configuration
FINRAG_EMBEDDING_MODEL=text-embedding-3-small
FINRAG_LLM_MODEL=gpt-4-turbo-preview
FINRAG_SUMMARIZATION_MODEL=gpt-4-turbo-preview

# Cache Configuration
FINRAG_USE_CACHE=true
FINRAG_CACHE_DIR=./cache
```

---

## Testing Your Setup

Run the environment checker:

```powershell
python env_loader.py
```

Expected output:
```
✓ Loaded environment variables from: .env
✓ OPENAI_API_KEY: ********abc1 (OpenAI API key...)
✓ LLAMA_CLOUD_API_KEY: ********xyz9 (LlamaParse API key...)
```

Or run the full installation test:

```powershell
python test_installation.py
```

---

## Troubleshooting

### ".env file not found"
- Make sure `.env` exists in the FinRAG directory
- Check you're running from the correct directory
- Try absolute path: `python c:\full\path\to\example.py`

### "API key not set"
- Check `.env` file has correct format (no quotes needed)
- Verify no spaces around `=`
- Correct: `OPENAI_API_KEY=sk-123`
- Wrong: `OPENAI_API_KEY = "sk-123"`

### ".env not loading"
- Install python-dotenv: `pip install python-dotenv`
- Check `.env` file encoding (should be UTF-8)
- Verify file isn't `.env.txt` (no extension needed)

### "Permission denied"
- Check file permissions
- Make sure `.env` is readable
- On Linux/Mac: `chmod 644 .env`

---

## Security Best Practices

### ✅ DO:
- Add `.env` to `.gitignore` (already done)
- Use `.env.example` for templates
- Keep API keys private
- Rotate keys regularly
- Use different keys for dev/prod

### ❌ DON'T:
- Commit `.env` to git
- Share API keys
- Store keys in code
- Use production keys in development
- Expose keys in logs

---

## Getting API Keys

### OpenAI API Key (Required)

1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Click "Create new secret key"
5. Copy the key (starts with `sk-`)
6. Add to `.env`: `OPENAI_API_KEY=sk-your-key`

**Cost**: Pay-as-you-go, ~$0.01-0.10 per query

### LlamaParse API Key (Recommended)

1. Go to https://cloud.llamaindex.ai/
2. Sign up for free account
3. Navigate to API Keys
4. Create new API key
5. Copy the key (starts with `llx-`)
6. Add to `.env`: `LLAMA_CLOUD_API_KEY=llx-your-key`

**Cost**: Free tier (1,000 pages/day), then $49/month

---

## Quick Commands

```powershell
# Create .env from template
Copy-Item .env.example .env

# Check environment variables
python env_loader.py

# Test installation
python test_installation.py

# Run example
python example.py

# Interactive mode
python cli.py
```

---

## Summary

1. **Copy** `.env.example` to `.env`
2. **Edit** `.env` and add your API keys
3. **Run** any FinRAG script - it loads automatically!

That's it! The `.env` file makes managing API keys simple and secure. 🎉
