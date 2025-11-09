# Stock Scoring System - Quick Reference

## 🚀 5-Minute Setup

```bash
# 1. Install dependencies
pip install yfinance feedparser

# 2. Set up environment
export OPENAI_API_KEY="your-key"
export LLAMA_CLOUD_API_KEY="your-key"

# 3. Run example
cd FinRAG
python examples/stock_scoring_example.py
```

## 📝 Minimal Example

```python
from finrag import FinRAG, FinRAGConfig
from finrag.scoring import EnsembleScorer

# Initialize
config = FinRAGConfig()
config.use_filtered_parsing = True
finrag = FinRAG(config=config)

# Load report
text = finrag.load_pdf("annual_report.pdf")
finrag.add_documents([text])

# Score
scorer = EnsembleScorer()
result = scorer.score_company(finrag, ticker="AAPL")

# Results
print(f"Score: {result.score:.1f}/100")
print(f"Direction: {result.direction}")
print(f"Confidence: {result.confidence:.1f}%")
```

## 🎯 Key Components

| Component | Weight | What It Does |
|-----------|--------|--------------|
| Sentiment Analysis | 25% | Analyzes 7 aspects of annual report |
| YoY Trends | 20% | Revenue/earnings growth patterns |
| Risk-Adjusted | 20% | Sentiment adjusted for risks |
| Quantitative | 20% | Financial ratios from yfinance |
| LLM Judge | 15% | Holistic GPT-4 assessment |

## 📊 Score Interpretation

| Score | Action | Meaning |
|-------|--------|---------|
| 80-100 | 🟢 Strong Buy | Excellent fundamentals |
| 65-79 | 🟢 Buy | Positive outlook |
| 50-64 | 🟡 Hold+ | Slight upside |
| 45-49 | 🟡 Hold | Mixed signals |
| 30-44 | 🔴 Sell | Concerns present |
| 0-29 | 🔴 Strong Sell | Significant issues |

## 🔧 Common Configurations

### Conservative (Risk-Focused)
```python
config = ScoringConfig()
config.risk_adjusted_weight = 0.30
config.quantitative_weight = 0.25
config.sentiment_weight = 0.20
```

### Growth-Focused
```python
config = ScoringConfig()
config.yoy_trend_weight = 0.30
config.sentiment_weight = 0.25
config.quantitative_weight = 0.20
```

### Value-Focused
```python
config = ScoringConfig()
config.quantitative_weight = 0.35
config.risk_adjusted_weight = 0.25
config.sentiment_weight = 0.20
```

## 🌏 Ticker Formats

```python
# US Stocks
ticker="AAPL", suffix=""

# India - NSE
ticker="TCS", suffix=".NS"

# India - BSE
ticker="RELIANCE", suffix=".BO"

# UK
ticker="VOD", suffix=".L"

# Germany
ticker="BMW", suffix=".DE"
```

## 📦 Output Structure

```python
result.score                 # 0-100 overall score
result.direction             # bullish/bearish/neutral
result.confidence            # 0-100% confidence
result.sentiment_score       # Component score
result.yoy_trend_score       # Component score
result.risk_adjusted_score   # Component score
result.quantitative_score    # Component score
result.llm_judge_score       # Component score
result.key_drivers           # List of positive factors
result.risk_factors          # List of concerns
result.breakdown             # Full detailed data
```

## 💾 Save Results

```python
# JSON
with open("score.json", "w") as f:
    f.write(result.to_json())

# Dictionary
data = result.to_dict()

# Pretty print
print(result)
```

## 🔍 Access Detailed Data

```python
# Financial metrics
fin_data = result.breakdown["financial_data"]
print(f"PE Ratio: {fin_data['pe_ratio']}")
print(f"ROE: {fin_data['roe']}")

# Sentiment details
for aspect in result.breakdown["sentiment_analysis"]["aspect_scores"]:
    print(f"{aspect['aspect']}: {aspect['sentiment_score']}")

# Quantitative breakdown
quant = result.breakdown["quantitative"]["breakdown"]
print(f"Valuation Score: {quant['valuation']}")
print(f"Growth Score: {quant['growth']}")
```

## 🎛️ Performance Settings

### Fast (Lower Cost)
```python
config = FinRAGConfig()
config.llm_model = "gpt-3.5-turbo"  # Instead of gpt-4
config.top_k = 5                     # Fewer retrievals

scoring_config = ScoringConfig()
scoring_config.sentiment_aspects = [...]  # Fewer aspects (3-4)
```

### Accurate (Higher Cost)
```python
config = FinRAGConfig()
config.llm_model = "gpt-4-turbo-preview"
config.top_k = 15

scoring_config = ScoringConfig()
# Use all 7 sentiment aspects (default)
```

## 🐛 Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| "Ticker not found" | Add correct suffix (.NS, .BO, etc.) |
| Low confidence | Load multiple years of reports |
| Neutral sentiment | Verify PDF loaded correctly |
| API errors | Check API keys in .env |
| Slow performance | Reduce top_k and sentiment aspects |

## 📈 Batch Processing

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
    print(f"{company['ticker']}: {result.score:.1f}")
```

## 🔗 Integration Examples

### FastAPI
```python
from fastapi import FastAPI

@app.post("/score/{ticker}")
def score(ticker: str):
    result = scorer.score_company(finrag, ticker=ticker)
    return result.to_dict()
```

### Pandas DataFrame
```python
import pandas as pd

results = []
for ticker in tickers:
    result = scorer.score_company(finrag, ticker=ticker)
    results.append({
        "ticker": ticker,
        "score": result.score,
        "direction": result.direction,
        "confidence": result.confidence
    })

df = pd.DataFrame(results)
df.to_csv("scores.csv")
```

## 💡 Pro Tips

1. **Use Filtered Parsing** - Saves 60-80% on costs
2. **Load Multiple Years** - Better trend analysis
3. **Verify Tickers** - Check on finance.yahoo.com first
4. **Batch at Night** - Avoid rate limits
5. **Save Results** - Cache scores to avoid re-processing
6. **Combine Methods** - Use with your existing analysis
7. **Monitor Confidence** - Low confidence = more research needed

## 📚 Full Documentation

- **Detailed Guide**: `STOCK_SCORING_GUIDE.md`
- **Example Script**: `examples/stock_scoring_example.py`
- **API Reference**: `src/finrag/scoring/`

## 🎓 Learning Path

1. Run `stock_scoring_example.py` with sample data
2. Try with one real company (single PDF)
3. Customize weights for your strategy
4. Scale to multiple companies
5. Integrate with your workflow

---

**Quick Start Command:**
```bash
cd FinRAG && python examples/stock_scoring_example.py
```
