# ============================================
# STEP 3: DATA WAREHOUSE
# ============================================
# This file saves processed stock data
# into MySQL database for structured querying
# Think of this as building a library where
# all your data is organized and searchable
# ============================================

import os
import sys
import pandas as pd
import mysql.connector
from mysql.connector import Error

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_CONFIG, PROCESSED_DATA_PATH


def create_connection():
    """
    Connect to MySQL database
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            print("✅ Connected to MySQL!")
            return conn
    except Error as e:
        print(f"❌ Connection failed: {e}")
        return None


def create_database():
    """
    Create the stock_warehouse database
    and all required tables
    """
    print("\n🏗️ Setting up database...")

    # Connect without database first
    conn = mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password']
    )
    cursor = conn.cursor()

    # Create database
    cursor.execute("CREATE DATABASE IF NOT EXISTS stock_warehouse")
    cursor.execute("USE stock_warehouse")

    # Create main stock data table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_prices (
            id INT AUTO_INCREMENT PRIMARY KEY,
            symbol VARCHAR(20),
            date DATE,
            open_price DECIMAL(10,2),
            high_price DECIMAL(10,2),
            low_price DECIMAL(10,2),
            close_price DECIMAL(10,2),
            volume BIGINT,
            daily_return_pct DECIMAL(10,2),
            ma_7 DECIMAL(10,2),
            ma_30 DECIMAL(10,2),
            volatility_pct DECIMAL(10,2),
            price_range DECIMAL(10,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY unique_stock_date (symbol, date)
        )
    """)

    # Create summary table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_summary (
            id INT AUTO_INCREMENT PRIMARY KEY,
            symbol VARCHAR(20) UNIQUE,
            company_name VARCHAR(100),
            total_records INT,
            avg_close_price DECIMAL(10,2),
            max_price DECIMAL(10,2),
            min_price DECIMAL(10,2),
            avg_daily_return DECIMAL(10,2),
            avg_volatility DECIMAL(10,2),
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Database and tables created!")


def load_processed_data():
    """
    Read processed CSV files from data/processed folder
    """
    print("\n📖 Loading processed data...")

    import glob
    # Find the CSV file in processed folder
    csv_files = glob.glob(f"{PROCESSED_DATA_PATH}/all_stocks/*.csv")

    if not csv_files:
        print("❌ No processed data found!")
        print("Run process_data.py first!")
        return None

    # Read all CSV files
    dfs = []
    for f in csv_files:
        df = pd.read_csv(f)
        dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)
    print(f"✅ Loaded {len(df)} records")
    return df


def insert_stock_data(df):
    """
    Insert stock price data into MySQL
    """
    print("\n💾 Inserting data into MySQL...")

    conn = create_connection()
    if not conn:
        return

    cursor = conn.cursor()
    cursor.execute("USE stock_warehouse")

    # Insert query
    query = """
        INSERT IGNORE INTO stock_prices
        (symbol, date, open_price, high_price, low_price,
         close_price, volume, daily_return_pct, ma_7, ma_30,
         volatility_pct, price_range)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Convert dataframe to list of tuples
    records = []
    for _, row in df.iterrows():
        records.append((
            row['Symbol'],
            row['Date'],
            row['Open'],
            row['High'],
            row['Low'],
            row['Close'],
            int(row['Volume']),
            row.get('Daily_Return_Pct', 0),
            row.get('MA_7', 0),
            row.get('MA_30', 0),
            row.get('Volatility_Pct', 0),
            row.get('Price_Range', 0)
        ))

    # Insert in batches of 100
    batch_size = 100
    total = len(records)
    inserted = 0

    for i in range(0, total, batch_size):
        batch = records[i:i + batch_size]
        cursor.executemany(query, batch)
        conn.commit()
        inserted += len(batch)
        print(f"   Inserted {inserted}/{total} records...")

    cursor.close()
    conn.close()
    print(f"✅ Successfully inserted {inserted} records!")


def create_summary():
    """
    Create a summary for each company
    showing key statistics
    """
    print("\n📊 Creating stock summary...")

    conn = create_connection()
    if not conn:
        return

    cursor = conn.cursor()
    cursor.execute("USE stock_warehouse")

    # Company names mapping
    company_names = {
        "TCS.NS": "Tata Consultancy Services",
        "INFY.NS": "Infosys",
        "WIPRO.NS": "Wipro",
        "RELIANCE.NS": "Reliance Industries",
        "HDFCBANK.NS": "HDFC Bank",
        "ICICIBANK.NS": "ICICI Bank",
        "HINDUNILVR.NS": "Hindustan Unilever",
        "ITC.NS": "ITC Limited",
        "SBIN.NS": "State Bank of India",
        "BAJFINANCE.NS": "Bajaj Finance"
    }

    # Calculate summary for each company
    summary_query = """
        INSERT INTO stock_summary
        (symbol, company_name, total_records, avg_close_price,
         max_price, min_price, avg_daily_return, avg_volatility)
        SELECT
            symbol,
            %s as company_name,
            COUNT(*) as total_records,
            ROUND(AVG(close_price), 2) as avg_close_price,
            ROUND(MAX(high_price), 2) as max_price,
            ROUND(MIN(low_price), 2) as min_price,
            ROUND(AVG(daily_return_pct), 2) as avg_daily_return,
            ROUND(AVG(volatility_pct), 2) as avg_volatility
        FROM stock_prices
        WHERE symbol = %s
        GROUP BY symbol
        ON DUPLICATE KEY UPDATE
            total_records = VALUES(total_records),
            avg_close_price = VALUES(avg_close_price),
            max_price = VALUES(max_price),
            min_price = VALUES(min_price),
            avg_daily_return = VALUES(avg_daily_return),
            avg_volatility = VALUES(avg_volatility),
            updated_at = CURRENT_TIMESTAMP
    """

    for symbol, name in company_names.items():
        cursor.execute(summary_query, (name, symbol))

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Summary created!")


def setup_warehouse():
    """
    Main function - runs entire warehouse setup
    """
    print("\n" + "="*50)
    print("🏗️ SETTING UP DATA WAREHOUSE")
    print("="*50)

    # Step 1 - Create database and tables
    create_database()

    # Step 2 - Load processed data
    df = load_processed_data()
    if df is None:
        return

    # Step 3 - Insert into MySQL
    insert_stock_data(df)

    # Step 4 - Create summary
    create_summary()

    print("\n" + "="*50)
    print("✅ DATA WAREHOUSE SETUP COMPLETE!")
    print("="*50)


if __name__ == "__main__":
    setup_warehouse()