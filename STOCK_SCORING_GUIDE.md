# Stock Prediction Scoring System - Guide

## Overview

The **Ensemble Scoring System** combines multiple analytical approaches to generate comprehensive stock prediction scores from annual reports and quantitative financial data.

## 🎯 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ENSEMBLE SCORER                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. SENTIMENT ANALYSIS (25%)                                │
│     └─ Multi-aspect RAG query analysis                     │
│        ├─ Revenue & Growth                                  │
│        ├─ Profitability                                     │
│        ├─ Risk Factors                                      │
│        ├─ Strategic Initiatives                             │
│        ├─ Market Position                                   │
│        ├─ Financial Health                                  │
│        └─ Corporate Governance                              │
│                                                              │
│  2. YEAR-OVER-YEAR TRENDS (20%)                            │
│     └─ Historical performance analysis                      │
│        ├─ Revenue growth trends                             │
│        ├─ Earnings momentum                                 │
│        └─ RAG-based trend extraction                        │
│                                                              │
│  3. RISK-ADJUSTED SCORE (20%)                              │
│     └─ Sentiment adjusted by risk severity                 │
│        ├─ Risk factor identification                        │
│        ├─ Risk severity weighting                           │
│        └─ Score adjustment                                  │
│                                                              │
│  4. QUANTITATIVE METRICS (20%)                             │
│     └─ yfinance financial ratios                            │
│        ├─ Valuation (PE, PB, PS)                           │
│        ├─ Profitability (Margins, ROE, ROA)                │
│        ├─ Growth (Revenue, Earnings)                        │
│        ├─ Financial Health (Debt, Cash Flow)               │
│        └─ Momentum (Price trends, Analysts)                 │
│                                                              │
│  5. LLM JUDGE ASSESSMENT (15%)                             │
│     └─ Holistic evaluation by GPT-4                        │
│        ├─ Comprehensive context retrieval                   │
│        ├─ Integration of all metrics                        │
│        └─ Expert-level scoring                              │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│                   FINAL OUTPUT                              │
├─────────────────────────────────────────────────────────────┤
│  • Overall Score (0-100)                                    │
│  • Direction (Bullish/Bearish/Neutral)                     │
│  • Confidence Level (0-100%)                                │
│  • Component Breakdown                                      │
│  • Key Drivers                                              │
│  • Risk Factors                                             │
└─────────────────────────────────────────────────────────────┘
```

## 📦 Installation

```bash
# Install additional dependencies
pip install yfinance feedparser

# Or update requirements
pip install -r requirements.txt
```

## 🚀 Quick Start

### Basic Usage

```python
from finrag import FinRAG, FinRAGConfig
from finrag.scoring import EnsembleScorer, ScoringConfig

# 1. Initialize FinRAG
config = FinRAGConfig()
config.use_filtered_parsing = True
finrag = FinRAG(config=config)

# 2. Load annual report
text = finrag.load_pdf("annual_report.pdf")
finrag.add_documents([text])

# 3. Initialize scorer
scorer = EnsembleScorer()

# 4. Generate score
result = scorer.score_company(
    finrag=finrag,
    ticker="AAPL",
    company_name="Apple Inc.",
    ticker_suffix=""  # Use ".NS" for NSE, ".BO" for BSE
)

# 5. Display results
print(result)
print(f"Score: {result.score:.1f}/100")
print(f"Direction: {result.direction}")
print(f"Confidence: {result.confidence:.1f}%")
```

### Indian Stocks Example

```python
# For NSE-listed stocks
result = scorer.score_company(
    finrag=finrag,
    ticker="TCS",
    company_name="Tata Consultancy Services",
    ticker_suffix=".NS"  # NSE suffix
)

# For BSE-listed stocks
result = scorer.score_company(
    finrag=finrag,
    ticker="RELIANCE",
    ticker_suffix=".BO"  # BSE suffix
)
```

## ⚙️ Configuration

### Customize Component Weights

```python
from finrag.scoring import ScoringConfig

config = ScoringConfig()

# Adjust weights (must sum to 1.0)
config.sentiment_weight = 0.30      # Increase sentiment importance
config.quantitative_weight = 0.25   # Increase quantitative importance
config.yoy_trend_weight = 0.20
config.risk_adjusted_weight = 0.15
config.llm_judge_weight = 0.10

# Modify time horizon
config.time_horizon = "12-18 months"

scorer = EnsembleScorer(config=config)
```

### Customize Sentiment Aspects

```python
config = ScoringConfig()

# Add custom aspects
config.sentiment_aspects = [
    {
        "name": "Innovation",
        "question": "What innovations and R&D initiatives are mentioned?",
        "weight": 0.30
    },
    {
        "name": "Market Expansion",
        "question": "What market expansion and geographic growth plans exist?",
        "weight": 0.25
    },
    # ... more aspects
]
```

## 📊 Output Format

### ScoringResult Object

```python
result = scorer.score_company(...)

# Access properties
result.score              # 0-100 overall score
result.direction          # 'bullish', 'bearish', 'neutral'
result.confidence         # 0-100% confidence level
result.ticker             # Stock ticker
result.company_name       # Company name

