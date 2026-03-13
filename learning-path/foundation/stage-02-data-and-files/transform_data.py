"""Stage 02: data transformation and file IO."""

import json
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent
INPUT_FILE = BASE / "input.json"
OUTPUT_FILE = BASE / "summary.json"


def main() -> None:
    payload = json.loads(INPUT_FILE.read_text(encoding="utf-8"))
    events = payload["events"]

    kind_counts = Counter(event["kind"] for event in events)
    success_rate = sum(1 for event in events if event["ok"]) / len(events)

    summary = {
        "total_events": len(events),
        "kind_counts": dict(kind_counts),
        "success_rate": round(success_rate, 3),
    }

    OUTPUT_FILE.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(summary)


if __name__ == "__main__":
    main()
