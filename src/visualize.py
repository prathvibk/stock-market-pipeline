# ============================================
# STEP 5: DATA VISUALIZATION
# ============================================
# This file creates beautiful charts from
# your stock market data using Matplotlib
# and Seaborn
# ============================================

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import mysql.connector
import warnings
warnings.filterwarnings('ignore')

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_CONFIG, VISUALIZATION_PATH


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def setup_style():
    """
    Set dark Netflix-style theme for all charts
    """
    plt.style.use('dark_background')
    sns.set_palette("husl")


def get_data(query):
    """
    Run SQL query and return dataframe
    """
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def chart1_stock_price_trends():
    """
    Chart 1 — Stock price trend for all companies
    Line chart showing how each stock moved over time
    """
    print("📈 Creating Chart 1 — Stock Price Trends...")

    query = """
        SELECT symbol, date, close_price, ma_7, ma_30
        FROM stock_prices
        ORDER BY symbol, date
    """
    df = get_data(query)
    df['date'] = pd.to_datetime(df['date'])

    # Get unique symbols
    symbols = df['symbol'].unique()

    # Create figure with subplots — 2 columns
    fig, axes = plt.subplots(5, 2, figsize=(20, 25))
    fig.patch.set_facecolor('#0a0a0a')
    fig.suptitle('📈 Indian Stock Market Price Trends 2024-2025',
                 fontsize=20, color='white', fontweight='bold', y=1.02)

    axes = axes.flatten()

    for i, symbol in enumerate(symbols):
        stock_df = df[df['symbol'] == symbol]
        ax = axes[i]
        ax.set_facecolor('#1a1a2e')

        # Plot close price
        ax.plot(stock_df['date'], stock_df['close_price'],
                color='#00d4ff', linewidth=1.5, label='Close Price')

        # Plot moving averages
        ax.plot(stock_df['date'], stock_df['ma_7'],
                color='#ff6b6b', linewidth=1, linestyle='--', label='MA 7')
        ax.plot(stock_df['date'], stock_df['ma_30'],
                color='#ffd93d', linewidth=1, linestyle='--', label='MA 30')

        # Styling
        ax.set_title(symbol.replace('.NS', ''),
                    color='white', fontsize=12, fontweight='bold')
        ax.tick_params(colors='white', labelsize=8)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        ax.legend(fontsize=7, loc='upper left')
        ax.grid(True, alpha=0.2)
        ax.spines['bottom'].set_color('#333333')
        ax.spines['left'].set_color('#333333')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.yaxis.label.set_color('white')

    plt.tight_layout()
    filepath = f"{VISUALIZATION_PATH}/chart1_price_trends.png"
    plt.savefig(filepath, dpi=150, bbox_inches='tight',
                facecolor='#0a0a0a')
    plt.close()
    print(f"✅ Saved: {filepath}")


