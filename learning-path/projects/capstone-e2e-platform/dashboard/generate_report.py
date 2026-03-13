"""Generate markdown dashboard report from DB summary."""

from pathlib import Path

from app.repository import summary

OUT = Path(__file__).resolve().parent / "report.md"


def main() -> None:
    data = summary()
    content = "\n".join(
        [
            "# Capstone Dashboard",
            "",
            f"- queued: {data['queued']}",
            f"- processed: {data['processed']}",
        ]
    )
    OUT.write_text(content, encoding="utf-8")
    print(content)


if __name__ == "__main__":
    main()