# Component scores
result.sentiment_score       # Sentiment analysis score
result.yoy_trend_score      # Year-over-year trend score
result.risk_adjusted_score  # Risk-adjusted score
result.quantitative_score   # Quantitative metrics score
result.llm_judge_score      # LLM judge score

# Insights
result.key_drivers        # List of positive drivers
result.risk_factors       # List of risk factors

# Detailed breakdown
result.breakdown          # Full breakdown of all components
```

### Save Results

```python
# As JSON
with open("score.json", "w") as f:
    f.write(result.to_json())

# As dictionary
data = result.to_dict()

# Pretty print
print(result)  # Human-readable format
```

## 🔍 Understanding the Components

### 1. Sentiment Analysis (25%)

Analyzes annual report text across 7 aspects:
- **Revenue & Growth**: Sales trends, growth rates
- **Profitability**: Margins, net income
- **Risk Factors**: Challenges, threats
- **Strategic Initiatives**: Future plans, innovations
- **Market Position**: Competitive standing
- **Financial Health**: Cash flow, debt
- **Corporate Governance**: Management quality

**How it works:**
1. Queries RAG for each aspect
2. Extracts sentiment score (-1 to +1)
3. Weights by aspect importance
4. Combines with retrieval confidence

### 2. Year-over-Year Trends (20%)

Combines yfinance growth metrics with RAG analysis:
- Revenue growth rate
- Earnings growth rate
- Historical trend patterns
- Growth acceleration/deceleration

**How it works:**
1. Fetches growth data from yfinance
2. Queries RAG for historical trends
3. Combines quantitative + qualitative analysis
4. Scores based on growth momentum

### 3. Risk-Adjusted Score (20%)

Adjusts sentiment score based on risk severity:
- Identifies risk factors from annual report
- Categorizes risks (high/medium/low)
- Applies risk-based adjustments
- Balances opportunity vs. risk

**How it works:**
1. Queries RAG for risk factors
2. Analyzes risk severity keywords
3. Adjusts base sentiment score
4. Returns risk-adjusted score

### 4. Quantitative Metrics (20%)

Scores financial ratios from yfinance across 5 categories:

**Valuation (Weight: 20%)**
- PE Ratio: Lower is better (optimal 10-20)
- PEG Ratio: <1 is excellent
- Price-to-Book: <3 is good

**Profitability (Weight: 25%)**
- Profit Margin: >20% is excellent
- Operating Margin: >25% is excellent
- ROE: >20% is excellent
- ROA: >10% is excellent

**Growth (Weight: 25%)**
- Revenue Growth: >20% is excellent
- Earnings Growth: >25% is excellent

**Financial Health (Weight: 15%)**
- Debt-to-Equity: <1 is good
- Current Ratio: >1.5 is good
- Free Cash Flow: Positive is essential

**Momentum (Weight: 15%)**
- Price changes (1M, 3M, 6M, 1Y)
- Analyst recommendations
- Target price vs. current price

### 5. LLM Judge Assessment (15%)

GPT-4 provides holistic evaluation:
1. Retrieves comprehensive context from RAG
2. Considers all quantitative metrics
3. Reviews preliminary scores
4. Provides expert-level assessment

## 📈 Interpreting Scores

### Score Ranges

| Score | Direction | Interpretation |
|-------|-----------|----------------|
| 80-100 | Bullish | Strong Buy - Excellent fundamentals & outlook |
| 65-79 | Bullish | Buy - Positive indicators, good potential |
| 50-64 | Neutral+ | Hold - Stable with slight upside |
| 45-49 | Neutral | Hold - Mixed signals |
| 30-44 | Bearish | Sell - Concerning indicators |
| 0-29 | Bearish | Strong Sell - Significant issues |

### Confidence Levels

| Confidence | Interpretation |
|------------|----------------|
| 80-100% | High - Strong data availability, method agreement |
| 60-79% | Medium - Good data, some method disagreement |
| 40-59% | Low - Limited data or significant disagreement |
| 0-39% | Very Low - Insufficient data or major conflicts |

### Investment Recommendations

```
Score ≥ 65 + Confidence > 70% → STRONG BUY
Score ≥ 65 + Confidence ≤ 70% → BUY
Score 50-64 → HOLD (Slight Positive)
Score 45-49 → HOLD
Score 30-44 → SELL
Score < 30 + Confidence > 70% → STRONG SELL
```

## 🎯 Best Practices

### 1. Use Filtered Parsing
```python
config = FinRAGConfig()
config.use_filtered_parsing = True  # Reduces costs, improves quality
```

### 2. Load Multiple Years
```python
# Load 3+ years for better trend analysis
reports = [
    "annual_report_2024.pdf",
    "annual_report_2023.pdf",
    "annual_report_2022.pdf"
]

documents = [finrag.load_pdf(pdf) for pdf in reports]
finrag.add_documents(documents)
```

### 3. Verify Ticker Format
```python
# US Stocks: No suffix
ticker="AAPL", suffix=""

