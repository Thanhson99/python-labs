# python-labs

A personal collection of Python experiments and mini-projects.

## Project Structure

- `AI-search-engine/`: Search and report generation utilities.
- `basic-bot/`: Small bot and data analysis scripts.
- `box-browser/`: Browser window automation sample.
- `calculator-gradient-image/`: Image gradient processing script.
- `composio/`: Composio + OpenAI integration demos.
- `crypto-bot/`: Crypto tracking and Telegram bot utilities.
- `download-video/`: Video download script.
- `dropshipping-bot/`: Dropshipping research helpers.
- `exe/`: PyInstaller build output and executable experiments.
- `get-data/`: Data fetcher script.
- `nft-ai-bot/`: NFT and AI related automation script.
- `smart-contract/`: Solidity and web3 testing scripts.

## Security Notes

This repository may require API keys for local runs, but secrets must never be committed.

- Keep real keys only in local environment files.
- Use placeholder values in tracked files.
- Rotate any key that was previously exposed.

## Local Setup (General)

1. Create a virtual environment.
2. Install dependencies per project (`requirements.txt` where available).
3. Configure local environment values (`.env` / `config.ini`) with your own keys.
4. Run scripts from each project folder.

## Git Hygiene

A root `.gitignore` is included to exclude:

- `.env` files and local secret configs
- Python cache and virtual environments
- logs and local build artifacts

## Disclaimer

These are lab/demo projects and may need refactoring, tests, and production hardening before real-world use.
