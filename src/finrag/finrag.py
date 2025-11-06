"""
Main FinRAG implementation combining all components.
"""
from typing import List, Dict, Any, Optional
import numpy as np
from pathlib import Path
import PyPDF2

from .config import FinRAGConfig
from .models import (
    OpenAIEmbeddingModel,
    OpenAISummarizationModel,
    OpenAIQAModel,
    FinancialChunker
)
from .core.tree import RAPTORTree, TreeConfig
from .core.retrieval import RAPTORRetriever


class FinRAG:
    """
    Main FinRAG class implementing retrieval-augmented generation
    with RAPTOR-style hierarchical indexing for financial documents.
    """
    
    def __init__(self, config: FinRAGConfig = None):
        """
        Initialize FinRAG system.
        
        Args:
            config: FinRAG configuration
        """
        self.config = config or FinRAGConfig()
        
        # Initialize models
        self.embedding_model = OpenAIEmbeddingModel(
            model=self.config.embedding_model,
            api_key=self.config.openai_api_key
        )
        
        self.summarization_model = OpenAISummarizationModel(
            model=self.config.summarization_model,
            api_key=self.config.openai_api_key
        )
        
        self.qa_model = OpenAIQAModel(
            model=self.config.llm_model,
            api_key=self.config.openai_api_key
        )
        
        self.chunker = FinancialChunker(
            chunk_size=self.config.chunk_size,
            chunk_overlap=self.config.chunk_overlap
        )
        
        # Initialize tree
        tree_config = TreeConfig(
            max_depth=self.config.tree_depth,
            max_cluster_size=self.config.max_cluster_size,
            min_cluster_size=self.config.min_cluster_size,
            summarization_length=self.config.summarization_length
        )
        
        self.tree = RAPTORTree(
            embedding_model=self.embedding_model,
            summarization_model=self.summarization_model,
            config=tree_config
        )
        
        self.retriever = None
    
    def load_pdf(self, pdf_path: str, use_llamaparse: bool = None) -> str:
        """
        Load text from a PDF file using LlamaParse (preferred) or PyPDF2 (fallback).
        
        Args:
            pdf_path: Path to PDF file
            use_llamaparse: Override config to force LlamaParse usage (None = use config)
        
        Returns:
            Extracted text (markdown format if LlamaParse, plain text if PyPDF2)
        """
        # Determine which parser to use
        if use_llamaparse is None:
            use_llamaparse = self.config.use_llamaparse
        
        # Try LlamaParse first if enabled and API key is available
        if use_llamaparse and self.config.llamaparse_api_key:
            try:
                print(f"  Using LlamaParse for high-quality extraction...")
                from llama_cloud_services import LlamaParse
                
                parser = LlamaParse(
                    api_key=self.config.llamaparse_api_key,
                    num_workers=self.config.llamaparse_num_workers,
                    verbose=False,
                    parse_mode=self.config.llamaparse_mode,
                    language=self.config.llamaparse_language
                )
                
                result = parser.parse(pdf_path)
                text = result.get_markdown()
                print(f"  ✓ Successfully parsed with LlamaParse ({len(text)} chars)")
                return text
                
            except ImportError:
                print("  ⚠ LlamaParse not installed, falling back to PyPDF2")
                print("  Install with: pip install llama-parse llama-cloud-services")
            except Exception as e:
                print(f"  ⚠ LlamaParse failed ({str(e)}), falling back to PyPDF2")
        
        # Fallback to PyPDF2
        print(f"  Using PyPDF2 for basic text extraction...")
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            print(f"  ✓ Successfully parsed with PyPDF2 ({len(text)} chars)")
        except Exception as e:
            print(f"  ✗ PyPDF2 failed: {str(e)}")
            raise
        
        return text
    
    def load_text(self, text_path: str) -> str:
        """
        Load text from a text file.
        
        Args:
            text_path: Path to text file
        
        Returns:
            File content
        """
        with open(text_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def add_documents(self, documents: List[str]) -> None:
        """
        Add documents to the RAPTOR tree.
        
        Args:
            documents: List of document texts
        """
        print("Chunking documents...")
        all_chunks = []
        for doc in documents:
            chunks = self.chunker.chunk_text(doc)
            all_chunks.extend(chunks)
        
        print(f"Created {len(all_chunks)} chunks")
        
        print("Creating embeddings...")
        # Create embeddings in batches
        batch_size = 100
        embeddings_list = []
        
        for i in range(0, len(all_chunks), batch_size):
            batch = all_chunks[i:i+batch_size]
            batch_texts = [chunk["text"] for chunk in batch]
            batch_embeddings = self.embedding_model.create_embeddings(batch_texts)
            embeddings_list.append(batch_embeddings)
        
        embeddings = np.vstack(embeddings_list)
        print(f"Created {len(embeddings)} embeddings")
        
        print("Building RAPTOR tree...")
        self.tree.build_tree(all_chunks, embeddings)
        
        print("Initializing retriever...")
        self.retriever = RAPTORRetriever(
            tree=self.tree,
            embedding_model=self.embedding_model,
            top_k=self.config.top_k
        )
        
        print("FinRAG system ready!")
    
    def query(
        self,
        question: str,
        retrieval_method: str = None,
        top_k: int = None
    ) -> Dict[str, Any]:
        """
        Query the FinRAG system.
        
        Args:
            question: Question to answer
            retrieval_method: Retrieval method to use
            top_k: Number of documents to retrieve
        
        Returns:
            Dictionary containing answer and metadata
        """
        if self.retriever is None:
            raise RuntimeError("No documents added. Call add_documents() first.")
        
        if retrieval_method is None:
            retrieval_method = self.config.traversal_method
        
        if top_k is None:
            top_k = self.config.top_k
        
        # Retrieve relevant context
        print(f"Retrieving relevant documents using {retrieval_method}...")
        context = self.retriever.retrieve_with_context(
            question,
            method=retrieval_method,
            k=top_k
        )
        
        # Answer question
        print("Generating answer...")
        result = self.qa_model.answer_question(context, question)
        
        # Add retrieval metadata
        retrieved_nodes = self.retriever.retrieve(question, retrieval_method, top_k)
        result["retrieved_nodes"] = [
            {
                "node_id": node.node_id,
                "level": node.level,
                "score": float(score),
                "text_preview": node.text[:200] + "..." if len(node.text) > 200 else node.text
            }
            for node, score in retrieved_nodes
        ]
        result["retrieval_method"] = retrieval_method
        
        return result
    
    def save(self, path: str) -> None:
        """
        Save the FinRAG system to disk.
        
        Args:
            path: Directory path to save to
        """
        save_path = Path(path)
        save_path.mkdir(parents=True, exist_ok=True)
        
        # Save tree
        self.tree.save(path)
        
        print(f"FinRAG system saved to {path}")
    
    def load(self, path: str) -> None:
        """
        Load a saved FinRAG system from disk.
        
        Args:
            path: Directory path to load from
        """
        # Load tree
        self.tree = RAPTORTree.load(
            path,
            self.embedding_model,
            self.summarization_model
        )
        
        # Initialize retriever
        self.retriever = RAPTORRetriever(
            tree=self.tree,
            embedding_model=self.embedding_model,
            top_k=self.config.top_k
        )
        
        print(f"FinRAG system loaded from {path}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the current tree.
        
        Returns:
            Dictionary of statistics
        """
        if not self.tree.all_nodes:
            return {"message": "No documents added yet"}
        
        levels = {}
        for node in self.tree.all_nodes.values():
            levels[node.level] = levels.get(node.level, 0) + 1
        
        return {
            "total_nodes": len(self.tree.all_nodes),
            "leaf_nodes": len(self.tree.leaf_nodes),
            "root_nodes": len(self.tree.root_nodes),
            "levels": levels,
            "tree_depth": max(levels.keys()) if levels else 0
        }
