"""Phase G: latency metric aggregation sample."""


def percentile(values: list[float], p: float) -> float:
    ordered = sorted(values)
    idx = int((len(ordered) - 1) * p)
    return ordered[idx]


if __name__ == "__main__":
    latencies = [0.12, 0.18, 0.24, 0.08, 0.31, 0.15, 0.11]
    print({"p50": percentile(latencies, 0.50), "p95": percentile(latencies, 0.95)})
