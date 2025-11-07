"""
Configuration settings for FinRAG implementation.
"""
import os
from dataclasses import dataclass, field
from typing import Optional, List
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    # Look for .env file in the same directory as this config file
    env_path = Path(__file__).parent / '.env'
    load_dotenv(dotenv_path=env_path)
except ImportError:
    print("Warning: python-dotenv not installed. Using system environment variables only.")
    print("Install with: pip install python-dotenv")

@dataclass
class FinRAGConfig:
    """Configuration for FinRAG system."""
    
    # API Keys
    openai_api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    llamaparse_api_key: str = field(default_factory=lambda: os.getenv("LLAMA_CLOUD_API_KEY", ""))
    
    # Model configurations
    embedding_model: str = field(default_factory=lambda: os.getenv("FINRAG_EMBEDDING_MODEL", "text-embedding-3-small"))
    llm_model: str = field(default_factory=lambda: os.getenv("FINRAG_LLM_MODEL", "gpt-4-turbo-preview"))
    summarization_model: str = field(default_factory=lambda: os.getenv("FINRAG_SUMMARIZATION_MODEL", "gpt-3.5-turbo"))  # Changed to faster model
    
    # Chunking parameters
    chunk_size: int = field(default_factory=lambda: int(os.getenv("FINRAG_CHUNK_SIZE", "512")))
    chunk_overlap: int = field(default_factory=lambda: int(os.getenv("FINRAG_CHUNK_OVERLAP", "50")))
    
    # RAPTOR tree parameters
    max_cluster_size: int = field(default_factory=lambda: int(os.getenv("FINRAG_MAX_CLUSTER_SIZE", "100")))
    min_cluster_size: int = field(default_factory=lambda: int(os.getenv("FINRAG_MIN_CLUSTER_SIZE", "5")))
    summarization_length: int = field(default_factory=lambda: int(os.getenv("FINRAG_SUMMARIZATION_LENGTH", "200")))
    tree_depth: int = field(default_factory=lambda: int(os.getenv("FINRAG_TREE_DEPTH", "3")))
    
    # Metadata clustering (FinRAG paper feature)
    use_metadata_clustering: bool = field(default_factory=lambda: os.getenv("FINRAG_USE_METADATA_CLUSTERING", "true").lower() == "true")
    metadata_keys: List[str] = field(default_factory=lambda: ["sector", "company", "year"])
    
    # Retrieval parameters
    top_k: int = field(default_factory=lambda: int(os.getenv("FINRAG_TOP_K", "10")))
    similarity_threshold: float = field(default_factory=lambda: float(os.getenv("FINRAG_SIMILARITY_THRESHOLD", "0.7")))
    
    # Financial domain specific
    extract_tables: bool = True
    extract_financial_entities: bool = True
    entity_types: List[str] = field(default_factory=lambda: [
        "MONEY", "PERCENT", "DATE", "ORG", "PRODUCT", "LAW"
    ])
    
    # PDF Parsing configuration
    use_llamaparse: bool = field(default_factory=lambda: os.getenv("FINRAG_USE_LLAMAPARSE", "true").lower() == "true")
    llamaparse_mode: str = field(default_factory=lambda: os.getenv("FINRAG_LLAMAPARSE_MODE", "parse_page_with_llm"))
    llamaparse_num_workers: int = field(default_factory=lambda: int(os.getenv("FINRAG_LLAMAPARSE_WORKERS", "4")))
    llamaparse_language: str = field(default_factory=lambda: os.getenv("FINRAG_LLAMAPARSE_LANGUAGE", "en"))
    
    # Tree traversal method
    traversal_method: str = field(default_factory=lambda: os.getenv("FINRAG_TRAVERSAL_METHOD", "tree_traversal"))
    
    # Cache settings
    use_cache: bool = field(default_factory=lambda: os.getenv("FINRAG_USE_CACHE", "true").lower() == "true")
    cache_dir: str = field(default_factory=lambda: os.getenv("FINRAG_CACHE_DIR", "./cache"))
    
    def __post_init__(self):
        """Validate configuration."""
        if not self.openai_api_key:
            raise ValueError("OpenAI API key must be provided")
        
        os.makedirs(self.cache_dir, exist_ok=True)