def chart2_top_gainers_losers():
    """
    Chart 2 — Top gainers vs losers bar chart
    """
    print("📊 Creating Chart 2 — Top Gainers vs Losers...")

    query = """
        SELECT symbol, avg_daily_return, avg_volatility
        FROM stock_summary
        ORDER BY avg_daily_return DESC
    """
    df = get_data(query)
    df['symbol'] = df['symbol'].str.replace('.NS', '')

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    fig.patch.set_facecolor('#0a0a0a')

    # Colors based on positive/negative
    colors = ['#00ff88' if x > 0 else '#ff4757'
              for x in df['avg_daily_return']]

    # Chart 1 - Daily Returns
    ax1.set_facecolor('#1a1a2e')
    bars = ax1.barh(df['symbol'], df['avg_daily_return'],
                    color=colors, edgecolor='none')
    ax1.set_title('Average Daily Return %',
                  color='white', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Return %', color='white')
    ax1.tick_params(colors='white')
    ax1.axvline(x=0, color='white', linewidth=0.5)
    ax1.grid(True, alpha=0.2, axis='x')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['bottom'].set_color('#333333')
    ax1.spines['left'].set_color('#333333')

    # Add value labels
    for bar, val in zip(bars, df['avg_daily_return']):
        ax1.text(val + 0.001, bar.get_y() + bar.get_height()/2,
                f'{val:.3f}%', va='center', color='white', fontsize=9)

    # Chart 2 - Volatility
    ax2.set_facecolor('#1a1a2e')
    colors2 = sns.color_palette("husl", len(df))
    bars2 = ax2.barh(df['symbol'], df['avg_volatility'],
                     color=colors2, edgecolor='none')
    ax2.set_title('Average Volatility %',
                  color='white', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Volatility %', color='white')
    ax2.tick_params(colors='white')
    ax2.grid(True, alpha=0.2, axis='x')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['bottom'].set_color('#333333')
    ax2.spines['left'].set_color('#333333')

    for bar, val in zip(bars2, df['avg_volatility']):
        ax2.text(val + 0.01, bar.get_y() + bar.get_height()/2,
                f'{val:.2f}%', va='center', color='white', fontsize=9)

    fig.suptitle('📊 Stock Performance Dashboard — 2024-2025',
                fontsize=16, color='white', fontweight='bold')
    plt.tight_layout()

    filepath = f"{VISUALIZATION_PATH}/chart2_gainers_losers.png"
    plt.savefig(filepath, dpi=150, bbox_inches='tight',
                facecolor='#0a0a0a')
    plt.close()
    print(f"✅ Saved: {filepath}")


def chart3_volatility_heatmap():
    """
    Chart 3 — Monthly volatility heatmap
    Shows which months were most volatile
    """
    print("🗺️ Creating Chart 3 — Volatility Heatmap...")

    query = """
        SELECT
            symbol,
            DATE_FORMAT(date, '%Y-%m') as month,
            ROUND(AVG(volatility_pct), 2) as avg_volatility
        FROM stock_prices
        GROUP BY symbol, month
        ORDER BY symbol, month
    """
    df = get_data(query)
    df['symbol'] = df['symbol'].str.replace('.NS', '')

    # Pivot for heatmap
    pivot = df.pivot(index='symbol', columns='month', values='avg_volatility')

    fig, ax = plt.subplots(figsize=(20, 8))
    fig.patch.set_facecolor('#0a0a0a')
    ax.set_facecolor('#1a1a2e')

    sns.heatmap(pivot, ax=ax, cmap='YlOrRd',
            annot=True, fmt='.1f',
            linewidths=0.5, linecolor='#333333',
            cbar_kws={'label': 'Volatility %'},
            annot_kws={'size': 8})

    ax.set_title('🗺️ Monthly Volatility Heatmap — Higher = More Volatile',
                color='white', fontsize=14, fontweight='bold', pad=20)
    ax.tick_params(colors='white', labelsize=9)
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)

    filepath = f"{VISUALIZATION_PATH}/chart3_volatility_heatmap.png"
    plt.savefig(filepath, dpi=150, bbox_inches='tight',
                facecolor='#0a0a0a')
    plt.close()
    print(f"✅ Saved: {filepath}")


def chart4_daily_returns_distribution():
    """
    Chart 4 — Distribution of daily returns
    Shows how returns are spread for each stock
    """
    print("📉 Creating Chart 4 — Returns Distribution...")

    query = """
        SELECT symbol, daily_return_pct
        FROM stock_prices
        WHERE daily_return_pct IS NOT NULL
    """
    df = get_data(query)
    df['symbol'] = df['symbol'].str.replace('.NS', '')

    symbols = df['symbol'].unique()
    fig, axes = plt.subplots(2, 5, figsize=(20, 8))
    fig.patch.set_facecolor('#0a0a0a')
    fig.suptitle('📉 Daily Returns Distribution — Normal = Stable Stock',
                fontsize=14, color='white', fontweight='bold')

    axes = axes.flatten()
    colors = sns.color_palette("husl", len(symbols))

    for i, symbol in enumerate(symbols):
        stock_df = df[df['symbol'] == symbol]
        ax = axes[i]
        ax.set_facecolor('#1a1a2e')

        ax.hist(stock_df['daily_return_pct'], bins=50,
                color=colors[i], alpha=0.8, edgecolor='none')
        ax.axvline(x=0, color='white', linewidth=1, linestyle='--')

        mean_return = stock_df['daily_return_pct'].mean()
        ax.set_title(f'{symbol}\nMean: {mean_return:.3f}%',
                    color='white', fontsize=10)
        ax.tick_params(colors='white', labelsize=7)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color('#333333')
        ax.spines['left'].set_color('#333333')

    plt.tight_layout()
    filepath = f"{VISUALIZATION_PATH}/chart4_returns_distribution.png"
    plt.savefig(filepath, dpi=150, bbox_inches='tight',
                facecolor='#0a0a0a')
    plt.close()
    print(f"✅ Saved: {filepath}")


def create_visualizations():
    """
    Main function - creates all charts
    """
    print("\n" + "="*50)
    print("🎨 CREATING VISUALIZATIONS")
    print("="*50)

    # Create output folder
    os.makedirs(VISUALIZATION_PATH, exist_ok=True)

    setup_style()

    # Create all charts
    chart1_stock_price_trends()
    chart2_top_gainers_losers()
    chart3_volatility_heatmap()
    chart4_daily_returns_distribution()

    print("\n" + "="*50)
    print("✅ ALL CHARTS CREATED!")
    print("="*50)
    print(f"\n📁 Charts saved in: {VISUALIZATION_PATH}/")
    print("   chart1_price_trends.png")
    print("   chart2_gainers_losers.png")
    print("   chart3_volatility_heatmap.png")
    print("   chart4_returns_distribution.png")


if __name__ == "__main__":
    create_visualizations()