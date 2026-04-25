# stock-market-pipeline

# 📈 Stock Market Data Pipeline
An end-to-end data engineering pipeline that collects, processes,
and visualizes real stock market data for 10 Indian companies
using Apache Spark, Hadoop, MySQL, Flask, and React.

---

## 🚀 Pipeline Architecture
Yahoo Finance API
↓
Data Collection (Python)
↓
Big Data Processing (Apache Spark)
↓
Data Warehouse (MySQL + Hadoop)
↓
REST API (Flask)
↓
Dashboard (React)

---

## 📊 Companies Tracked
| Company | Symbol |
|---------|--------|
| Tata Consultancy Services | TCS.NS |
| Infosys | INFY.NS |
| Wipro | WIPRO.NS |
| Reliance Industries | RELIANCE.NS |
| HDFC Bank | HDFCBANK.NS |
| ICICI Bank | ICICIBANK.NS |
| Hindustan Unilever | HINDUNILVR.NS |
| ITC Limited | ITC.NS |
| State Bank of India | SBIN.NS |
| Bajaj Finance | BAJFINANCE.NS |

---

## 🛠️ Tech Stack
| Layer | Technology |
|-------|------------|
| Data Collection | Python, Yahoo Finance API |
| Big Data Processing | Apache Spark 3.5, PySpark |
| Distributed Storage | Apache Hadoop 3.3.6, HDFS |
| Data Warehouse | MySQL, Hive |
| REST API | Flask, Flask-CORS |
| Dashboard | React, Recharts |
| Cloud Database | Railway MySQL |
| Deployment | Render, Netlify |

---

## 📁 Project Structure
stock-pipeline/
│
├── src/
│   ├── collect_data.py       # Yahoo Finance API data collection
│   ├── process_data.py       # Apache Spark processing
│   ├── warehouse.py          # MySQL data warehouse setup
│   ├── analytics.py          # SQL analytics and insights
│   └── visualize.py          # Matplotlib/Seaborn charts
│
├── dashboard/                # React frontend
│   └── src/
│       └── App.js            # Netflix-style dark dashboard
│
├── data/
│   ├── raw/                  # Raw CSV files from Yahoo Finance
│   └── processed/            # Spark processed data
│
├── visualizations/           # Generated charts
├── app.py                    # Flask REST API
├── config.py                 # Configuration settings
└── requirements.txt          # Python dependencies

---

## ⚙️ How to Run
### Prerequisites
- Python 3.12
- Java 11
- Apache Hadoop 3.3.6
- Apache Spark 3.5.0
- MySQL
- Node.js

### Installation
```bash
# 1. Clone the repo
git clone https://github.com/prathvibk/stock-market-pipeline.git
cd stock-market-pipeline

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Run the pipeline
python src/collect_data.py        # Collect stock data
python src/process_data.py        # Process with Spark
python src/warehouse.py           # Load to MySQL
python src/analytics.py           # Generate insights
python src/visualize.py           # Create charts

# 4. Start Flask API
python app.py

# 5. Start React Dashboard
cd dashboard
npm install
npm start
```

---

## 📡 API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/summary` | All stocks overview |
| GET | `/api/stock/<symbol>` | Stock price history |
| GET | `/api/top-gainers` | Best performing stocks |
| GET | `/api/top-losers` | Worst performing stocks |
| GET | `/api/most-volatile` | Most volatile stocks |
| GET | `/api/monthly/<symbol>` | Monthly performance |
| GET | `/api/best-days` | Best trading days |
| GET | `/api/worst-days` | Worst trading days |

---

## 📊 Key Insights (2024-2025)
| Metric | Stock | Value |
|--------|-------|-------|
| 🏆 Best Performer | SBIN | +0.10% avg daily return |
| ⚡ Most Volatile | Bajaj Finance | 2.23% avg volatility |
| 🛡️ Most Stable | HDFC Bank | 1.58% avg volatility |
| 📈 Highest Price | TCS | ₹4,348 max |
| 📉 Lowest Price | Wipro | ₹195 min |

---

## 🎨 Dashboard Features
- 📈 Real-time stock price charts
- 📊 Moving average overlays (7-day, 30-day)
- 💚 Top gainers and losers
- ⚡ Volatility comparison
- 📋 Complete stocks table
- 🌑 Netflix-style dark theme

---

## 👨‍💻 Author
**Prathvi**
MCA Graduate — PES University, Bangalore
📧 prathvibk686@gmail.com
🔗 [LinkedIn](https://linkedin.com/in/prathvi-bk)
⭐ [GitHub](https://github.com/prathvibk)

---

## 📄 License
This project is open source and available under the
[MIT License](LICENSE).










