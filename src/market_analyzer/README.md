# Market Analyzer Module

**Domain:** Finance & Market Intelligence  
**Description:** Analyzes news to determine impact on specific companies, calculating potential monetary gains or losses based on market data.

---

## Features

- **Company Database**: Tracks 25+ major companies across multiple sectors
- **Sector Analysis**: Identifies which industries are affected by news
- **Sentiment Detection**: Determines if news is positive/negative for each company
- **Monetary Impact Calculation**: Estimates dollar gains or losses based on market cap
- **Competitor Dynamics**: Considers inverse effects (competitor loss = your gain)
- **Confidence Scoring**: Provides reliability metrics for predictions

---

## Tracked Sectors

| Sector | Example Companies |
|--------|-------------------|
| Technology | AAPL, MSFT, GOOGL, META, NVDA, AMD, TSM |
| Finance | JPM, GS, V |
| Healthcare | JNJ, PFE, MRNA |
| Automotive | TSLA, F, GM |
| Energy | XOM, CVX |
| Retail | AMZN, WMT |
| Defense | LMT, RTX |

---

## Usage

```python
from src.market_analyzer import MarketAnalyzer

# Initialize
analyzer = MarketAnalyzer()

# Analyze news articles
news = [
    {
        "title": "NVIDIA Reports Record AI Chip Demand",
        "snippet": "GPU maker sees unprecedented orders from cloud providers.",
        "link": "https://example.com/news"
    }
]

# Get market analysis
analysis = analyzer.analyze_news(news)

# Access results
print(f"Total Market Impact: ${analysis.total_market_impact:,.0f}")
print(f"Sentiment: {analysis.market_sentiment}")

# Top gainers
for company in analysis.top_gainers:
    print(f"{company.company.ticker}: +${company.monetary_impact/1e6:.2f}M")

# Top losers
for company in analysis.top_losers:
    print(f"{company.company.ticker}: ${company.monetary_impact/1e6:.2f}M")
```

---

## Output Data Structure

### MarketAnalysis
```python
@dataclass
class MarketAnalysis:
    news_summary: str               # Summary of analyzed news
    timestamp: str                  # ISO timestamp
    sector_impacts: Dict            # Sector -> Impact type
    affected_companies: List        # All affected companies
    total_market_impact: float      # Net market movement ($)
    top_gainers: List               # Companies with positive impact
    top_losers: List                # Companies with negative impact
    market_sentiment: str           # "bullish", "bearish", "neutral"
    key_insights: List[str]         # Key takeaways
```

### CompanyImpact
```python
@dataclass
class CompanyImpact:
    company: Company                # Company details
    impact_type: ImpactType         # POSITIVE, NEGATIVE, NEUTRAL
    relevance_score: float          # 0-1 how relevant the news is
    monetary_impact: float          # $ gain (+) or loss (-)
    percentage_change: float        # Expected stock % change
    reasoning: str                  # Explanation of impact
    confidence: float               # Prediction confidence
```

---

## Impact Calculation

The monetary impact is calculated using:

```
Base Impact = Market Cap × 0.1% (baseline exposure)
Sentiment Modifier = (positive - negative words) × 0.5% per word
Relevance Factor = 0-1 based on keyword matches
Final Impact = Base × Relevance × (1 + Sentiment Modifier)
```

---

## Example Output

```
📊 MARKET IMPACT ANALYSIS
=====================================
Market Sentiment: BULLISH
Total Impact: +$1,234,567,890

📈 TOP GAINERS:
  NVDA: +$485.2M (+0.35%)
  MSFT: +$312.5M (+0.12%)
  GOOGL: +$186.3M (+0.18%)

📉 TOP LOSERS:
  INTC: -$92.1M (-0.45%)
  AMD: -$45.6M (-0.21%)

💡 KEY INSIGHTS:
  • Bullish signal for: Technology
  • NVDA expected to gain $485.2M
  • Market shift: 8 gainers vs 2 losers
```

---

## Configuration

Add companies to the database by modifying `_load_companies()`:

```python
Company(
    ticker="TICKER",
    name="Company Name",
    sector=Sector.TECHNOLOGY,
    market_cap_billions=100.0,
    stock_price=50.00,
    daily_volume_millions=10.0,
    keywords=["keyword1", "keyword2"],
    competitors=["COMP1", "COMP2"],
    suppliers=["SUP1"]
)
```

---

## Notes

- Impacts are estimates based on simulated market dynamics
- Real-time stock data integration can be added via APIs
- Competitor inverse-impact modeling creates more realistic scenarios
