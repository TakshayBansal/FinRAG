"""
Simple example demonstrating FinRAG usage.
API keys are loaded from .env file automatically.
"""
import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Load environment variables from .env file
from finrag.utils import load_env_file, check_required_env_vars
load_env_file()

from finrag import FinRAGConfig, FinRAG


def simple_example():
    """Simple example with sample financial data."""
    
    # Check API keys (loaded from .env file automatically)
    if not check_required_env_vars():
        print("\n" + "="*60)
        print("ERROR: Required environment variables not set")
        print("="*60)
        print("\nPlease either:")
        print("  1. Add keys to .env file (recommended)")
        print("  2. Set environment variables manually")
        print("\nTo setup .env file:")
        print("  1. Copy .env.example to .env")
        print("  2. Edit .env and add your API keys")
        print("  3. Run this script again")
        return
    
    print("="*80)
    print("FinRAG Simple Example")
    print("="*80)
    
    # Create sample financial documents
    sample_documents = [
        """
        Tech Corp Inc. - Q4 2024 Financial Results
        
        Financial Highlights:
        - Total Revenue: $500 million (up 35% year-over-year)
        - Net Income: $125 million (up 40% year-over-year)
        - Operating Margin: 25% (improved from 22% in Q4 2023)
        - Earnings Per Share: $3.50 (up from $2.50 in Q4 2023)
        - Cash and Cash Equivalents: $800 million
        
        Business Segment Performance:
        
        Cloud Services: Revenue of $300M (up 45% YoY)
        - Strong adoption of our new AI-powered analytics platform
        - Added 500 new enterprise customers
        - Renewal rate of 95%
        
        Software Products: Revenue of $150M (up 25% YoY)
        - Successful launch of version 5.0
        - Expanded into healthcare and finance verticals
        
        Professional Services: Revenue of $50M (up 15% YoY)
        - Increased consulting engagements
        - Higher average deal sizes
        """,
        
        """
        Risk Factors and Challenges:
        
        1. Market Competition
        - Facing increased competition from established cloud providers
        - Price pressure in the software market
        - Need to continuously innovate to maintain market share
        
        2. Cybersecurity Risks
        - Growing threat landscape
        - Invested $50M in security infrastructure
        - Implemented zero-trust architecture
        
        3. Regulatory Environment
        - New data privacy regulations in Europe and Asia
        - Compliance costs estimated at $20M annually
        - Working with regulators to ensure compliance
        
        4. Talent Acquisition and Retention
        - Competitive market for AI/ML engineers
        - Increased employee benefits budget by 15%
        - Stock-based compensation remains competitive
        
        5. Economic Uncertainty
        - Potential recession could impact customer spending
        - Foreign exchange headwinds in key markets
        - Monitoring macro trends closely
        """,
        
        """
        Future Outlook and Strategy - 2025 Guidance
        
        Revenue Projections:
        - Q1 2025: $520-540M (4-8% growth)
        - Full Year 2025: $2.2-2.3B (10-15% growth)
        
        Strategic Priorities:
        
        1. AI and Machine Learning Expansion
        - Investing $200M in AI research and development
        - Building new generative AI capabilities
        - Target: Launch 3 new AI-powered products by Q3 2025
        
        2. Geographic Expansion
        - Opening offices in Singapore, Dubai, and São Paulo
        - Targeting 30% of revenue from international markets by end of 2025
        - Currently at 20% international revenue
        
        3. Strategic Acquisitions
        - Allocated $300M for M&A activity
        - Focusing on cybersecurity and data analytics companies
        - Completed due diligence on 2 potential targets
        
        4. Operational Efficiency
        - Implementing automation to reduce costs
        - Target: Improve operating margin to 28% by Q4 2025
        - Streamlining sales and marketing operations
        
        5. Customer Success Initiatives
        - Expanding customer support team by 40%
        - Launching new training and certification programs
        - Goal: Achieve Net Promoter Score of 70+
        
        Capital Allocation:
        - R&D: 25% of revenue
        - Sales & Marketing: 35% of revenue
        - G&A: 15% of revenue
        - Share buyback program: $100M authorized
        """
    ]
    
    # Initialize FinRAG (config loads from .env automatically)
    print("\n1. Initializing FinRAG system...")
    config = FinRAGConfig(
        chunk_size=400,
        chunk_overlap=50,
        top_k=8,
        tree_depth=2,
        traversal_method="tree_traversal"
    )
    finrag = FinRAG(config)
    
    # Build the tree
    print("\n2. Building RAPTOR tree from sample documents...")
    finrag.add_documents(sample_documents)
    
    # Show statistics
    print("\n3. Tree Statistics:")
    stats = finrag.get_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Example queries
    print("\n4. Running Example Queries")
    print("="*80)
    
    queries = [
        "What is the estimated future trend of the stock based on this data? Give the direction along with confidence score(out of 100)."
    ]
    
    for i, question in enumerate(queries, 1):
        print(f"\n[Query {i}] {question}")
        print("-"*80)
        
        result = finrag.query(question, top_k=5)
        
        print(f"\n{result['answer']}")
        print(f"\n(Retrieved {len(result['retrieved_nodes'])} nodes, "
              f"Method: {result['retrieval_method']})")
        print()
    
    # Save the system
    print("\n5. Saving FinRAG system...")
    save_path = "./finrag_example_index"
    finrag.save(save_path)
    print(f"   Saved to: {save_path}")
    
    # Test loading
    print("\n6. Testing reload functionality...")
    finrag_reloaded = FinRAG(config)
    finrag_reloaded.load(save_path)
    test_result = finrag_reloaded.query("What is the operating margin?")
    print(f"   Test query result: {test_result['answer'][:100]}...")
    
    print("\n" + "="*80)
    print("Example completed successfully!")
    print("="*80)


if __name__ == "__main__":
    simple_example()
