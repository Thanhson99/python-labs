# python-labs

Reorganized Python lab workspace with multiple learning sites and GitHub Pages friendly entrypoints.

Live site: https://thanhson99.github.io/python-labs/

## New Structure

- `services/`: all lab projects grouped as independent services.
- `site/`: static portal with learning sites, including a GitHub Pages compatible interview-prep site.
- `index.html`: root redirect entry so GitHub Pages can open the portal from repo root.
- `learning-path/`: hands-on code labs mapped to roadmap stages/phases.
- `scripts/`: cross-platform scripts to build and run the site.
- `docs/`: markdown versions of roadmap and cheat sheet.
- `archive/`: legacy/experimental folders not used for the main learning flow.

## Services

- `services/AI-search-engine`
- `services/basic-bot`
- `services/box-browser`
- `services/calculator-gradient-image`
- `services/composio`
- `services/crypto-bot`
- `services/download-video`
- `services/dropshipping-bot`
- `services/get-data`
- `services/nft-ai-bot`
- `services/smart-contract`

## Build and Run Learning Site

### macOS / Linux

```bash
./scripts/run_site.sh
```

Optional custom start port:

```bash
./scripts/run_site.sh 8080
```

### Windows PowerShell

```powershell
./scripts/run_site.ps1
```

Optional custom start port:

```powershell
./scripts/run_site.ps1 -StartPort 8080
```

### Windows CMD

```cmd
scripts\run_site.cmd
```

## Open the Sites

Public GitHub Pages:

- `https://thanhson99.github.io/python-labs/` -> live static entry page

- `http://127.0.0.1:<PORT>/` -> track selector landing page
- `http://127.0.0.1:<PORT>/foundation.html` -> huge foundation cheatsheet + roadmap
- `http://127.0.0.1:<PORT>/advanced.html` -> advanced architecture roadmap + Java/Python stack mapping
- `http://127.0.0.1:<PORT>/interview.html` -> static interview topic catalog and preparation ladders
- `http://127.0.0.1:<PORT>/interview-sources.html` -> static interview source hub for Vietnamese and English learning links
- `http://127.0.0.1:<PORT>/code-questions.html` -> code-only static JSON question bank with answers/explanations
- `http://127.0.0.1:<PORT>/code-questions.html?set=advanced` -> 100+ advanced code questions
- `http://127.0.0.1:<PORT>/code-questions.html?set=automation` -> automation code set
- `http://127.0.0.1:<PORT>/code-questions.html?set=backend` -> backend/data code set
- `http://127.0.0.1:<PORT>/code-questions.html?set=ai-ml` -> AI/ML code set
- `http://127.0.0.1:<PORT>/code-questions.html?set=system-design` -> system design code set
- `http://127.0.0.1:<PORT>/interview-role-questions.html` -> interview-only question bank for fresher/intermediate/senior/bilingual

Each roadmap card includes an `Example code` path under `learning-path/` so you can open matching code while reading the site.
Roadmap cards also include:
- progress checkbox (saved in browser local storage)
- `Run example` button (runs local `.py` sample and shows output in-page)

## GitHub Pages Static Deployment

If GitHub Pages points to the repository root, the top-level `index.html` will redirect users into `site/index.html`.
That means you do not need to move the whole static portal out of `site/` just to make the root URL work.

The interview-prep pages are designed to work as a pure static site:

- `site/interview.html`
- `site/interview-sources.html`
- `site/interview-questions.html`
- `site/code-questions.html`
- `site/interview-role-questions.html`
- `site/data/interview-catalog.json`
- `site/data/interview-basic-questions.json`
- `site/data/interview-intermediate-questions.json`
- `site/data/interview-advanced-questions.json`
- `site/data/interview-question-sets.json`
- `site/data/interview-code-sets.json`
- `site/data/interview-role-sets.json`
- `site/data/interview-sources.json`
- `site/data/interview-automation-questions.json`
- `site/data/interview-backend-questions.json`
- `site/data/interview-ai-ml-questions.json`
- `site/data/interview-system-design-questions.json`
- `site/data/interview-bilingual-questions.json`

This means you can publish that part to GitHub Pages without requiring Python, a local server API, or a database.
The existing `foundation.html` and `advanced.html` pages still support local interactive example execution through `POST /api/run-example`, so that specific feature is local-only.

The interview site is designed to remain fully static on GitHub Pages:
- no Python runtime required
- no database required
- no local API required
- all content is loaded from JSON in the browser

## Contributions

If you want to contribute more interview question sets, please send them by email to `sonvi10101999@gmail.com`.
Suggested contribution formats:
- JSON question sets matching the existing schema in `site/data/`
- Vietnamese or English interview questions
- code-comparison, optimization, trap, and system-design style questions

## Auto Runtime Behavior

- Auto-detects available Python command (`python3`, `python`, or `py -3` on Windows).
- Auto-checks if requested port is in use.
- If port is busy, automatically increments to the next free port.
- Rebuilds all track data from `services/` before serving:
  - `site/data/catalog.json`
  - `site/data/foundation.json`
  - `site/data/advanced.json`
- Starts interactive site API:
  - `POST /api/run-example` for running local learning examples

## Manual Build Only

```bash
python3 scripts/build_site.py
```

## Learning-Path Quality Gate

Run all core learning-path checks (compile + selected samples + pytest stage):

```bash
python3 scripts/verify_learning_path.py
```

## Extended Learning Content

- `learning-path/foundation/extras/`: additional foundational examples (decorators, context managers, regex, argparse, logging, typing, etc.).
- `learning-path/database/`: practical database track (PostgreSQL local, Alembic flow, indexing/query plans, isolation, pooling).
- `learning-path/advanced/extras/`: distributed pattern examples with tests (idempotency, retry/backoff, circuit breaker, saga, outbox, contracts).
- `learning-path/projects/capstone-e2e-platform/`: end-to-end capstone (API + queue + DB + metrics + dashboard + deploy templates + tests).

## Notes

- Keep secrets in local env files only; never commit real keys.
- This repo is for learning/lab use; each service may need additional refactor/tests for production.
