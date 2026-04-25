# ============================================
# STEP 2: DATA PROCESSING WITH APACHE SPARK
# ============================================
# This file reads raw CSV files and uses
# Apache Spark to clean and transform data.
# We calculate:
# - Moving averages (7 day, 30 day)
# - Daily returns (profit/loss %)
# - Price volatility
# - Trading volume trends
# ============================================

# ============================================
# STEP 2: DATA PROCESSING WITH APACHE SPARK
# ============================================
import os
import sys

os.environ['JAVA_HOME'] = r'C:\Program Files\Eclipse Adoptium\jdk-11.0.30.7-hotspot'
#os.environ['HADOOP_HOME'] = r'C:\hadoop'
os.environ['HADOOP_HOME'] = r'C:\hadoop'
os.environ['HADOOP_CONF_DIR'] = r'C:\hadoop\etc\hadoop'
os.environ['hadoop.home.dir'] = r'C:\hadoop'
os.environ['SPARK_HOME'] = r'C:\spark\spark-3.5.0-bin-hadoop3'
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
os.environ['PATH'] = (
    r'C:\Program Files\Eclipse Adoptium\jdk-11.0.30.7-hotspot\bin' + ';' +
    r'C:\hadoop\bin' + ';' +
    r'C:\spark\spark-3.5.0-bin-hadoop3\bin' + ';' +
    os.environ['PATH']
)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (RAW_DATA_PATH, PROCESSED_DATA_PATH,
                    SPARK_APP_NAME, SPARK_MASTER)

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql.types import *


def create_spark_session():
    """
    Create and return a Spark session
    Think of this like starting your Spark engine
    """
    print(" Starting Apache Spark...")
    
    spark = SparkSession.builder \
        .appName(SPARK_APP_NAME) \
        .master(SPARK_MASTER) \
        .config("spark.driver.host", "127.0.0.1") \
        .config("spark.hadoop.fs.defaultFS", "file:///") \
        .config("spark.sql.shuffle.partitions", "4") \
        .config("spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version", "2") \
        .config("spark.sql.warehouse.dir", "file:///C:/stock-pipeline/spark-warehouse") \
        .getOrCreate()
    
    # Hide unnecessary logs
    spark.sparkContext.setLogLevel("ERROR")
    
    print("✅ Spark is running!")
    return spark


def read_raw_data(spark):
    """
    Read all CSV files from data/raw folder
    Combines all 10 company files into one big table
    """
    print("\n📖 Reading raw stock data...")
    
    # Read all CSV files at once using wildcard *
    df = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .csv(f"{RAW_DATA_PATH}/*.csv")
    
    print(f"✅ Total records loaded: {df.count()}")
    print(f"✅ Columns: {df.columns}")
    
    return df


def clean_data(df):
    """
    Clean the raw data:
    - Remove null/missing values
    - Fix data types
    - Sort by symbol and date
    """
    print("\n🧹 Cleaning data...")
    
    # Remove rows with missing values
    df = df.dropna()
    
    # Convert Date to proper date type
    df = df.withColumn("Date", F.to_date(F.col("Date")))
    
    # Remove rows where price is 0 or negative
    df = df.filter(
        (F.col("Close") > 0) &
        (F.col("Open") > 0) &
        (F.col("Volume") > 0)
    )
    
    # Sort by Symbol and Date
    df = df.orderBy("Symbol", "Date")
    
    print(f"✅ Clean records: {df.count()}")
    return df


def calculate_metrics(df):
    """
    Calculate important financial metrics using Spark:
    
    1. Daily Return = how much price changed today vs yesterday
    2. Moving Average 7 = average price over last 7 days
    3. Moving Average 30 = average price over last 30 days
    4. Volatility = how much price fluctuates in a day
    """
    print("\n📊 Calculating financial metrics...")
    
    # Window = look at data for each company separately
    # ordered by date
    window_spec = Window.partitionBy("Symbol").orderBy("Date")
    
    # Window for 7 day moving average
    window_7 = Window.partitionBy("Symbol") \
                     .orderBy("Date") \
                     .rowsBetween(-6, 0)
    
    # Window for 30 day moving average
    window_30 = Window.partitionBy("Symbol") \
                      .orderBy("Date") \
                      .rowsBetween(-29, 0)
    
    # 1. Daily Return % = (Today's Close - Yesterday's Close) / Yesterday's Close * 100
    df = df.withColumn(
        "Previous_Close",
        F.lag("Close", 1).over(window_spec)
    )
    df = df.withColumn(
        "Daily_Return_Pct",
        F.round(
            ((F.col("Close") - F.col("Previous_Close")) /
             F.col("Previous_Close") * 100), 2
        )
    )
    
    # 2. 7 Day Moving Average
    df = df.withColumn(
        "MA_7",
        F.round(F.avg("Close").over(window_7), 2)
    )
    
    # 3. 30 Day Moving Average
    df = df.withColumn(
        "MA_30",
        F.round(F.avg("Close").over(window_30), 2)
    )
    
    # 4. Daily Volatility = (High - Low) / Low * 100
    df = df.withColumn(
        "Volatility_Pct",
        F.round(
            ((F.col("High") - F.col("Low")) /
             F.col("Low") * 100), 2
        )
    )
    
    # 5. Price Range = High - Low
    df = df.withColumn(
        "Price_Range",
        F.round(F.col("High") - F.col("Low"), 2)
    )
    
    # Remove rows where Previous_Close is null
    # (first row of each stock has no previous day)
    df = df.dropna(subset=["Daily_Return_Pct"])
    
    print("✅ Metrics calculated successfully!")
    print("   - Daily Return %")
    print("   - 7 Day Moving Average")
    print("   - 30 Day Moving Average")
    print("   - Volatility %")
    print("   - Price Range")
    
    return df


def save_processed_data(df):
    """
    Save processed data as CSV files
    Split by company for easy querying
    """
    print("\n💾 Saving processed data...")
    
    os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)
    
    # Save as single CSV file
    # coalesce(1) combines all partitions into one file
    df.coalesce(1) \
      .write \
      .mode("overwrite") \
      .option("header", "true") \
      .csv(PROCESSED_DATA_PATH + "/all_stocks")
    
    print(f"✅ Processed data saved to {PROCESSED_DATA_PATH}")
    
    # Show sample data
    print("\n📋 Sample processed data:")
    df.select(
        "Symbol", "Date", "Close",
        "Daily_Return_Pct", "MA_7", "MA_30", "Volatility_Pct"
    ).show(5)


def process_stocks():
    """
    Main function - runs entire processing pipeline
    """
    print("\n" + "="*50)
    print("🚀 STARTING SPARK PROCESSING PIPELINE")
    print("="*50)
    
    # Step 1 - Start Spark
    spark = create_spark_session()
    
    # Step 2 - Read raw data
    df = read_raw_data(spark)
    
    # Step 3 - Clean data
    df = clean_data(df)
    
    # Step 4 - Calculate metrics
    df = calculate_metrics(df)
    
    # Step 5 - Save processed data
    save_processed_data(df)
    
    print("\n" + "="*50)
    print("✅ SPARK PROCESSING COMPLETE!")
    print("="*50)
    
    # Stop Spark
    spark.stop()
    print("🛑 Spark stopped.")


if __name__ == "__main__":
    process_stocks()