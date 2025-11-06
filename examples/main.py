"""
Main entry point for FinRAG system with example usage.
"""
import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Load environment variables from .env file
from finrag.utils import load_env_file
load_env_file()

from finrag import FinRAGConfig, FinRAG


def main():
    """Main function demonstrating FinRAG usage."""
    
    # API keys are loaded from .env file automatically
    # Or you can override them here if needed
    
    # Initialize config (reads from environment variables and .env file)
    config = FinRAGConfig()
    
    # Or override specific values:
    # config = FinRAGConfig(
    #     openai_api_key="your-key",  # Override .env value
    #     chunk_size=1024,            # Override default
    # )
    
    # Initialize FinRAG
    print("Initializing FinRAG system...")
    finrag = FinRAG(config)
    
    # Example 1: Load and process a financial document
    pdf_path = Path(__file__).parent / "256911814.pdf"
    
    if pdf_path.exists():
        print(f"\nLoading PDF: {pdf_path}")
        text = finrag.load_pdf(str(pdf_path))
        print(f"Loaded {len(text)} characters")
        
        # Add document to FinRAG
        print("\nProcessing document and building RAPTOR tree...")
        finrag.add_documents([text])
        
        # Print statistics
        stats = finrag.get_statistics()
        print("\nTree Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        # Example queries
        questions = [
            "What are the main financial highlights?",
            "What is the revenue growth rate?",
            "What are the key risk factors mentioned?",
        ]
        
        print("\n" + "="*80)
        print("QUERYING THE SYSTEM")
        print("="*80)
        
        for question in questions:
            print(f"\nQuestion: {question}")
            print("-" * 80)
            
            result = finrag.query(question)
            
            print(f"Answer:\n{result['answer']}")
            print(f"\nRetrieved {len(result['retrieved_nodes'])} relevant nodes")
            print(f"Retrieval method: {result['retrieval_method']}")
            
            # Show top 3 retrieved nodes
            print("\nTop retrieved nodes:")
            for i, node_info in enumerate(result['retrieved_nodes'][:3], 1):
                print(f"  {i}. Level {node_info['level']} "
                      f"(score: {node_info['score']:.3f})")
                print(f"     {node_info['text_preview']}")
            
            print()
        
        # Save the system
        save_path = "./finrag_index"
        print(f"\nSaving FinRAG system to {save_path}...")
        finrag.save(save_path)
        
        # Example: Load the saved system
        print(f"\nLoading FinRAG system from {save_path}...")
        finrag_loaded = FinRAG(config)
        finrag_loaded.load(save_path)
        
        # Test loaded system
        print("\nTesting loaded system...")
        test_question = "Summarize the financial performance"
        result = finrag_loaded.query(test_question)
        print(f"Question: {test_question}")
        print(f"Answer: {result['answer'][:200]}...")
        
    else:
        print(f"PDF file not found: {pdf_path}")
        print("\nExample usage without PDF:")
        print("="*80)
        
        # Example with text documents
        sample_docs = [
            """
            Company XYZ Financial Report Q4 2024
            
            Revenue: $150M (up 25% YoY)
            Net Income: $45M (up 30% YoY)
            Operating Margin: 30%
            
            Key Highlights:
            - Strong growth in cloud services segment
            - Successful product launch in Asian markets
            - Improved operational efficiency
            """,
            """
            Risk Factors:
            
            1. Market Competition: Intense competition from established players
            2. Regulatory Changes: Potential new regulations in key markets
            3. Currency Fluctuations: Exposure to foreign exchange risk
            4. Technology Disruption: Rapid changes in technology landscape
            """,
            """
            Future Outlook:
            
            The company expects continued growth in 2025 with projected revenue
            of $180-200M. Key focus areas include:
            - Expansion into new geographic markets
            - Investment in R&D for next-generation products
            - Strategic acquisitions to enhance market position
            """
        ]
        
        print("Processing sample financial documents...")
        finrag.add_documents(sample_docs)
        
        stats = finrag.get_statistics()
        print("\nTree Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        # Query the system
        question = "What is the revenue and growth rate?"
        print(f"\nQuestion: {question}")
        result = finrag.query(question)
        print(f"Answer: {result['answer']}")


if __name__ == "__main__":
    main()
