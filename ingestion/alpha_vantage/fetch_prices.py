import logging
logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/pipeline.log"),
            logging.StreamHandler()
        ]
    )
logger = logging.getLogger(__name__)

import requests
import time
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

BASE_URL = "https://www.alphavantage.co/query"

tickers = {
        "tech": ["NVDA", "GOOGL", "AAPL", "AMZN", "MSFT"],
        "finance": ["JPM", "SPGI", "GS", "BAC", "V"],
        "healthcare": ["JNJ", "UNH", "PFE", "ABBV", "MRK"]
    }

def save_data(ticker, sector, data):
    os.makedirs(f"data/{sector}", exist_ok=True)
    with open(f"data/{sector}/{ticker}.json", "w") as f:
        json.dump(data, f)


def fetch_prices(ticker, sector):
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ticker,
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()


def run_pipeline():
    for sector, stocks in tickers.items():
        for ticker in stocks:
            try:
                data = fetch_prices(ticker, sector)
                save_data(ticker, sector, data)
                time.sleep(12)
                logger.info(f"{ticker} fetched successfully")
            except Exception as e:
                logger.error(f"{ticker} failed: {e}")
                continue


if __name__ == "__main__":
    run_pipeline()