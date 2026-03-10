#!/bin/bash

# Define project root
PROJECT_NAME="dropshipping-bot"
mkdir -p $PROJECT_NAME

# Define subdirectories
mkdir -p $PROJECT_NAME/{configs,logs,services,utils}

# Create .env file (global settings)
cat <<EOL > $PROJECT_NAME/.env
# Global environment variables
DEBUG=True
EOL

# Create configs folder (to store different configurations)
mkdir -p $PROJECT_NAME/configs
touch $PROJECT_NAME/configs/__init__.py
cat <<EOL > $PROJECT_NAME/configs/base_config.py
import os
from dotenv import load_dotenv

# Load global .env file
load_dotenv()

DEBUG = os.getenv("DEBUG", "False").lower() == "true"
EOL

# Create log folder
mkdir -p $PROJECT_NAME/logs

# Create utils folder (helper functions)
mkdir -p $PROJECT_NAME/utils
touch $PROJECT_NAME/utils/__init__.py
cat <<EOL > $PROJECT_NAME/utils/logger.py
import logging

def setup_logger(name):
    """Setup a logger with a specific name."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger
EOL

# Create services folder (each service has its own config and logic)
mkdir -p $PROJECT_NAME/services/{google_trends,taobao,amazon}

# Create Google Trends service
cat <<EOL > $PROJECT_NAME/services/google_trends/config.py
import os
from dotenv import load_dotenv

# Load environment variables for Google Trends
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

TREND_FETCH_INTERVAL = int(os.getenv("GOOGLE_TREND_FETCH_INTERVAL", 3))  # Default: 3 months
REGION = os.getenv("GOOGLE_REGION", "US")  # Default: US
EOL

cat <<EOL > $PROJECT_NAME/services/google_trends/google_trends.py
from services.google_trends.config import TREND_FETCH_INTERVAL, REGION
from utils.logger import setup_logger

logger = setup_logger("GoogleTrends")

def fetch_trends():
    """Fetch trending data from Google Trends"""
    logger.info(f"Fetching Google Trends for {TREND_FETCH_INTERVAL} months in {REGION}")

if __name__ == "__main__":
    fetch_trends()
EOL

# Final message
echo "✅ Project structure created successfully!"
