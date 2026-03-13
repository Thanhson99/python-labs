"""CLI data toolkit project example."""

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--status", default="active")
    args = parser.parse_args()

    rows = json.loads(Path(args.input).read_text(encoding="utf-8"))
    filtered = [row for row in rows if row["status"] == args.status]
    avg = sum(row["score"] for row in filtered) / max(len(filtered), 1)
    print({"count": len(filtered), "avg_score": round(avg, 2)})


if __name__ == "__main__":
    main()
