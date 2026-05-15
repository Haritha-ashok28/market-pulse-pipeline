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

for sector, stocks in tickers.items():
        for i in stocks:
            params = {
                "function": "TIME_SERIES_DAILY",
                "symbol": i,
                "apikey": API_KEY
                }
            try:
                response = requests.get(BASE_URL,params=params)
                data = response.json()
                os.makedirs(f"data/{sector}", exist_ok=True)
                with open(f"data/{sector}/{i}.json", "w") as f:
                    json.dump(data,f)
                time.sleep(12)
                logger.info(f"{i} fetched successfully")
            except Exception as e:
                logger.error(f"{i} failed: {e}")
                continue