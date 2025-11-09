"""
Example: Stock Prediction Scoring with Ensemble Method

This example demonstrates how to use the EnsembleScorer to generate
comprehensive stock prediction scores by combining:
1. Annual report analysis (RAG)
2. Financial ratios from yfinance
3. Multiple scoring methods (sentiment, trends, quantitative, etc.)
"""
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from finrag import FinRAG, FinRAGConfig
from finrag.scoring import EnsembleScorer, ScoringConfig
from finrag.utils import load_env_file

# Load environment variables
load_env_file()


def main():
    """Main function demonstrating stock scoring."""
    
    print("="*80)
    print("STOCK PREDICTION SCORING - ENSEMBLE METHOD")
    print("="*80)
    
    # ========================================
    # STEP 1: Initialize FinRAG and Load Pre-built Tree
    # ========================================
    print("\n📚 Step 1: Initializing FinRAG system...")
    
    config = FinRAGConfig()
    config.use_filtered_parsing = True  # Use intelligent filtering
    config.use_metadata_clustering = True  # Use fixed hierarchical structure
    
    finrag = FinRAG(config=config)
    print("   ✓ FinRAG initialized")
    
    # ========================================
    # STEP 2: Load Pre-built Tree (from all PDFs)
    # ========================================
    print("\n📄 Step 2: Loading pre-built tree...")
    
    # Load tree built from all PDFs in data folder
    tree_path = Path(__file__).parent.parent / "finrag_tree"
    
    if tree_path.exists():
        print(f"   Loading tree from: {tree_path}")
        finrag.load(str(tree_path))
        
        stats = finrag.get_statistics()
        print(f"   ✓ Tree loaded with {stats['total_nodes']} nodes")
        print(f"   ✓ Documents from data folder already indexed")
        
    else:
        print(f"   ❌ Tree not found at: {tree_path}")
        print("\n   Please build the tree first by running:")
        print("     python scripts/build_tree.py")
        print("\n   This will process all PDFs in data folder and create a reusable tree.")
        return
    
    # ========================================
    # STEP 3: Initialize Ensemble Scorer
    # ========================================
    print("\n🎯 Step 3: Initializing Ensemble Scorer...")
    
    # Use default configuration or customize
    scoring_config = ScoringConfig()
    
    # Optional: Customize weights
    # scoring_config.sentiment_weight = 0.30
    # scoring_config.quantitative_weight = 0.25
    
    scorer = EnsembleScorer(config=scoring_config)
    print("   ✓ Ensemble scorer initialized")
    
    # ========================================
    # STEP 4: Generate Stock Prediction Score
    # ========================================
    print("\n💹 Step 4: Generating stock prediction score...")
    print("\nThis will:")
    print("  1. Fetch financial data from yfinance")
    print("  2. Analyze sentiment from annual report")
    print("  3. Calculate year-over-year trends")
    print("  4. Generate risk-adjusted score")
    print("  5. Score quantitative metrics")
    print("  6. Get LLM judge assessment")
    print("  7. Combine all methods into ensemble score\n")
    
    # Example companies (customize for your use case)
    # For Indian stocks, use .NS (NSE) or .BO (BSE) suffix
    examples = [
        {
            "ticker": "WIPRO.NS",
            "company_name": "Wipro",
            "suffix": ""  # US stocks don't need suffix
        },
        # Uncomment for Indian stocks:
        # {
        #     "ticker": "TCS",
        #     "company_name": "Tata Consultancy Services",
        #     "suffix": ".NS"  # NSE
        # },
        # {
        #     "ticker": "RELIANCE",
        #     "company_name": "Reliance Industries",
        #     "suffix": ".NS"
        # }
    ]
    
    # Score first company (customize as needed)
    company = examples[0]
    
    try:
        result = scorer.score_company(
            finrag=finrag,
            ticker=company["ticker"],
            company_name=company["company_name"],
            ticker_suffix=company["suffix"]
        )
        
        # ========================================
        # STEP 5: Display Results
        # ========================================
        print("\n" + "="*80)
        print("RESULTS")
        print("="*80)
        
        # Pretty print result
        print(result)
        
        # Save results
        output_dir = Path(__file__).parent.parent / "output"
        output_dir.mkdir(exist_ok=True)
        
        # Save as JSON
        json_path = output_dir / f"{company['ticker']}_score.json"
        with open(json_path, 'w') as f:
            f.write(result.to_json())
        print(f"\n💾 Results saved to: {json_path}")
        
        # ========================================
        # STEP 6: Detailed Breakdown
        # ========================================
        print("\n" + "="*80)
        print("DETAILED BREAKDOWN")
        print("="*80)
        
        breakdown = result.breakdown
        
        # Sentiment Analysis Details
        print("\n📊 SENTIMENT ANALYSIS:")
        for aspect in breakdown["sentiment_analysis"].get("aspect_scores", []):
            if "error" not in aspect:
                print(f"  • {aspect['aspect']}: {aspect['sentiment_score']:.2f} "
                      f"(confidence: {aspect['retrieval_confidence']:.2f})")
        
        # Quantitative Metrics Details
        print("\n💰 QUANTITATIVE METRICS:")
        quant_breakdown = breakdown["quantitative"].get("breakdown", {})
        for category, score in quant_breakdown.items():
            print(f"  • {category.replace('_', ' ').title()}: {score:.1f}/100")
        
        # Financial Data Summary
        print("\n📈 KEY FINANCIAL METRICS:")
        fin_data = breakdown["financial_data"]
        metrics_to_show = [
            ("PE Ratio", "pe_ratio"),
            ("Profit Margin", "profit_margin"),
            ("ROE", "roe"),
            ("Revenue Growth", "revenue_growth"),
            ("Debt to Equity", "debt_to_equity"),
            ("Price Change (1Y)", "price_change_1y")
        ]
        
        for label, key in metrics_to_show:
            value = fin_data.get(key)
            if value is not None:
                if key in ["profit_margin", "roe", "revenue_growth"]:
                    print(f"  • {label}: {value*100:.2f}%")
                else:
                    print(f"  • {label}: {value:.2f}")
        
        # ========================================
        # STEP 7: Investment Recommendation
        # ========================================
        print("\n" + "="*80)
        print("INVESTMENT RECOMMENDATION")
        print("="*80)
        
        if result.direction == "bullish" and result.confidence > 70:
            recommendation = "STRONG BUY"
            emoji = "🟢"
        elif result.direction == "bullish":
            recommendation = "BUY"
            emoji = "🟢"
        elif result.direction == "neutral" and result.score > 50:
            recommendation = "HOLD (Slight Positive)"
            emoji = "🟡"
        elif result.direction == "neutral":
            recommendation = "HOLD"
            emoji = "🟡"
        elif result.direction == "bearish" and result.confidence > 70:
            recommendation = "STRONG SELL"
            emoji = "🔴"
        else:
            recommendation = "SELL"
            emoji = "🔴"
        
        print(f"\n{emoji} Recommendation: {recommendation}")
        print(f"   Score: {result.score:.1f}/100")
        print(f"   Confidence: {result.confidence:.1f}%")
        print(f"   Time Horizon: {result.time_horizon}")
        
        print("\n✅ Scoring complete!")
        
    except Exception as e:
        print(f"\n❌ Error during scoring: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # ========================================
    # OPTIONAL: Score Multiple Companies
    # ========================================
    print("\n" + "="*80)
    print("TIP: To score multiple companies, loop through your ticker list:")
    print("="*80)
    print("""
    for company in companies:
        result = scorer.score_company(
            finrag=finrag,
            ticker=company['ticker'],
            ticker_suffix=company['suffix']
        )
        # Process result...
    """)


if __name__ == "__main__":
    main()
