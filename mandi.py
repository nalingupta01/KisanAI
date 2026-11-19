"""
KisanAI - Mandi Price Tracker (CSV-based version)
------------------------------------------------------
Reads mandi prices from a local CSV file instead of calling a live API.
This removes any dependency on data.gov.in API keys/signup working,
which makes the project fully self-contained and demo-safe.

FILE: mandi_prices.csv (same folder as this file)
COLUMNS: state, district, market, commodity, variety, arrival_date,
         min_price, max_price, modal_price

--------------------------------------------------------------------
HOW TO GET REAL DATA (recommended before your final submission):
--------------------------------------------------------------------
1. Go to https://www.data.gov.in/catalog/current-daily-price-various-
   commodities-various-markets-mandi  (no login needed for this step)
2. Click the "CSV" export button next to "Current Daily Price..."
3. Solve the captcha, download the CSV
4. Rename the downloaded file to mandi_prices.csv and replace the
   sample file in this project folder (keep the same column names,
   or adjust the COLUMN NAMES section below to match the real file)
5. Re-run the app - no code changes needed if columns match

A starter mandi_prices.csv with realistic sample data for all states/
crops used in this app is already included, so the app works out of
the box even before you swap in the real download.
--------------------------------------------------------------------
"""

import os
import pandas as pd

CSV_PATH = os.path.join(os.path.dirname(__file__), "mandi_prices.csv")


def get_mandi_prices(state=None, commodity=None, limit=50):
    """
    Reads mandi_prices.csv and returns a filtered pandas DataFrame.
    Returns an empty DataFrame if the file is missing or no rows match.
    """
    if not os.path.exists(CSV_PATH):
        return pd.DataFrame()

    try:
        df = pd.read_csv(CSV_PATH)
    except Exception:
        return pd.DataFrame()

    if state:
        df = df[df["state"].str.lower() == state.lower()]
    if commodity:
        df = df[df["commodity"].str.lower() == commodity.lower()]

    return df.head(limit)


INDIAN_STATES = [
    "Rajasthan", "Uttar Pradesh", "Madhya Pradesh", "Punjab", "Haryana",
    "Maharashtra", "Gujarat", "Bihar", "West Bengal", "Karnataka",
    "Tamil Nadu", "Andhra Pradesh", "Telangana",
]

COMMON_COMMODITIES = [
    "Wheat", "Rice", "Onion", "Potato", "Tomato", "Mustard",
    "Cotton", "Maize", "Gram", "Sugarcane",
]