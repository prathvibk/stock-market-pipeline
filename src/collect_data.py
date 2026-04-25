# ============================================
# STEP 1: DATA COLLECTION
# ============================================
# This file downloads real stock market data
# from Yahoo Finance API for 10 Indian companies
# and saves it as CSV files locally
# ============================================

import yfinance as yf
import pandas as pd
import os
import sys

# Import our config settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import STOCKS, START_DATE, END_DATE, RAW_DATA_PATH


def create_folders():
    """
    Create folders to store raw data if they don't exist
    """
    os.makedirs(RAW_DATA_PATH, exist_ok=True)
    print(f"✅ Folder ready: {RAW_DATA_PATH}")


def download_stock_data(symbol):
    """
    Download historical stock data for one company
    
    symbol = stock ticker like "TCS.NS"
    Returns a pandas DataFrame with columns:
    Date, Open, High, Low, Close, Volume
    """
    print(f"📥 Downloading data for {symbol}...")
    
    try:
        # Download data from Yahoo Finance
        stock = yf.Ticker(symbol)
        df = stock.history(start=START_DATE, end=END_DATE)
        
        # Check if we got data
        if df.empty:
            print(f"⚠️ No data found for {symbol}")
            return None
        
        # Reset index to make Date a column
        df = df.reset_index()
        
        # Keep only important columns
        df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        
        # Add company symbol column
        df['Symbol'] = symbol
        
        # Clean the date format
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        
        # Round prices to 2 decimal places
        df['Open'] = df['Open'].round(2)
        df['High'] = df['High'].round(2)
        df['Low'] = df['Low'].round(2)
        df['Close'] = df['Close'].round(2)
        
        print(f"✅ Got {len(df)} records for {symbol}")
        return df
        
    except Exception as e:
        print(f"❌ Error downloading {symbol}: {e}")
        return None


def save_to_csv(df, symbol):
    """
    Save stock data to CSV file
    
    Each company gets its own CSV file
    Example: data/raw/TCS.NS.csv
    """
    # Create filename from symbol
    filename = symbol.replace(".", "_") + ".csv"
    filepath = os.path.join(RAW_DATA_PATH, filename)
    
    # Save to CSV
    df.to_csv(filepath, index=False)
    print(f"💾 Saved to {filepath}")


def collect_all_stocks():
    """
    Main function - downloads data for ALL 10 companies
    and saves each one as a CSV file
    """
    print("\n" + "="*50)
    print("🚀 STARTING STOCK DATA COLLECTION")
    print("="*50)
    print(f"📅 Period: {START_DATE} to {END_DATE}")
    print(f"📊 Companies: {len(STOCKS)}")
    print("="*50 + "\n")
    
    # Create folders first
    create_folders()
    
    # Track success and failures
    successful = []
    failed = []
    
    # Loop through each stock and download
    for symbol in STOCKS:
        df = download_stock_data(symbol)
        
        if df is not None:
            save_to_csv(df, symbol)
            successful.append(symbol)
        else:
            failed.append(symbol)
    
    # Print summary
    print("\n" + "="*50)
    print("📊 COLLECTION COMPLETE!")
    print("="*50)
    print(f"✅ Successfully downloaded: {len(successful)} stocks")
    print(f"❌ Failed: {len(failed)} stocks")
    
    if failed:
        print(f"Failed stocks: {failed}")
    
    print("\nFiles saved in:", RAW_DATA_PATH)
    print("="*50)


# Run when this file is executed directly
if __name__ == "__main__":
    collect_all_stocks()