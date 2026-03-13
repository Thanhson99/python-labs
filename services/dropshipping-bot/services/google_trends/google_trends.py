from services.google_trends.config import TREND_FETCH_INTERVAL, REGION
from utils.logger import setup_logger

logger = setup_logger("GoogleTrends")

def fetch_trends():
    """Fetch trending data from Google Trends"""
    logger.info(f"Fetching Google Trends for {TREND_FETCH_INTERVAL} months in {REGION}")

if __name__ == "__main__":
    fetch_trends()
