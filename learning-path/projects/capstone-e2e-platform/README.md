# Capstone E2E Platform

End-to-end learning project with:
- API ingestion (`app/api.py`)
- queue + persistence (`app/repository.py`)
- worker processing (`app/worker.py`)
- metrics snapshot (`app/metrics.py`)
- dashboard report (`dashboard/generate_report.py`)
- deployment templates (`infra/`)
- tests (`tests/`)

## Run

1. Initialize schema:
```bash
python3 app/repository.py
```

2. In terminal A, run API:
```bash
python3 app/api.py
```

3. In terminal B, submit task:
```bash
curl -s -X POST http://127.0.0.1:9200/tasks -H 'content-type: application/json' --data '{"name":"reconcile-orders"}'
```

4. Process queue:
```bash
python3 app/worker.py
```

5. Generate dashboard:
```bash
python3 dashboard/generate_report.py
```

6. Run tests:
```bash
pytest -q tests
```
