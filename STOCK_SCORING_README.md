# 📊 Stock Prediction Scoring System

> **Ensemble scoring system combining annual report analysis (RAG) with quantitative financial metrics (yfinance) to generate comprehensive stock prediction scores.**

## 🎯 What Does It Do?

Analyzes company annual reports and financial data to generate:
- **Overall Score** (0-100): Stock prediction score
- **Direction**: Bullish/Bearish/Neutral
- **Confidence Level**: How reliable the prediction is
- **Component Breakdown**: Detailed analysis of all factors
- **Key Drivers**: What's pushing the stock up
- **Risk Factors**: What could hold it back
- **Investment Recommendation**: Clear buy/hold/sell signal

## 🚀 Quick Start (5 Minutes)

```bash
# 1. Install dependencies
pip install yfinance feedparser

# 2. Run example
cd FinRAG
python examples/stock_scoring_example.py
```

## 💻 Basic Usage

```python
from finrag import FinRAG, FinRAGConfig, EnsembleScorer

# Initialize
config = FinRAGConfig()
config.use_filtered_parsing = True  # Save 60% on costs
finrag = FinRAG(config=config)

# Load annual report
text = finrag.load_pdf("annual_report.pdf")
finrag.add_documents([text])

# Score the company
scorer = EnsembleScorer()
result = scorer.score_company(
    finrag=finrag,
    ticker="AAPL",
    ticker_suffix=""  # Use ".NS" for NSE, ".BO" for BSE
)

# View results
print(f"Score: {result.score:.1f}/100")
print(f"Direction: {result.direction}")
print(f"Confidence: {result.confidence:.1f}%")
print(f"Recommendation: {result.direction.upper()}")
```

## 🎨 System Architecture

```
┌─────────────────────────────────────────┐
│        ENSEMBLE SCORER                  │
├─────────────────────────────────────────┤
│                                          │
│  1. Sentiment Analysis      (25%)       │
│     └─ 7 aspects from annual report     │
│                                          │
│  2. Year-over-Year Trends   (20%)       │
│     └─ Growth momentum analysis          │
│                                          │
│  3. Risk-Adjusted Score     (20%)       │
│     └─ Sentiment adjusted for risks     │
│                                          │
│  4. Quantitative Metrics    (20%)       │
│     └─ 40+ financial ratios              │
│                                          │
│  5. LLM Judge Assessment    (15%)       │
│     └─ Holistic GPT-4 evaluation        │
│                                          │
├─────────────────────────────────────────┤
│  Final Score: 0-100                     │
│  Direction: Bullish/Bearish/Neutral     │
│  Confidence: 0-100%                      │
└─────────────────────────────────────────┘
```

## 📊 Score Interpretation

| Score | Direction | Action | Meaning |
|-------|-----------|--------|---------|
| 80-100 | Bullish | 🟢 **Strong Buy** | Excellent fundamentals |
| 65-79 | Bullish | 🟢 **Buy** | Positive outlook |
| 50-64 | Neutral | 🟡 **Hold+** | Slight upside |
| 45-49 | Neutral | 🟡 **Hold** | Mixed signals |
| 30-44 | Bearish | 🔴 **Sell** | Concerns present |
| 0-29 | Bearish | 🔴 **Strong Sell** | Significant issues |

## 🔧 What Gets Analyzed?

### From Annual Report (via RAG)
- Revenue & growth trends
- Profitability metrics
- Risk factors & challenges
- Strategic initiatives
- Market positioning
- Corporate governance
- Future outlook

### From yfinance (Real-time)
- **Valuation**: PE, PB, PS ratios
- **Profitability**: Margins, ROE, ROA
- **Growth**: Revenue/earnings growth
- **Health**: Debt levels, cash flow
- **Momentum**: Price trends, analyst ratings

## ⚙️ Configuration

### Customize Component Weights

```python
from finrag.scoring import ScoringConfig

# Conservative (risk-focused)
config = ScoringConfig()
config.sentiment_weight = 0.20
config.risk_adjusted_weight = 0.30
config.quantitative_weight = 0.25
config.yoy_trend_weight = 0.15
config.llm_judge_weight = 0.10

# Growth-focused
config = ScoringConfig()
config.yoy_trend_weight = 0.30
config.sentiment_weight = 0.25
config.quantitative_weight = 0.20
```

### For Indian Stocks

```python
# NSE-listed
result = scorer.score_company(
    finrag=finrag,
    ticker="TCS",
    ticker_suffix=".NS"
)

# BSE-listed
result = scorer.score_company(
    finrag=finrag,
    ticker="RELIANCE",
    ticker_suffix=".BO"
)
```

## 📈 Output Format

```python
result.score                   # 72.5
result.direction               # 'bullish'
result.confidence              # 84.3

# Component scores
result.sentiment_score         # 75.2
result.yoy_trend_score        # 68.5
result.risk_adjusted_score    # 70.1
result.quantitative_score     # 78.9
result.llm_judge_score        # 73.0

# Insights
result.key_drivers            # ['Strong revenue growth', 'Expanding margins']
result.risk_factors           # ['Market competition', 'Regulatory concerns']

# Detailed data
result.breakdown              # Full breakdown dictionary

# Save results
with open("score.json", "w") as f:
    f.write(result.to_json())
```

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| **STOCK_SCORING_QUICKSTART.md** | Quick reference guide |
| **STOCK_SCORING_GUIDE.md** | Complete documentation |
| **ENSEMBLE_SCORING_SUMMARY.md** | Implementation details |
| **examples/stock_scoring_example.py** | Working code examples |
| **scoring_flow_diagram.py** | Visual flow diagram |

