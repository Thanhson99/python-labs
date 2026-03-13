"""CSV read/write with DictReader and DictWriter."""

from pathlib import Path
import csv

BASE = Path(__file__).resolve().parent
IN_FILE = BASE / "in.csv"
OUT_FILE = BASE / "out.csv"


def main() -> None:
    rows = []
    with IN_FILE.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["score"] = str(int(row["score"]) + 1)
            rows.append(row)

    with OUT_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "score"])
        writer.writeheader()
        writer.writerows(rows)

    print(rows)


if __name__ == "__main__":
    main()
