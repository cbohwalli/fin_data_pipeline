import os
import requests
import psycopg2
from dotenv import load_dotenv
from datetime import datetime, timedelta
from psycopg2.extras import Json 

# --- Configuration & Environment ---
# Load environment variables from a .env file
load_dotenv()

# Retrieve credentials and API keys
API_KEY = os.getenv("POLYGON_API_KEY")
DB_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@db:5432/{os.getenv('DB_NAME')}"

# List of stocks to track
TICKERS = ["AAPL", "GOOGL", "ORCL", "META", "MSFT"]

# --- Dynamic Date Calculation ---
# Set the end date to today's date
today = datetime.now()
END_DATE = today.strftime("%Y-%m-%d")

# Set the start date to exactly two years ago (730 days)
two_years_ago = today - timedelta(days=730)
START_DATE = two_years_ago.strftime("%Y-%m-%d")

def get_stock_data():
    """
    Connects to the database, fetches stock aggregates from Polygon.io,
    and saves them to the TICKER table.
    """

    # Initialize database connection
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    received_at = datetime.now()

    for ticker in TICKERS:
        print(f"Fetch data for: {ticker}...")

        # Construct the API URL with dynamic dates and ticker
        url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{START_DATE}/{END_DATE}?adjusted=true&sort=asc&apiKey={API_KEY}"
        
        # Execute the network request
        response = requests.get(url)
        data = response.json()
        
        # Check if the API returned valid results
        if "results" in data:

            # We insert the ticker and the whole JSON response
            cur.execute("""
                INSERT INTO raw.TICKER_DATA (ticker_symbol, received_at, json_payload)
                VALUES (%s, %s, %s)
                ON CONFLICT (ticker_symbol, received_at) DO NOTHING;
            """, (ticker, received_at, Json(data)))
            
            conn.commit()
            print(f"done for {ticker}!")
        else:
            print(f"could not find data for {ticker}")

    # Clean up: close the cursor and connection
    cur.close()
    conn.close()

if __name__ == "__main__":
    get_stock_data()