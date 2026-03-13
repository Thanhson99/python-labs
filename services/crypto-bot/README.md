# Crypto Bot

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env
```

## Structure
- `bot/`: Telegram bot handlers and commands
- `core/`: shared utilities
- `data/`: static source/coin configuration
- `modules/`: domain modules (`crypto`, `news`, `whale`)
- `tests/`: test scripts
- `main.py`: scheduler entrypoint
- `run.sh`: background runner

## Run
```bash
python main.py
```

or

```bash
./run.sh
```

## Notes
- Add real API keys in `.env`.
- Use test channels/chats before production use.
