import os
from dotenv import load_dotenv

# Load environment variables for Google Trends
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

TREND_FETCH_INTERVAL = int(os.getenv("GOOGLE_TREND_FETCH_INTERVAL", 3))  # Default: 3 months
REGION = os.getenv("GOOGLE_REGION", "US")  # Default: US
