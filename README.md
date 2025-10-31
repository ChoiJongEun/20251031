# Stock Price Dataset Overview

This repository contains `temp.csv`, a price history for Samsung Electronics (005930.KS), Apple (AAPL), and Nvidia (NVDA). The file stores five daily metrics—open, high, low, close, and volume—for each ticker across a shared date index.

## Data coverage
- **Trading days:** 516
- **Date range:** 2023-10-16 to 2025-10-10
- **Metrics per ticker:** Close, High, Low, Open, Volume

The CSV uses a three-row header produced from a multi-index export. The included [`analysis.py`](analysis.py) helper normalizes that header into single-level column names before computing statistics.

## Summary statistics

### Daily close price (₩ for 005930.KS, USD for AAPL & NVDA)

| Ticker    | Mean Close | Minimum Close | Maximum Close |
|-----------|-----------:|--------------:|--------------:|
| 005930.KS | 66,471.53  | 48,968.97     | 94,400.00     |
| AAPL      |    209.52  |    163.82     |    258.10     |
| NVDA      |    115.60  |     40.30     |    192.57     |

### Daily volume (shares)

| Ticker    | Mean Volume | Minimum Volume | Maximum Volume |
|-----------|------------:|---------------:|---------------:|
| 005930.KS |  19,481,205 |      2,957,915 |     57,691,266 |
| AAPL      |  56,558,297 |     23,234,700 |    318,679,900 |
| NVDA      | 325,122,505 |    105,157,000 |  1,142,269,000 |

### Close-price correlations

| Pair                | Pearson _r_ |
|---------------------|-------------|
| 005930.KS vs AAPL   | -0.316      |
| 005930.KS vs NVDA   | -0.191      |
| AAPL vs NVDA        |  0.733      |

## Key takeaways
- Samsung's price history is quoted in KRW and averages ₩66.5K, while the U.S. tech names trade on a much lower nominal scale but show wider percentage swings (e.g., NVDA ranges from $40 to $193).
- NVDA posts the largest trading volumes and shows a strong positive correlation with AAPL (0.73), hinting at similar market drivers during the observed period. Samsung's movements are weakly negatively correlated with the U.S. tickers.
- The helper script offers a quick way to regenerate these figures and can serve as a template for deeper analyses (moving averages, returns, etc.).

## Reproducing the analysis
1. Ensure Python 3.11+ is available in your environment.
2. Run the helper script:
   ```bash
   python analysis.py
   ```
   The script prints the summaries shown above and can be extended with additional indicators as needed.

For further analysis, consider augmenting the script with return calculations, volatility measures, or visualization tooling.
