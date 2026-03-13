# AI Search Engine Lab

## Overview
This project searches algorithm resources, extracts code snippets, measures execution time, and generates a report.

## Main Components
- `main.py`: orchestrates the full workflow
- `core/search.py`: fetches URLs via search API
- `core/scraper.py`: extracts code blocks from pages
- `core/evaluator.py`: measures execution time
- `core/reporter.py`: writes report output
- `data/`: generated artifacts (`algorithms.json`, `report.txt`)

## Run
```bash
pip install -r requirements.txt
python main.py
```

## Output
- `data/algorithms.json`
- `data/report.txt`

## Notes
- API keys should be provided via environment variables.
- Scraped pages may include noisy/non-runnable snippets.
