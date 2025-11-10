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

# Rich formatting imports
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box
from rich.layout import Layout
from rich.text import Text

# Load environment variables
load_env_file()

# Initialize Rich console
console = Console()


def main():
    """Main function demonstrating stock scoring."""
    
    # Header
    console.print(Panel.fit(
        "[bold cyan]STOCK PREDICTION SCORING[/bold cyan]\n"
        "[yellow]Ensemble Method with RAG + Financial Data[/yellow]",
        border_style="cyan",
        padding=(1, 2)
    ))
    
    # ========================================
    # STEP 1: Initialize FinRAG and Load Pre-built Tree
    # ========================================
    console.print("\n[bold cyan]📚 Step 1:[/bold cyan] Initializing FinRAG system...")
    
    config = FinRAGConfig()
    config.use_filtered_parsing = True  # Use intelligent filtering
    config.use_metadata_clustering = True  # Use fixed hierarchical structure
    
    finrag = FinRAG(config=config)
    console.print("   [green]✓[/green] FinRAG initialized")
    
    # ========================================
    # STEP 2: Load Pre-built Tree (from all PDFs)
    # ========================================
    console.print("\n[bold cyan]📄 Step 2:[/bold cyan] Loading pre-built tree...")
    
    # Load tree built from all PDFs in data folder
    tree_path = Path(__file__).parent.parent / "finrag_tree"
    
    if tree_path.exists():
        with console.status("[cyan]Loading tree..."):
            finrag.load(str(tree_path))
        
        stats = finrag.get_statistics()
        console.print(f"   [green]✓[/green] Tree loaded with [bold]{stats['total_nodes']}[/bold] nodes")
        console.print(f"   [green]✓[/green] Documents from data folder already indexed")
        
    else:
        console.print(f"   [red]✗[/red] Tree not found at: {tree_path}")
        console.print("\n   Please build the tree first by running:")
        console.print("     [yellow]python scripts/build_tree.py[/yellow]")
        console.print("\n   This will process all PDFs in data folder and create a reusable tree.")
        return
    
    # ========================================
    # STEP 3: Initialize Ensemble Scorer
    # ========================================
    console.print("\n[bold cyan]🎯 Step 3:[/bold cyan] Initializing Ensemble Scorer...")
    
    # Use default configuration or customize
    scoring_config = ScoringConfig()
    
    # Optional: Customize weights
    # scoring_config.sentiment_weight = 0.30
    # scoring_config.quantitative_weight = 0.25
    
    scorer = EnsembleScorer(config=scoring_config)
    console.print("   [green]✓[/green] Ensemble scorer initialized")
    
    # ========================================
    # STEP 4: Generate Stock Prediction Score
    # ========================================
    console.print("\n[bold cyan]💹 Step 4:[/bold cyan] Generating stock prediction score...")
    
    # Show scoring methods
    methods_table = Table(title="Scoring Pipeline", box=box.ROUNDED, border_style="yellow")
    methods_table.add_column("Step", style="cyan", justify="center")
    methods_table.add_column("Method", style="white")
    methods_table.add_column("Weight", style="yellow", justify="right")
    
    methods_table.add_row("1", "Fetch financial data from yfinance", "-")
    methods_table.add_row("2", "Analyze sentiment from annual report", "25%")
    methods_table.add_row("3", "Calculate year-over-year trends", "20%")
    methods_table.add_row("4", "Generate risk-adjusted score", "20%")
    methods_table.add_row("5", "Score quantitative metrics", "20%")
    methods_table.add_row("6", "Get LLM judge assessment", "15%")
    methods_table.add_row("7", "Combine into ensemble score", "100%")
    
    console.print(methods_table)
    console.print()
    
    # Example companies (customize for your use case)
    # For Indian stocks, use .NS (NSE) or .BO (BSE) suffix
    examples = [
        {
            "ticker": "M&M.NS",
            "company_name": "Mahindra",
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
        # Show which company we're scoring
        console.print(Panel(
            f"[bold white]Scoring:[/bold white] {company['company_name']}\n"
            f"[cyan]Ticker:[/cyan] {company['ticker']}{company['suffix']}",
            border_style="blue",
            padding=(1, 2)
        ))
        
        with console.status("[bold cyan]Running ensemble scoring (this may take 30-60 seconds)..."):
            result = scorer.score_company(
                finrag=finrag,
                ticker=company["ticker"],
                company_name=company["company_name"],
                ticker_suffix=company["suffix"]
            )
        
        console.print("[green]✓[/green] Scoring complete!\n")
        
        # ========================================
        # STEP 5: Display Results
        # ========================================
        
        # Main Score Display
        score_color = "green" if result.score >= 65 else "red" if result.score <= 45 else "yellow"
        direction_emoji = "📈" if result.direction == "bullish" else "📉" if result.direction == "bearish" else "➡️"
        
        score_panel = Panel(
            f"[bold {score_color}]{result.score:.1f}/100[/bold {score_color}]\n\n"
            f"{direction_emoji} Direction: [bold]{result.direction.upper()}[/bold]\n"
            f"🎯 Confidence: [bold]{result.confidence:.1f}%[/bold]\n"
            f"⏰ Time Horizon: [bold]{result.time_horizon}[/bold]",
            title="[bold cyan]📊 FINAL SCORE[/bold cyan]",
            border_style=score_color,
            padding=(1, 2)
        )
        console.print(score_panel)
        console.print()
        
        # Save results
        output_dir = Path(__file__).parent.parent / "output"
        output_dir.mkdir(exist_ok=True)
        
        # Save as JSON
        json_path = output_dir / f"{company['ticker']}_score.json"
        with open(json_path, 'w') as f:
            f.write(result.to_json())
        console.print(f"[green]💾[/green] Results saved to: [cyan]{json_path}[/cyan]\n")
        
        # ========================================
        # STEP 6: Detailed Breakdown
        # ========================================
        
        breakdown = result.breakdown
        
        # Component Scores Table
        components_table = Table(
            title="🎯 Scoring Components Breakdown",
            box=box.DOUBLE_EDGE,
            border_style="cyan"
        )
        components_table.add_column("Method", style="cyan")
        components_table.add_column("Score", style="yellow", justify="right")
        components_table.add_column("Weight", style="white", justify="right")
        components_table.add_column("Contribution", style="green", justify="right")
        
        components = [
            ("Sentiment Analysis", result.sentiment_score, 0.25),
            ("YoY Trends", result.yoy_trend_score, 0.20),
            ("Risk-Adjusted", result.risk_adjusted_score, 0.20),
            ("Quantitative Metrics", result.quantitative_score, 0.20),
            ("LLM Judge", result.llm_judge_score, 0.15)
        ]
        
        for method, score, weight in components:
            contribution = score * weight
            components_table.add_row(
                method,
                f"{score:.1f}",
                f"{weight*100:.0f}%",
                f"{contribution:.1f}"
            )
        
        console.print(components_table)
        console.print()
        
        # Sentiment Analysis Details
        sentiment_table = Table(
            title="📊 Sentiment Analysis by Aspect",
            box=box.ROUNDED,
            border_style="blue"
        )
        sentiment_table.add_column("Aspect", style="cyan")
        sentiment_table.add_column("Score", style="yellow", justify="right")
        sentiment_table.add_column("Confidence", style="green", justify="right")
        
        for aspect in breakdown["sentiment_analysis"].get("aspect_scores", []):
            if "error" not in aspect:
                sentiment_table.add_row(
                    aspect['aspect'],
                    f"{aspect['sentiment_score']:.2f}",
                    f"{aspect['retrieval_confidence']:.2f}"
                )
        
        console.print(sentiment_table)
        console.print()
        
        # Quantitative Metrics Details
        quant_table = Table(
            title="💰 Quantitative Metrics by Category",
            box=box.ROUNDED,
            border_style="green"
        )
        quant_table.add_column("Category", style="cyan")
        quant_table.add_column("Score", style="yellow", justify="right")
        quant_table.add_column("Status", style="white")
        
        quant_breakdown = breakdown["quantitative"].get("breakdown", {})
        for category, score in quant_breakdown.items():
            status = "🟢 Excellent" if score >= 80 else "🟡 Good" if score >= 60 else "🟠 Fair" if score >= 40 else "🔴 Poor"
            quant_table.add_row(
                category.replace('_', ' ').title(),
                f"{score:.1f}",
                status
            )
        
        console.print(quant_table)
        console.print()
        
        # Financial Data Summary
        fin_table = Table(
            title="📈 Key Financial Metrics",
            box=box.ROUNDED,
            border_style="magenta"
        )
        fin_table.add_column("Metric", style="cyan")
        fin_table.add_column("Value", style="yellow", justify="right")
        
        fin_data = breakdown["financial_data"]
        metrics_to_show = [
            ("PE Ratio", "pe_ratio", False),
            ("Profit Margin", "profit_margin", True),
            ("ROE", "roe", True),
            ("Revenue Growth", "revenue_growth", True),
            ("Debt to Equity", "debt_to_equity", False),
            ("Price Change (1Y)", "price_change_1y", True)
        ]
        
        for label, key, is_percentage in metrics_to_show:
            value = fin_data.get(key)
            if value is not None:
                if is_percentage:
                    fin_table.add_row(label, f"{value*100:.2f}%")
                else:
                    fin_table.add_row(label, f"{value:.2f}")
        
        console.print(fin_table)
        console.print()
        
        # ========================================
        # STEP 7: Investment Recommendation
        # ========================================
        
        if result.direction == "bullish" and result.confidence > 70:
            recommendation = "STRONG BUY"
            emoji = "🟢"
            rec_color = "green"
        elif result.direction == "bullish":
            recommendation = "BUY"
            emoji = "🟢"
            rec_color = "green"
        elif result.direction == "neutral" and result.score > 50:
            recommendation = "HOLD (Slight Positive)"
            emoji = "🟡"
            rec_color = "yellow"
        elif result.direction == "neutral":
            recommendation = "HOLD"
            emoji = "🟡"
            rec_color = "yellow"
        elif result.direction == "bearish" and result.confidence > 70:
            recommendation = "STRONG SELL"
            emoji = "🔴"
            rec_color = "red"
        else:
            recommendation = "SELL"
            emoji = "🔴"
            rec_color = "red"
        
        # Final Recommendation Panel
        rec_panel = Panel(
            f"{emoji} [bold {rec_color}]{recommendation}[/bold {rec_color}]\n\n"
            f"[cyan]Score:[/cyan] {result.score:.1f}/100\n"
            f"[cyan]Confidence:[/cyan] {result.confidence:.1f}%\n"
            f"[cyan]Time Horizon:[/cyan] {result.time_horizon}\n\n"
            f"[dim]Based on ensemble analysis of annual reports and financial data[/dim]",
            title="[bold white]💡 INVESTMENT RECOMMENDATION[/bold white]",
            border_style=rec_color,
            padding=(1, 2)
        )
        
        console.print(rec_panel)
        
        # Success message
        console.print("\n[green]✅ Scoring complete![/green]")
        
    except Exception as e:
        console.print(f"\n[red]✗ Error during scoring: {str(e)}[/red]")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
