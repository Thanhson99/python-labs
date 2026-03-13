# python-labs

Reorganized Python lab workspace with a unified learning site.

## New Structure

- `services/`: all lab projects grouped as independent services.
- `site/`: static learning portal (cheat sheet + roadmap + service catalog).
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

## Auto Runtime Behavior

- Auto-detects available Python command (`python3`, `python`, or `py -3` on Windows).
- Auto-checks if requested port is in use.
- If port is busy, automatically increments to the next free port.
- Rebuilds `site/data/catalog.json` from `services/` before serving.

## Manual Build Only

```bash
python3 scripts/build_site.py
```

## Notes

- Keep secrets in local env files only; never commit real keys.
- This repo is for learning/lab use; each service may need additional refactor/tests for production.
