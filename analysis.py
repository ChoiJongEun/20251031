"""Utility script for summarizing the stock dataset in temp.csv."""
from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date, datetime
from math import sqrt
from statistics import mean
from typing import Dict, Iterable, List, Tuple, cast

DATA_FILE = "temp.csv"
TICKERS = ["005930.KS", "AAPL", "NVDA"]
METRICS = ["Close", "High", "Low", "Open", "Volume"]


def load_records(path: str = DATA_FILE) -> List[Dict[str, float | date | None]]:
    """Parse the CSV with its three-row header into a list of dictionaries."""
    with open(path, newline="") as f:
        reader = csv.reader(f)
        lvl1 = next(reader)
        lvl2 = next(reader)
        lvl3 = next(reader)
        rows = list(reader)

    columns: List[str] = []
    for i in range(len(lvl1)):
        l1 = lvl1[i].strip()
        l2 = lvl2[i].strip()
        l3 = lvl3[i].strip()
        if i == 0:
            columns.append(l3 or l2 or l1 or f"column_{i}")
            continue
        parts = [l1, l2]
        columns.append("_".join(p for p in parts if p))

    records: List[Dict[str, float | date | None]] = []
    for row in rows:
        entry: Dict[str, float | date | None] = {}
        for col, value in zip(columns, row):
            if col == "Date":
                entry[col] = datetime.strptime(value, "%Y-%m-%d").date()
            elif value:
                entry[col] = float(value)
            else:
                entry[col] = None
        records.append(entry)
    return records


@dataclass
class MetricSummary:
    mean: float
    minimum: float
    maximum: float


@dataclass
class TickerSummary:
    metrics: Dict[str, MetricSummary]


def summarize_records(
    records: Iterable[Dict[str, float | date | None]]
) -> Tuple[date, date, Dict[str, TickerSummary]]:
    """Return the coverage window and per-ticker summaries."""
    rows = list(records)
    start_date = cast(date, rows[0]["Date"])
    end_date = cast(date, rows[-1]["Date"])

    summaries: Dict[str, TickerSummary] = {}
    for ticker in TICKERS:
        metric_summaries: Dict[str, MetricSummary] = {}
        for metric in METRICS:
            key = f"{metric}_{ticker}"
            values = [float(r[key]) for r in rows if r[key] is not None]
            metric_summaries[metric] = MetricSummary(
                mean=mean(values), minimum=min(values), maximum=max(values)
            )
        summaries[ticker] = TickerSummary(metrics=metric_summaries)
    return start_date, end_date, summaries


def pearson(x: Iterable[float], y: Iterable[float]) -> float:
    xs = list(x)
    ys = list(y)
    mx = mean(xs)
    my = mean(ys)
    numerator = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    denominator = sqrt(sum((a - mx) ** 2 for a in xs) * sum((b - my) ** 2 for b in ys))
    return numerator / denominator if denominator else float("nan")


def correlation_matrix(
    records: Iterable[Dict[str, float | date | None]]
) -> List[Tuple[str, str, float]]:
    rows = list(records)
    results: List[Tuple[str, str, float]] = []
    for i, left in enumerate(TICKERS):
        for right in TICKERS[i + 1 :]:
            paired: List[Tuple[float, float]] = []
            for row in rows:
                left_value = row.get(f"Close_{left}")
                right_value = row.get(f"Close_{right}")
                if left_value is None or right_value is None:
                    continue
                paired.append((float(left_value), float(right_value)))
            if paired:
                lx, ry = zip(*paired)
                results.append((left, right, pearson(lx, ry)))
    return results


def format_number(value: float, digits: int = 2) -> str:
    return f"{value:,.{digits}f}" if digits else f"{int(round(value)):,}"


def main() -> None:
    records = load_records()
    start, end, summaries = summarize_records(records)
    print(f"Date range: {start} – {end} ({len(records)} trading days)")

    print("\nPrice summary (mean / min / max):")
    for ticker in TICKERS:
        stats = summaries[ticker].metrics["Close"]
        print(
            f"  {ticker}: {format_number(stats.mean)} / "
            f"{format_number(stats.minimum)} / {format_number(stats.maximum)}"
        )

    print("\nVolume summary (mean / min / max):")
    for ticker in TICKERS:
        stats = summaries[ticker].metrics["Volume"]
        print(
            f"  {ticker}: {format_number(stats.mean, 0)} / "
            f"{format_number(stats.minimum, 0)} / {format_number(stats.maximum, 0)}"
        )

    print("\nClose-price correlations:")
    for left, right, corr in correlation_matrix(records):
        print(f"  {left} vs {right}: {corr:.3f}")


if __name__ == "__main__":
    main()
