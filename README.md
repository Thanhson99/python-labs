# python-labs

Reorganized Python lab workspace with dual learning sites.

## New Structure

- `services/`: all lab projects grouped as independent services.
- `site/`: static portal with two separated learning sites.
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

## Open the Two Sites

- `http://127.0.0.1:<PORT>/` -> track selector landing page
- `http://127.0.0.1:<PORT>/foundation.html` -> huge foundation cheatsheet + roadmap
- `http://127.0.0.1:<PORT>/advanced.html` -> advanced architecture roadmap + Java/Python stack mapping

Each roadmap card includes an `Example code` path under `learning-path/` so you can open matching code while reading the site.
Roadmap cards also include:
- progress checkbox (saved in browser local storage)
- `Run example` button (runs local `.py` sample and shows output in-page)

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

## Notes

- Keep secrets in local env files only; never commit real keys.
- This repo is for learning/lab use; each service may need additional refactor/tests for production.
