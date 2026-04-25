# ============================================
# STEP 4: ANALYTICS
# ============================================
# This file runs SQL queries on MySQL database
# to generate business insights like:
# - Top performing stocks
# - Most volatile stocks
# - Best and worst days
# - Sector trends
# ============================================

import os
import sys
import mysql.connector
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_CONFIG


def get_connection():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn


def run_query(query, title):
    """
    Run a SQL query and print results nicely
    """
    print(f"\n{'='*50}")
    print(f"📊 {title}")
    print('='*50)

    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()

    print(df.to_string(index=False))
    return df


def top_performing_stocks():
    """
    Which stock gave best average daily return?
    """
    query = """
        SELECT
            symbol,
            ROUND(AVG(daily_return_pct), 2) as avg_daily_return,
            ROUND(MAX(close_price), 2) as max_price,
            ROUND(MIN(close_price), 2) as min_price,
            COUNT(*) as trading_days
        FROM stock_prices
        GROUP BY symbol
        ORDER BY avg_daily_return DESC
    """
    return run_query(query, "TOP PERFORMING STOCKS BY AVERAGE DAILY RETURN")


def most_volatile_stocks():
    """
    Which stock is most volatile?
    High volatility = risky but potentially high reward
    """
    query = """
        SELECT
            symbol,
            ROUND(AVG(volatility_pct), 2) as avg_volatility,
            ROUND(MAX(volatility_pct), 2) as max_volatility,
            ROUND(MIN(volatility_pct), 2) as min_volatility
        FROM stock_prices
        GROUP BY symbol
        ORDER BY avg_volatility DESC
    """
    return run_query(query, "MOST VOLATILE STOCKS")


def best_worst_days():
    """
    What were the best and worst trading days?
    """
    query = """
        SELECT
            symbol,
            date,
            close_price,
            daily_return_pct
        FROM stock_prices
        ORDER BY daily_return_pct DESC
        LIMIT 10
    """
    run_query(query, "TOP 10 BEST TRADING DAYS")

    query2 = """
        SELECT
            symbol,
            date,
            close_price,
            daily_return_pct
        FROM stock_prices
        ORDER BY daily_return_pct ASC
        LIMIT 10
    """
    return run_query(query2, "TOP 10 WORST TRADING DAYS")


def monthly_trends():
    """
    How did stocks perform month by month?
    """
    query = """
        SELECT
            symbol,
            DATE_FORMAT(date, '%Y-%m') as month,
            ROUND(AVG(close_price), 2) as avg_price,
            ROUND(AVG(daily_return_pct), 2) as avg_return,
            ROUND(AVG(volatility_pct), 2) as avg_volatility
        FROM stock_prices
        GROUP BY symbol, month
        ORDER BY symbol, month
        LIMIT 20
    """
    return run_query(query, "MONTHLY TRENDS")


def stock_comparison():
    """
    Compare all stocks side by side
    """
    query = """
        SELECT
            s.symbol,
            s.company_name,
            s.avg_close_price,
            s.max_price,
            s.min_price,
            s.avg_daily_return,
            s.avg_volatility,
            s.total_records
        FROM stock_summary s
        ORDER BY avg_daily_return DESC
    """
    return run_query(query, "COMPLETE STOCK COMPARISON")


def run_analytics():
    """
    Main function - runs all analytics
    """
    print("\n" + "="*50)
    print("🔍 STARTING STOCK MARKET ANALYTICS")
    print("="*50)

    # Run all analyses
    top_performing_stocks()
    most_volatile_stocks()
    best_worst_days()
    monthly_trends()
    stock_comparison()

    print("\n" + "="*50)
    print("✅ ANALYTICS COMPLETE!")
    print("="*50)


if __name__ == "__main__":
    run_analytics()