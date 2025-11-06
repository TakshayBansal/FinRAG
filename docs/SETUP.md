# FinRAG Setup Guide

## Installation Steps

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set OpenAI API Key

**Windows PowerShell:**
```powershell
$env:OPENAI_API_KEY="your-openai-api-key-here"
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

**Permanent (Windows):**
```powershell
[System.Environment]::SetEnvironmentVariable('OPENAI_API_KEY', 'your-key', 'User')
```

### 3. Verify Installation

```bash
python -c "import openai, numpy, sklearn; print('✅ All dependencies installed')"
```

## Quick Test

Run the example script:
```bash
python example.py
```

## Usage Options

### Option 1: Interactive CLI
```bash
python cli.py
```

### Option 2: Python Script
```python
from finrag import FinRAG
from config import FinRAGConfig

config = FinRAGConfig()
finrag = FinRAG(config)

# Your code here
```

### Option 3: Use the Demo
```bash
python main.py
```

## Troubleshooting

### Import Errors
```bash
pip install --upgrade -r requirements.txt
```

### API Key Issues
Make sure your OpenAI API key is valid and has credits.

### Memory Issues
Reduce `chunk_size` and `max_cluster_size` in config:
```python
config = FinRAGConfig(
    chunk_size=256,
    max_cluster_size=50
)
```

## Next Steps

1. Place your PDF documents in the same directory
2. Run `python example.py` to see it in action
3. Modify `config.py` for your needs
4. Read `README.md` for detailed documentation

## Getting Help

- Check `README.md` for detailed documentation
- Review `example.py` for usage patterns
- Original RAPTOR paper: https://arxiv.org/abs/2401.18059
- RAPTOR repo: https://github.com/parthsarthi03/raptor