# NSE (India): .NS suffix
ticker="TCS", suffix=".NS"

# BSE (India): .BO suffix
ticker="RELIANCE", suffix=".BO"

# Other markets: Check yfinance documentation
```

### 4. Handle Errors Gracefully
```python
try:
    result = scorer.score_company(finrag, ticker="XYZ")
except Exception as e:
    print(f"Scoring failed: {e}")
    # Fallback strategy
```

### 5. Batch Processing
```python
companies = [
    {"ticker": "AAPL", "suffix": ""},
    {"ticker": "TCS", "suffix": ".NS"},
    # ... more companies
]

results = []
for company in companies:
    result = scorer.score_company(
        finrag=finrag,
        ticker=company["ticker"],
        ticker_suffix=company["suffix"]
    )
    results.append(result)
    
    # Save individual results
    with open(f"{company['ticker']}_score.json", "w") as f:
        f.write(result.to_json())
```

## 🐛 Troubleshooting

### Issue: Low data completeness

**Solution:** The company may not have complete data on yfinance. Check:
```python
result.breakdown["financial_data"]["data_completeness"]
```

### Issue: Sentiment score is 50 (neutral)

**Possible causes:**
- Annual report not loaded properly
- Filtered parsing removed relevant content
- Retrieval not finding relevant sections

**Solutions:**
- Verify PDF loaded: `finrag.get_statistics()`
- Disable filtering: `config.use_filtered_parsing = False`
- Check retrieval: Query manually to verify content

### Issue: yfinance fails

**Possible causes:**
- Invalid ticker symbol
- Network issues
- Yahoo Finance API changes

**Solutions:**
- Verify ticker on finance.yahoo.com
- Add correct suffix (.NS, .BO, etc.)
- Check internet connection

### Issue: LLM errors

**Possible causes:**
- API key issues
- Rate limits
- Model availability

**Solutions:**
- Verify `OPENAI_API_KEY` in .env
- Reduce number of queries
- Use fallback models

## 📚 Examples

### Example 1: Single Company Score

```python
scorer = EnsembleScorer()
result = scorer.score_company(finrag, ticker="AAPL")

if result.score >= 65:
    print(f"✅ BUY recommendation - Score: {result.score:.1f}")
else:
    print(f"⚠️ HOLD/SELL - Score: {result.score:.1f}")
```

### Example 2: Sector Comparison

```python
tech_companies = ["AAPL", "MSFT", "GOOGL"]

scores = {}
for ticker in tech_companies:
    result = scorer.score_company(finrag, ticker=ticker)
    scores[ticker] = result.score

best = max(scores, key=scores.get)
print(f"Best in sector: {best} ({scores[best]:.1f})")
```

### Example 3: Custom Weights

```python
# Conservative investor (more weight on risk)
conservative_config = ScoringConfig()
conservative_config.risk_adjusted_weight = 0.30
conservative_config.quantitative_weight = 0.25
conservative_config.sentiment_weight = 0.20
conservative_config.yoy_trend_weight = 0.15
conservative_config.llm_judge_weight = 0.10

scorer = EnsembleScorer(config=conservative_config)
```

## 🔗 Integration with Existing Systems

### With Your API

```python
from fastapi import FastAPI
from finrag.scoring import EnsembleScorer

app = FastAPI()

@app.post("/score")
def score_stock(ticker: str):
    scorer = EnsembleScorer()
    result = scorer.score_company(finrag, ticker=ticker)
    return result.to_dict()
```

### With Your Screening Tool

```python
# Combine with your api_ratios.py
from api_ratios import get_screener_data

def enhanced_analysis(ticker: str):
    # Get your existing data
    screener_data = get_screener_data(ticker)
    
    # Add FinRAG scoring
    finrag_score = scorer.score_company(finrag, ticker=ticker)
    
    return {
        "screener_data": screener_data,
        "finrag_score": finrag_score.to_dict()
    }
```

## 📊 Performance Expectations

- **Processing Time**: 2-5 minutes per company
  - yfinance fetch: 5-10 seconds
  - Sentiment analysis: 30-60 seconds (7 queries)
  - YoY trends: 10-15 seconds
  - Risk adjustment: 10-15 seconds
  - Quantitative: <1 second (local computation)
  - LLM judge: 15-20 seconds

- **Costs** (per company):
  - OpenAI API: ~$0.10-0.20
  - With filtered parsing: ~$0.05-0.10 (50-60% savings)

- **Accuracy**: Depends on:
  - Quality of annual report
  - Data completeness on yfinance
  - Number of years analyzed

## 🎓 Advanced Usage

See `examples/stock_scoring_example.py` for complete implementation.

## 📝 Notes

- Always verify ticker symbols on finance.yahoo.com
- Use filtered parsing to reduce costs
- Load multiple years for better trend analysis
- Adjust weights based on your investment strategy
- Confidence scores indicate reliability of predictions
- Combine with your own analysis for best results

---

**Need help?** Check the example script or review the component implementations in `src/finrag/scoring/`.
