import os
import requests
import psycopg2
from dotenv import load_dotenv
from datetime import datetime, timedelta

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
    
    for ticker in TICKERS:
        print(f"Fetch data for: {ticker}...")

        # Construct the API URL with dynamic dates and ticker
        url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{START_DATE}/{END_DATE}?adjusted=true&sort=asc&apiKey={API_KEY}"
        
        # Execute the network request
        response = requests.get(url)
        data = response.json()
        
        # Check if the API returned valid results
        if "results" in data:
            for day in data["results"]:
                # Mapping API response fields:
                # t = timestamp (Unix), h = high, l = low, o = open, c = close
                cur.execute("""
                    INSERT INTO raw.TICKER (ticker_name, unix_time, high, low, start_time, close_time)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (ticker_name, unix_time) DO NOTHING;
                """, (ticker, day['t'], day['h'], day['l'], day['o'], day['c']))
            
            # Commit changes for each ticker to ensure data is saved
            conn.commit()
            print(f"done for {ticker}!")
        else:
            print(f"could not find data for {ticker}")

    # Clean up: close the cursor and connection
    cur.close()
    conn.close()

if __name__ == "__main__":
    get_stock_data()