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
        Financial Capital

TCS' success is a testament to its robust business model and its ability to perpetually adapt in a constantly changing technology environment, ensuring it remains relevant to customers while delivering value to all stakeholders.

- Superior profitability, providing the financial strength to invest in new capabilities, Research &#x26; Innovation, navigating economic downturns and changing technology waves
- Prudent use of working capital and cash flow management, resulting in robust cash conversion and increased invested funds
- A strong balance sheet with zero debt, further strengthening return ratios
- Consistently high shareholder returns

# TCS Value Creation and Distribution (FY 2021 - 25)¹

# Revenue Trend

CAGR 10.2% In FY 2025, TCS achieved a year-over-year revenue growth of 6.0%, demonstrating a resilient business performance in this uncertain environment.

| FY        | 2021    | 2022    | 2023    | 2024    | 2025    |
| --------- | ------- | ------- | ------- | ------- | ------- |
| (₹ crore) | 164,177 | 191,754 | 225,458 | 240,893 | 255,324 |

On a constant currency basis, revenue grew by 4.2%, outpacing the growth in FY 2024.

Over the past five financial years, the company recorded a compound annual growth rate (CAGR) of 10.2%, highlighting the resilience and scalability of its business model.

# Operating Profit Trend

In FY 2025, TCS reported an operating margin of 24.3%, a marginal decline of 30 basis points compared to FY 2024.

This moderation was primarily attributable to the impact of annual wage hikes, associates promotions, and strategic investments in infrastructure and capability development.

| FY                         | 2021\* | 2022   | 2023   | 2024\* | 2025   |
| -------------------------- | ------ | ------ | ------ | ------ | ------ |
| Operating Profit (₹ crore) | 42,481 | 48,453 | 54,237 | 59,311 | 62,165 |
| Operating Margin           | 25.9%  | 25.3%  | 24.1%  | 24.6%  | 24.3%  |

These cost pressures were partially offset by improvements in workforce utilization, productivity, and realization, along with favourable currency movements.

¹GRI 201-1 *Excludes provision (in FY 2021) and settlement (in FY 2024) of legal claim

Integrated Annual Report 2024-25

---

Financial Capital

# Earnings Per Share

CAGR 9.3% TCS has consistently grown its Earnings Per Share (EPS), achieving a CAGR of 9.3% over the past five financial years. This steady increase highlights the company’s growing earnings and its commitment to delivering long-term value to shareholders.

| FY            | 2021\* | 2022   | 2023   | 2024\* | 2025   |
| ------------- | ------ | ------ | ------ | ------ | ------ |
| (Amount in ₹) | 89.27  | 103.62 | 115.19 | 127.74 | 134.19 |

# Operating Cash Flow and Cash Conversion

116.2% TCS maintained an excellent cash conversion ratio exceeding 100%, highlighting its robust financial health and strong ability to generate cash from operations. This efficiency in translating profits to cash flows enables TCS to meet financial obligations and fund growth initiatives without relying on external financing.

| FY                        | 2021\* | 2022   | 2023   | 2024\* | 2025   |
| ------------------------- | ------ | ------ | ------ | ------ | ------ |
| (₹ crore)                 | 38,802 | 39,949 | 41,965 | 45,097 | 48,908 |
| Operating Cash Flow (OCF) |        |        |        |        |        |
| OCF to Net Profit Ratio   | 116.2% | 104.2% | 99.6%  | 100.7% | 96.8%  |

# Shareholder Payouts

101.5% TCS has a practice of returning substantial free cash flow to shareholders and based on the company's performance, the Board of Directors have declared three interim dividends of ₹10 each, a special dividend of ₹66, and recommended a final dividend of ₹30 (pending shareholders' approval at this AGM), for a total dividend of ₹126 per share for FY 2025. TCS has consistently declared dividend every quarter since its listing, complemented by three bonus issues and five buyback offers.

| FY                       | 2021\* | 2022   | 2023   | 2024\* | 2025   |
| ------------------------ | ------ | ------ | ------ | ------ | ------ |
| (₹ crore)                | 33,873 | 38,010 | 42,079 | 47,445 | 45,588 |
| Shareholder Payout       |        |        |        |        |        |
| Shareholder Payout ratio | 101.5% | 99.2%  | 99.8%  | 101.8% | 93.9%  |

# ~~Return on Equity~~

TCS’ high and improving Return on Equity reflects the company’s ability to generate strong profitability and manage resources efficiently. This highlights the company’s financial discipline and operational rigor, as well as its judicious use of shareholder capital.

| FY | 2021\* | 2022  | 2023  | 2024\* | 2025  |
| -- | ------ | ----- | ----- | ------ | ----- |
|    | 38.9%  | 43.4% | 46.9% | 51.3%  | 52.2% |

*Excludes provision (in FY 2021) and settlement (in FY 2024) of legal claim

Integrated Annual Report 2024-25
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
