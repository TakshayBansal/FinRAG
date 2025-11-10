"""
Main FinRAG implementation combining all components.
"""
from typing import List, Dict, Any, Optional
import numpy as np
from pathlib import Path
import PyPDF2
import os

from .config import FinRAGConfig
from .models import (
    OpenAIEmbeddingModel,
    OpenAISummarizationModel,
    OpenAIQAModel,
    FinancialChunker
)
from .models.fallback_models import (
    SentenceTransformerEmbeddingModel,
    FlanT5SummarizationModel,
    FlanT5QAModel,
    check_openai_key_valid
)
from .core.tree import RAPTORTree, TreeConfig
from .core.retrieval import RAPTORRetriever
from .utils.filtered_parser import FilteredDocumentParser


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
        
        # Check if OpenAI API key is available and valid
        has_openai = check_openai_key_valid(self.config.openai_api_key)
        
        if not has_openai:
            print("\n" + "="*60)
            print("⚠️  OpenAI API Key Not Available")
            print("="*60)
            print("Using FREE open-source AI models:")
            print("  • Embeddings: sentence-transformers (all-MiniLM-L6-v2)")
            print("  • Summarization: FLAN-T5-small (Google)")
            print("  • QA: FLAN-T5-small (Google)")
            print("\nThese are actual AI models - not just keyword matching!")
            print("Quality: ~60-70% of OpenAI models")
            print("\nFor best results, set OPENAI_API_KEY:")
            print("  Windows: $env:OPENAI_API_KEY='sk-...'")
            print("  Linux/Mac: export OPENAI_API_KEY='sk-...'")
            print("="*60 + "\n")
        
        # Initialize models with fallback
        if has_openai:
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
        else:
            # Use fallback models (free, open-source AI)
            self.embedding_model = SentenceTransformerEmbeddingModel(
                model="all-MiniLM-L6-v2"
            )
            
            self.summarization_model = FlanT5SummarizationModel(
                model_name="google/flan-t5-small"
            )
            
            self.qa_model = FlanT5QAModel(
                model_name="google/flan-t5-small"
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
            config=tree_config,
            use_metadata_clustering=self.config.use_metadata_clustering
        )
        
        self.retriever = None
    
    def load_pdf(
        self, 
        pdf_path: str, 
        use_llamaparse: bool = None,
        use_filtering: bool = None,
        sections_to_extract: Optional[List[str]] = None
    ) -> str:
        """
        Load text from a PDF file using LlamaParse (preferred) or PyPDF2 (fallback).
        
        Args:
            pdf_path: Path to PDF file
            use_llamaparse: Override config to force LlamaParse usage (None = use config)
            use_filtering: Whether to use filtered parsing (None = use config)
            sections_to_extract: Specific sections to extract (None = all default sections)
        
        Returns:
            Extracted text (filtered if enabled, markdown/plain text otherwise)
        """
        # Determine which parser to use
        if use_llamaparse is None:
            use_llamaparse = self.config.use_llamaparse
        
        if use_filtering is None:
            use_filtering = getattr(self.config, 'use_filtered_parsing', False)
        
        # Try LlamaParse first if enabled and API key is available
        if use_llamaparse and self.config.llamaparse_api_key:
            try:
                from llama_cloud_services import LlamaParse
                
                # Use filtered parsing if enabled
                if use_filtering:
                    print(f"  Using LlamaParse with intelligent filtering...")
                    
                    # Initialize filtered parser
                    filtered_parser = FilteredDocumentParser(
                        sections_to_extract=sections_to_extract
                    )
                    
                    # Generate system prompt for section extraction
                    system_prompt = filtered_parser.generate_system_prompt()
                    
                    # Parse with custom prompt
                    parser = LlamaParse(
                        api_key=self.config.llamaparse_api_key,
                        num_workers=10,
                        verbose=False,
                        target_pages = "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50",
                        parse_mode="parse_document_with_llm",  # Use LLM mode for filtering
                        language=self.config.llamaparse_language,
                        system_prompt=system_prompt
                    )
                    
                    result = parser.parse(pdf_path)
                    raw_markdown = result.get_markdown()
                    
                    # Consolidate and filter sections
                    consolidated_data = filtered_parser.consolidate_sections(raw_markdown)
                    
                    # Get statistics
                    stats = filtered_parser.get_statistics(consolidated_data)
                    print(f"  ✓ Filtered parsing complete:")
                    print(f"    - Sections extracted: {stats['total_sections']}")
                    print(f"    - Total items: {stats['total_items']}")
                    print(f"    - Coverage: {stats['coverage']:.1f}%")
                    
                    # Convert to text format for embedding
                    text = filtered_parser.convert_to_text(consolidated_data)
                    
                    # Optionally save outputs for debugging
                    if hasattr(self.config, 'save_filtered_outputs') and self.config.save_filtered_outputs:
                        output_dir = Path(pdf_path).parent / "filtered_outputs"
                        base_name = Path(pdf_path).stem
                        saved_files = filtered_parser.save_outputs(
                            consolidated_data, 
                            str(output_dir),
                            base_name
                        )
                        print(f"    - Saved filtered outputs to: {output_dir}")
                    
                    print(f"  ✓ Final filtered text: {len(text)} chars (reduced from {len(raw_markdown)})")
                    return text
                
                else:
                    # Standard LlamaParse without filtering
                    print(f"  Using LlamaParse for high-quality extraction...")
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
            # Use metadata extraction if metadata clustering is enabled
            if self.config.use_metadata_clustering:
                chunks = self.chunker.chunk_text_with_metadata(doc)
            else:
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
