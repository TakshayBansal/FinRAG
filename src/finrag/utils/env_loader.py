"""
Environment variable management utilities for FinRAG.
"""
import os
from pathlib import Path
from typing import Optional


def load_env_file(env_path: Optional[str] = None) -> bool:
    """
    Load environment variables from .env file.
    
    Args:
        env_path: Path to .env file (default: looks in project root)
    
    Returns:
        True if .env file was loaded, False otherwise
    """
    try:
        from dotenv import load_dotenv
        
        if env_path is None:
            # Look for .env in project root
            current_dir = Path(__file__).parent
            env_path = current_dir / '.env'
        else:
            env_path = Path(env_path)
        
        if env_path.exists():
            load_dotenv(dotenv_path=env_path, override=True)
            print(f"✓ Loaded environment variables from: {env_path}")
            return True
        else:
            print(f"⚠ .env file not found at: {env_path}")
            print("  Using system environment variables only")
            return False
            
    except ImportError:
        print("⚠ python-dotenv not installed")
        print("  Install with: pip install python-dotenv")
        print("  Using system environment variables only")
        return False


def check_required_env_vars() -> bool:
    """
    Check if required environment variables are set.
    
    Returns:
        True if all required variables are set, False otherwise
    """
    required_vars = {
        "OPENAI_API_KEY": "OpenAI API key for embeddings and chat"
    }
    
    optional_vars = {
        "LLAMA_CLOUD_API_KEY": "LlamaParse API key for enhanced PDF parsing"
    }
    
    all_set = True
    
    print("\nChecking environment variables:")
    print("-" * 60)
    
    # Check required
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            print(f"✓ {var}: {'*' * 8}{value[-4:]} ({description})")
        else:
            print(f"✗ {var}: NOT SET ({description})")
            all_set = False
    
    # Check optional
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value:
            print(f"✓ {var}: {'*' * 8}{value[-4:]} ({description})")
        else:
            print(f"○ {var}: NOT SET (optional - {description})")
    
    print("-" * 60)
    
    return all_set


def get_env_value(key: str, default: str = "") -> str:
    """
    Get environment variable value with fallback.
    
    Args:
        key: Environment variable name
        default: Default value if not set
    
    Returns:
        Environment variable value or default
    """
    return os.getenv(key, default)


def set_env_value(key: str, value: str) -> None:
    """
    Set environment variable for current session.
    
    Args:
        key: Environment variable name
        value: Value to set
    """
    os.environ[key] = value


def create_env_file_from_template() -> None:
    """Create .env file from .env.example template."""
    current_dir = Path(__file__).parent
    template_path = current_dir / '.env.example'
    env_path = current_dir / '.env'
    
    if env_path.exists():
        print(f"⚠ .env file already exists at: {env_path}")
        response = input("Overwrite? (y/N): ").strip().lower()
        if response != 'y':
            print("Cancelled.")
            return
    
    if template_path.exists():
        # Copy template to .env
        with open(template_path, 'r') as f:
            template_content = f.read()
        
        with open(env_path, 'w') as f:
            f.write(template_content)
        
        print(f"✓ Created .env file at: {env_path}")
        print("  Please edit it and add your API keys")
    else:
        print(f"✗ Template file not found: {template_path}")


def print_env_help() -> None:
    """Print help information about environment variables."""
    print("""
╔════════════════════════════════════════════════════════════════╗
║                    FinRAG Environment Variables                ║
╚════════════════════════════════════════════════════════════════╝

Required:
  OPENAI_API_KEY          OpenAI API key for embeddings and chat
                          Get it: https://platform.openai.com/api-keys

Recommended:
  LLAMA_CLOUD_API_KEY     LlamaParse API key for PDF parsing
                          Get it: https://cloud.llamaindex.ai/

Optional Configuration:
  FINRAG_CHUNK_SIZE       Chunk size in tokens (default: 512)
  FINRAG_CHUNK_OVERLAP    Overlap between chunks (default: 50)
  FINRAG_TOP_K            Number of docs to retrieve (default: 10)
  FINRAG_TREE_DEPTH       RAPTOR tree depth (default: 3)
  FINRAG_TRAVERSAL_METHOD Retrieval method (default: tree_traversal)
  
  FINRAG_USE_LLAMAPARSE   Enable LlamaParse (default: true)
  FINRAG_LLAMAPARSE_MODE  Parsing mode (default: parse_page_with_llm)
  FINRAG_LLAMAPARSE_WORKERS Number of workers (default: 4)
  
  FINRAG_EMBEDDING_MODEL  Embedding model (default: text-embedding-3-small)
  FINRAG_LLM_MODEL        Chat model (default: gpt-4-turbo-preview)

Setup:
  1. Copy .env.example to .env
  2. Edit .env and add your API keys
  3. Run your script - variables load automatically

PowerShell Example:
  $env:OPENAI_API_KEY="sk-..."
  $env:LLAMA_CLOUD_API_KEY="llx-..."
  python example.py

Or use .env file (recommended for persistent setup)
""")


if __name__ == "__main__":
    """Test environment variable loading."""
    print("Testing environment variable loading...")
    print("=" * 60)
    
    # Try to load .env
    load_env_file()
    
    # Check required variables
    all_set = check_required_env_vars()
    
    if not all_set:
        print("\n⚠ Some required environment variables are missing")
        print("\nRun this to see setup instructions:")
        print("  python -c \"from env_loader import print_env_help; print_env_help()\"")
    else:
        print("\n✓ All required environment variables are set!")
        print("  You're ready to use FinRAG")