## 🎯 Common Use Cases

### 1. Single Company Analysis
```python
result = scorer.score_company(finrag, ticker="AAPL")
print(f"Recommendation: {result.direction.upper()}")
```

### 2. Sector Comparison
```python
tech_companies = ["AAPL", "MSFT", "GOOGL"]
scores = {t: scorer.score_company(finrag, ticker=t).score 
          for t in tech_companies}
best = max(scores, key=scores.get)
```

### 3. Portfolio Screening
```python
for ticker in portfolio:
    result = scorer.score_company(finrag, ticker=ticker)
    if result.score < 45 and result.confidence > 70:
        print(f"⚠️ Consider selling {ticker}")
```

### 4. Integration with Your API
```python
from fastapi import FastAPI

@app.post("/score/{ticker}")
def score_stock(ticker: str):
    result = scorer.score_company(finrag, ticker=ticker)
    return result.to_dict()
```

## 💡 Pro Tips

1. **Use Filtered Parsing** - Saves 60% on costs
   ```python
   config.use_filtered_parsing = True
   ```

2. **Load Multiple Years** - Better trend analysis
   ```python
   reports = ["2024.pdf", "2023.pdf", "2022.pdf"]
   finrag.add_documents([finrag.load_pdf(pdf) for pdf in reports])
   ```

3. **Verify Ticker Format** - Check on finance.yahoo.com
   ```python
   # US: No suffix
   # India NSE: .NS
   # India BSE: .BO
   ```

4. **Monitor Confidence** - Low confidence = more research needed
   ```python
   if result.confidence < 60:
       print("⚠️ Low confidence - verify manually")
   ```

5. **Customize for Your Strategy** - Adjust weights
   ```python
   # More weight on quantitative for value investing
   config.quantitative_weight = 0.35
   ```

## 📊 Performance

- **Processing Time**: 2-5 minutes per company
- **Cost per Company**: $0.05-0.10 (with filtering)
- **Accuracy**: Depends on report quality and data completeness

## 🔍 Components Breakdown

### 1. Sentiment Analysis (25%)
Queries annual report for 7 key aspects and extracts sentiment using LLM.

### 2. Year-over-Year Trends (20%)
Combines yfinance growth metrics with historical trend analysis from reports.

### 3. Risk-Adjusted Score (20%)
Adjusts sentiment score based on identified risk severity.

### 4. Quantitative Metrics (20%)
Scores 40+ financial ratios across 5 categories using industry thresholds.

### 5. LLM Judge (15%)
GPT-4 provides holistic assessment combining all factors.

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Ticker not found" | Add correct suffix (.NS, .BO, etc.) |
| Low confidence | Load multiple years of reports |
| Neutral sentiment | Verify PDF loaded correctly |
| API errors | Check `OPENAI_API_KEY` in .env |
| High costs | Enable `use_filtered_parsing` |

## 🎓 Examples

**View the flow diagram:**
```bash
python scoring_flow_diagram.py
```

**Run complete example:**
```bash
python examples/stock_scoring_example.py
```

**Batch processing:**
```python
companies = [
    {"ticker": "AAPL", "suffix": ""},
    {"ticker": "TCS", "suffix": ".NS"},
]

for company in companies:
    result = scorer.score_company(
        finrag=finrag,
        ticker=company["ticker"],
        ticker_suffix=company["suffix"]
    )
    print(f"{company['ticker']}: {result.score:.1f} ({result.direction})")
```

## 🔗 Integration

### With Your Existing System

```python
# Combine with your api_ratios.py
from api_ratios import get_screener_data

def comprehensive_analysis(ticker: str):
    # Your existing data
    screener = get_screener_data(ticker)
    
    # Add FinRAG scoring
    score = scorer.score_company(finrag, ticker=ticker, ticker_suffix=".NS")
    
    return {
        "financial_data": screener,
        "prediction": score.to_dict()
    }
```

## 📦 Installation

```bash
# Required packages
pip install yfinance feedparser

# Or update all requirements
pip install -r requirements.txt
```

## ✨ Key Features

- ✅ Combines qualitative (RAG) + quantitative (yfinance)
- ✅ 5 independent methods reduce bias
- ✅ Confidence scoring for reliability
- ✅ Full transparency and customization
- ✅ Works with filtered parsing (60% cost savings)
- ✅ Clear buy/hold/sell recommendations
- ✅ Detailed breakdown of all factors
- ✅ Ready for production use

## 🎉 Ready to Use!

```bash
python examples/stock_scoring_example.py
```

For more details, see:
- **Quick Start**: `STOCK_SCORING_QUICKSTART.md`
- **Full Guide**: `STOCK_SCORING_GUIDE.md`
- **Implementation**: `ENSEMBLE_SCORING_SUMMARY.md`

---

**Generate your first stock prediction score in under 5 minutes!** 🚀
