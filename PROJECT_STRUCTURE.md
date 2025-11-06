# FinRAG Project Structure

```
FinRAG/
│
├── src/                          # Source code
│   └── finrag/                   # Main package
│       ├── __init__.py
│       ├── config.py             # Configuration management
│       ├── finrag.py             # Main FinRAG class
│       │
│       ├── core/                 # Core components
│       │   ├── __init__.py
│       │   ├── base_models.py   # Abstract base classes
│       │   ├── clustering.py    # RAPTOR clustering algorithm
│       │   ├── tree.py          # Hierarchical tree structure
│       │   └── retrieval.py     # Retrieval strategies
│       │
│       ├── models/               # Model implementations
│       │   ├── __init__.py
│       │   └── models.py        # OpenAI model implementations
│       │
│       └── utils/                # Utilities
│           ├── __init__.py
│           ├── env_loader.py    # Environment variable management
│           └── utils.py         # General utilities
│
├── examples/                     # Example scripts
│   ├── example.py               # Simple example with sample data
│   ├── main.py                  # Full demo with PDF
│   └── cli.py                   # Interactive CLI
│
├── tests/                        # Test files
│   ├── test_installation.py     # Installation verification
│   └── test_openai_key.py       # API key validation
│
├── docs/                         # Documentation
│   ├── README.md                # Main documentation
│   ├── GETTING_STARTED.md       # Quick start guide
│   ├── IMPLEMENTATION.md        # Implementation details
│   ├── SETUP.md                 # Setup instructions
│   ├── ENV_SETUP.md             # Environment variables guide
│   ├── QUICKREF.md              # Quick reference
│   ├── LLAMAPARSE.md            # LlamaParse integration
│   ├── LLAMAPARSE_INTEGRATION.md
│   └── PARSER_COMPARISON.md
│
├── scripts/                      # Utility scripts
│   └── setup.ps1                # PowerShell setup script
│
├── data/                         # Data files
│   ├── 256911814.pdf            # Sample PDF
│   └── finrag_example_index/    # Cached indices
│
├── cache/                        # Cache directory
│
├── .env                          # Environment variables (not in git)
├── .env.example                  # Environment template
├── .gitignore                    # Git ignore rules
└── requirements.txt              # Python dependencies
```

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   copy .env.example .env
   # Edit .env and add your API keys
   ```

3. **Run examples:**
   ```bash
   # Simple example
   python examples/example.py
   
   # Full PDF example
   python examples/main.py
   
   # Interactive CLI
   python examples/cli.py
   ```

## Module Organization

- **src/finrag/core/** - Core algorithms and data structures
- **src/finrag/models/** - AI model implementations (OpenAI)
- **src/finrag/utils/** - Helper functions and utilities
- **examples/** - Usage examples and demos
- **tests/** - Testing and validation scripts
- **docs/** - Comprehensive documentation

For detailed documentation, see `docs/README.md`.
