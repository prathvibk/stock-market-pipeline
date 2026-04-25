# ============================================
# STOCK MARKET DATA PIPELINE - CONFIGURATION
# ============================================

import os

# --- JAVA & HADOOP SETTINGS ---
# These tell PySpark where Java and Hadoop are installed
os.environ['JAVA_HOME'] = r'C:\Progra~1\ECLIPS~1\JDK-11~1.7-H'
os.environ['HADOOP_HOME'] = r'C:\hadoop'
os.environ['PATH'] = (
    r'C:\Progra~1\ECLIPS~1\JDK-11~1.7-H\bin' + ';' +
    r'C:\hadoop\bin' + ';' +
    r'C:\spark\spark-3.5.0-bin-hadoop3\bin' + ';' +
    os.environ['PATH']
)

# --- STOCK SETTINGS ---
# These are the 10 Indian companies we will track
STOCKS = [
    "TCS.NS",       # Tata Consultancy Services
    "INFY.NS",      # Infosys
    "WIPRO.NS",     # Wipro
    "RELIANCE.NS",  # Reliance Industries
    "HDFCBANK.NS",  # HDFC Bank
    "ICICIBANK.NS", # ICICI Bank
    "HINDUNILVR.NS",# Hindustan Unilever
    "ITC.NS",       # ITC Limited
    "SBIN.NS",      # State Bank of India
    "BAJFINANCE.NS" # Bajaj Finance
]

# --- TIME PERIOD ---
# How much historical data to collect
START_DATE = "2024-01-01"
END_DATE = "2025-12-31"

# --- DATABASE SETTINGS ---
# Your MySQL connection details
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "prathvi@123",  # Change this
    "database": "stock_warehouse"
}

# --- FOLDER PATHS ---
# Where to save raw data and visualizations
RAW_DATA_PATH = "data/raw"
PROCESSED_DATA_PATH = "data/processed"
VISUALIZATION_PATH = "visualizations"

# --- SPARK SETTINGS ---
SPARK_APP_NAME = "StockMarketPipeline"
SPARK_MASTER = "local[*]"  # Use all CPU cores