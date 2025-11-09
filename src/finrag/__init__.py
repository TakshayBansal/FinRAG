"""
FinRAG: Financial Retrieval-Augmented Generation System
Based on RAPTOR (Recursive Abstractive Processing for Tree-Organized Retrieval)
"""

from .finrag import FinRAG
from .config import FinRAGConfig
from .scoring import EnsembleScorer, ScoringConfig, ScoringResult

__version__ = "1.0.0"
__all__ = ["FinRAG", "FinRAGConfig", "EnsembleScorer", "ScoringConfig", "ScoringResult"]
