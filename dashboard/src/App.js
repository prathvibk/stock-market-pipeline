import { useState, useEffect } from "react";
import axios from "axios";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, BarChart, Bar, Legend
} from "recharts";

const API = "https://stock-market-pipeline.onrender.com";

// ─── Color scheme ───
const COLORS = {
  bg: "#0a0a0a",
  card: "#141414",
  cardHover: "#1f1f1f",
  accent: "#00d4ff",
  green: "#00ff88",
  red: "#ff4757",
  yellow: "#ffd93d",
  text: "#ffffff",
  muted: "#999999",
  border: "#2a2a2a"
};

// ─── Stock symbol to short name ───
const SHORT_NAME = {
  "TCS.NS": "TCS",
  "INFY.NS": "INFY",
  "WIPRO.NS": "WIPRO",
  "RELIANCE.NS": "RELIANCE",
  "HDFCBANK.NS": "HDFC",
  "ICICIBANK.NS": "ICICI",
  "HINDUNILVR.NS": "HUL",
  "ITC.NS": "ITC",
  "SBIN.NS": "SBIN",
  "BAJFINANCE.NS": "BAJFIN"
};

export default function App() {
  const [summary, setSummary] = useState([]);
  const [selectedStock, setSelectedStock] = useState("TCS.NS");
  const [stockData, setStockData] = useState([]);
  const [topGainers, setTopGainers] = useState([]);
  const [topLosers, setTopLosers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("overview");

  // Fetch all data on load
  useEffect(() => {
    fetchAllData();
  }, []);

  // Fetch stock detail when selected stock changes
  useEffect(() => {
    fetchStockDetail(selectedStock);
  }, [selectedStock]);

  const fetchAllData = async () => {
    try {
      const [sumRes, gainRes, loseRes] = await Promise.all([
        axios.get(`${API}/api/summary`),
        axios.get(`${API}/api/top-gainers`),
        axios.get(`${API}/api/top-losers`)
      ]);
      setSummary(sumRes.data);
      setTopGainers(gainRes.data);
      setTopLosers(loseRes.data);
      setLoading(false);
    } catch (err) {
      console.error("API Error:", err);
      setLoading(false);
    }
  };

  const fetchStockDetail = async (symbol) => {
    try {
      const res = await axios.get(`${API}/api/stock/${symbol}`);
      // Take last 180 days for chart
      setStockData(res.data.slice(-180));
    } catch (err) {
      console.error("Stock Error:", err);
    }
  };

  if (loading) return (
    <div style={{
      background: COLORS.bg, height: "100vh",
      display: "flex", alignItems: "center",
      justifyContent: "center", flexDirection: "column"
    }}>
      <div style={{ fontSize: 48 }}>📈</div>
      <p style={{ color: COLORS.accent, fontSize: 20, marginTop: 16 }}>
        Loading Stock Market Data...
      </p>
    </div>
  );

  return (
    <div style={{
      background: COLORS.bg, minHeight: "100vh",
      fontFamily: "'Segoe UI', sans-serif", color: COLORS.text
    }}>

      {/* ── NAVBAR ── */}
      <nav style={{
        background: "linear-gradient(180deg, #000 0%, transparent 100%)",
        padding: "16px 40px",
        display: "flex", alignItems: "center",
        justifyContent: "space-between",
        position: "sticky", top: 0, zIndex: 100,
        borderBottom: `1px solid ${COLORS.border}`
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <span style={{ fontSize: 28 }}>📈</span>
          <span style={{
            fontSize: 22, fontWeight: 800,
            color: COLORS.accent, letterSpacing: 1
          }}>StockIQ</span>
          <span style={{
            fontSize: 11, color: COLORS.muted,
            marginLeft: 8, marginTop: 4
          }}>Indian Market Analytics</span>
        </div>

        {/* Tabs */}
        <div style={{ display: "flex", gap: 8 }}>
          {["overview", "charts", "analysis"].map(tab => (
            <button key={tab} onClick={() => setActiveTab(tab)}
              style={{
                background: activeTab === tab ? COLORS.accent : "transparent",
                color: activeTab === tab ? "#000" : COLORS.muted,
                border: `1px solid ${activeTab === tab ? COLORS.accent : COLORS.border}`,
                padding: "6px 16px", borderRadius: 20,
                cursor: "pointer", fontWeight: 600,
                textTransform: "capitalize", fontSize: 13
              }}>
              {tab}
            </button>
          ))}
        </div>

        <div style={{
          background: "#1a1a2e", padding: "6px 16px",
          borderRadius: 20, fontSize: 12, color: COLORS.green,
          border: `1px solid ${COLORS.green}`
        }}>
          🟢 Live Data
        </div>
      </nav>

      <div style={{ padding: "24px 40px" }}>

        {/* ── HERO ── */}
        <div style={{ marginBottom: 32 }}>
          <h1 style={{
            fontSize: 36, fontWeight: 900,
            background: `linear-gradient(135deg, ${COLORS.accent}, ${COLORS.green})`,
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
            marginBottom: 8
          }}>
            Indian Stock Market Dashboard
          </h1>
          <p style={{ color: COLORS.muted, fontSize: 14 }}>
            Real data pipeline — 10 companies • 2024-2025 • Powered by Apache Spark
          </p>
        </div>

        {/* ── OVERVIEW TAB ── */}
        {activeTab === "overview" && (
          <>
            {/* Stats Row */}
            <div style={{
              display: "grid",
              gridTemplateColumns: "repeat(4, 1fr)",
              gap: 16, marginBottom: 32
            }}>
              {[
                { label: "Companies Tracked", value: "10", icon: "🏢" },
                { label: "Total Records", value: "4,931", icon: "📊" },
                { label: "Best Performer", value: "SBIN +0.10%", icon: "🏆" },
                { label: "Most Volatile", value: "BAJFIN 2.23%", icon: "⚡" }
              ].map((stat, i) => (
                <div key={i} style={{
                  background: COLORS.card,
                  border: `1px solid ${COLORS.border}`,
                  borderRadius: 12, padding: "20px 24px",
                  transition: "border-color 0.2s"
                }}>
                  <div style={{ fontSize: 28, marginBottom: 8 }}>{stat.icon}</div>
                  <div style={{
                    fontSize: 22, fontWeight: 800,
                    color: COLORS.accent
                  }}>{stat.value}</div>
                  <div style={{
                    fontSize: 12, color: COLORS.muted, marginTop: 4
                  }}>{stat.label}</div>
                </div>
              ))}
            </div>

            {/* Gainers and Losers */}
            <div style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gap: 16, marginBottom: 32
            }}>
              {/* Top Gainers */}
              <div style={{
                background: COLORS.card,
                border: `1px solid ${COLORS.border}`,
                borderRadius: 12, padding: 24
              }}>
                <h3 style={{
                  color: COLORS.green, marginBottom: 16,
                  fontSize: 16, fontWeight: 700
                }}>🏆 Top Gainers</h3>
                {topGainers.map((s, i) => (
                  <div key={i} style={{
                    display: "flex", justifyContent: "space-between",
                    alignItems: "center", padding: "10px 0",
                    borderBottom: `1px solid ${COLORS.border}`
                  }}>
                    <div>
                      <div style={{ fontWeight: 700, fontSize: 14 }}>
                        {SHORT_NAME[s.symbol] || s.symbol}
                      </div>
                      <div style={{ color: COLORS.muted, fontSize: 11 }}>
                        {s.company_name}
                      </div>
                    </div>
                    <div style={{
                      color: COLORS.green, fontWeight: 800,
                      fontSize: 16
                    }}>
                      +{s.avg_daily_return}%
                    </div>
                  </div>
                ))}
              </div>

              {/* Top Losers */}
              <div style={{
                background: COLORS.card,
                border: `1px solid ${COLORS.border}`,
                borderRadius: 12, padding: 24
              }}>
                <h3 style={{
                  color: COLORS.red, marginBottom: 16,
                  fontSize: 16, fontWeight: 700
                }}>📉 Top Losers</h3>
                {topLosers.map((s, i) => (
                  <div key={i} style={{
                    display: "flex", justifyContent: "space-between",
                    alignItems: "center", padding: "10px 0",
                    borderBottom: `1px solid ${COLORS.border}`
                  }}>
                    <div>
                      <div style={{ fontWeight: 700, fontSize: 14 }}>
                        {SHORT_NAME[s.symbol] || s.symbol}
                      </div>
                      <div style={{ color: COLORS.muted, fontSize: 11 }}>
                        {s.company_name}
                      </div>
                    </div>
                    <div style={{
                      color: COLORS.red, fontWeight: 800,
                      fontSize: 16
                    }}>
                      {s.avg_daily_return}%
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* All Stocks Table */}
            <div style={{
              background: COLORS.card,
              border: `1px solid ${COLORS.border}`,
              borderRadius: 12, padding: 24
            }}>
              <h3 style={{
                marginBottom: 16, fontSize: 16, fontWeight: 700
              }}>📋 All Stocks Overview</h3>
              <table style={{ width: "100%", borderCollapse: "collapse" }}>
                <thead>
                  <tr style={{ color: COLORS.muted, fontSize: 12 }}>
                    {["Company", "Avg Price", "Max", "Min",
                      "Daily Return", "Volatility", "Records"].map(h => (
                      <th key={h} style={{
                        textAlign: "left", padding: "8px 12px",
                        borderBottom: `1px solid ${COLORS.border}`,
                        fontWeight: 600
                      }}>{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {summary.map((s, i) => (
                    <tr key={i}
                      onClick={() => {
                        setSelectedStock(s.symbol);
                        setActiveTab("charts");
                      }}
                      style={{
                        cursor: "pointer",
                        transition: "background 0.2s"
                      }}
                      onMouseEnter={e => e.currentTarget.style.background = COLORS.cardHover}
                      onMouseLeave={e => e.currentTarget.style.background = "transparent"}
                    >
                      <td style={{ padding: "12px 12px" }}>
                        <div style={{ fontWeight: 700 }}>
                          {SHORT_NAME[s.symbol]}
                        </div>
                        <div style={{ color: COLORS.muted, fontSize: 11 }}>
                          {s.company_name}
                        </div>
                      </td>
                      <td style={{ padding: "12px" }}>₹{s.avg_close_price}</td>
                      <td style={{
                        padding: "12px", color: COLORS.green
                      }}>₹{s.max_price}</td>
                      <td style={{
                        padding: "12px", color: COLORS.red
                      }}>₹{s.min_price}</td>
                      <td style={{
                        padding: "12px",
                        color: s.avg_daily_return >= 0 ? COLORS.green : COLORS.red,
                        fontWeight: 700
                      }}>
                        {s.avg_daily_return >= 0 ? "+" : ""}{s.avg_daily_return}%
                      </td>
                      <td style={{ padding: "12px", color: COLORS.yellow }}>
                        {s.avg_volatility}%
                      </td>
                      <td style={{ padding: "12px", color: COLORS.muted }}>
                        {s.total_records}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        )}

        {/* ── CHARTS TAB ── */}
        {activeTab === "charts" && (
          <>
            {/* Stock Selector */}
            <div style={{ marginBottom: 24 }}>
              <p style={{
                color: COLORS.muted, fontSize: 13, marginBottom: 12
              }}>Select a stock to view charts:</p>
              <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                {summary.map((s, i) => (
                  <button key={i}
                    onClick={() => setSelectedStock(s.symbol)}
                    style={{
                      background: selectedStock === s.symbol
                        ? COLORS.accent : COLORS.card,
                      color: selectedStock === s.symbol ? "#000" : COLORS.text,
                      border: `1px solid ${selectedStock === s.symbol
                        ? COLORS.accent : COLORS.border}`,
                      padding: "8px 16px", borderRadius: 20,
                      cursor: "pointer", fontWeight: 600, fontSize: 13
                    }}>
                    {SHORT_NAME[s.symbol]}
                  </button>
                ))}
              </div>
            </div>

            {/* Price Chart */}
            <div style={{
              background: COLORS.card,
              border: `1px solid ${COLORS.border}`,
              borderRadius: 12, padding: 24, marginBottom: 16
            }}>
              <h3 style={{ marginBottom: 4, fontSize: 16, fontWeight: 700 }}>
                📈 {SHORT_NAME[selectedStock]} — Price History
              </h3>
              <p style={{
                color: COLORS.muted, fontSize: 12, marginBottom: 16
              }}>Last 180 trading days with 7-day and 30-day moving averages</p>
              <ResponsiveContainer width="100%" height={350}>
                <LineChart data={stockData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#222" />
                  <XAxis dataKey="date" stroke={COLORS.muted}
                    tick={{ fontSize: 10 }}
                    tickFormatter={v => v?.slice(0, 7)} />
                  <YAxis stroke={COLORS.muted} tick={{ fontSize: 10 }} />
                  <Tooltip
                    contentStyle={{
                      background: "#1a1a2e",
                      border: `1px solid ${COLORS.border}`,
                      borderRadius: 8, color: COLORS.text
                    }}
                  />
                  <Legend />
                  <Line type="monotone" dataKey="close_price"
                    stroke={COLORS.accent} dot={false}
                    strokeWidth={2} name="Close Price" />
                  <Line type="monotone" dataKey="ma_7"
                    stroke={COLORS.red} dot={false}
                    strokeWidth={1} strokeDasharray="4 4" name="MA 7" />
                  <Line type="monotone" dataKey="ma_30"
                    stroke={COLORS.yellow} dot={false}
                    strokeWidth={1} strokeDasharray="4 4" name="MA 30" />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {/* Daily Returns Chart */}
            <div style={{
              background: COLORS.card,
              border: `1px solid ${COLORS.border}`,
              borderRadius: 12, padding: 24
            }}>
              <h3 style={{ marginBottom: 4, fontSize: 16, fontWeight: 700 }}>
                📊 {SHORT_NAME[selectedStock]} — Daily Returns %
              </h3>
              <p style={{
                color: COLORS.muted, fontSize: 12, marginBottom: 16
              }}>Green = profit day, Red = loss day</p>
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={stockData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#222" />
                  <XAxis dataKey="date" stroke={COLORS.muted}
                    tick={{ fontSize: 10 }}
                    tickFormatter={v => v?.slice(0, 7)} />
                  <YAxis stroke={COLORS.muted} tick={{ fontSize: 10 }} />
                  <Tooltip
                    contentStyle={{
                      background: "#1a1a2e",
                      border: `1px solid ${COLORS.border}`,
                      borderRadius: 8
                    }}
                  />
                  <Bar dataKey="daily_return_pct" name="Daily Return %"
                    fill={COLORS.green}
                    label={false} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </>
        )}

        {/* ── ANALYSIS TAB ── */}
        {activeTab === "analysis" && (
          <>
            <div style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gap: 16
            }}>
              {/* Volatility Comparison */}
              <div style={{
                background: COLORS.card,
                border: `1px solid ${COLORS.border}`,
                borderRadius: 12, padding: 24
              }}>
                <h3 style={{
                  marginBottom: 16, fontSize: 16, fontWeight: 700
                }}>⚡ Volatility Comparison</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={summary} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" stroke="#222" />
                    <XAxis type="number" stroke={COLORS.muted}
                      tick={{ fontSize: 10 }} />
                    <YAxis dataKey="symbol" type="category"
                      stroke={COLORS.muted} tick={{ fontSize: 10 }}
                      tickFormatter={v => SHORT_NAME[v] || v} width={60} />
                    <Tooltip
                      contentStyle={{
                        background: "#1a1a2e",
                        border: `1px solid ${COLORS.border}`,
                        borderRadius: 8
                      }}
                    />
                    <Bar dataKey="avg_volatility" fill={COLORS.yellow}
                      name="Avg Volatility %" />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              {/* Returns Comparison */}
              <div style={{
                background: COLORS.card,
                border: `1px solid ${COLORS.border}`,
                borderRadius: 12, padding: 24
              }}>
                <h3 style={{
                  marginBottom: 16, fontSize: 16, fontWeight: 700
                }}>📈 Returns Comparison</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={summary} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" stroke="#222" />
                    <XAxis type="number" stroke={COLORS.muted}
                      tick={{ fontSize: 10 }} />
                    <YAxis dataKey="symbol" type="category"
                      stroke={COLORS.muted} tick={{ fontSize: 10 }}
                      tickFormatter={v => SHORT_NAME[v] || v} width={60} />
                    <Tooltip
                      contentStyle={{
                        background: "#1a1a2e",
                        border: `1px solid ${COLORS.border}`,
                        borderRadius: 8
                      }}
                    />
                    <Bar dataKey="avg_daily_return" name="Avg Daily Return %"
                      fill={COLORS.green} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Key Insights */}
            <div style={{
              background: COLORS.card,
              border: `1px solid ${COLORS.border}`,
              borderRadius: 12, padding: 24, marginTop: 16
            }}>
              <h3 style={{
                marginBottom: 16, fontSize: 16, fontWeight: 700
              }}>💡 Key Insights</h3>
              <div style={{
                display: "grid",
                gridTemplateColumns: "repeat(3, 1fr)", gap: 16
              }}>
                {[
                  {
                    icon: "🏆",
                    title: "Best Performer",
                    value: "SBIN",
                    detail: "+0.10% avg daily return",
                    color: COLORS.green
                  },
                  {
                    icon: "⚡",
                    title: "Most Volatile",
                    value: "Bajaj Finance",
                    detail: "2.23% avg daily volatility",
                    color: COLORS.yellow
                  },
                  {
                    icon: "🛡️",
                    title: "Most Stable",
                    value: "HDFC Bank",
                    detail: "1.58% avg daily volatility",
                    color: COLORS.accent
                  }
                ].map((insight, i) => (
                  <div key={i} style={{
                    background: "#1a1a2e",
                    border: `1px solid ${insight.color}33`,
                    borderRadius: 10, padding: 16
                  }}>
                    <div style={{ fontSize: 28 }}>{insight.icon}</div>
                    <div style={{
                      color: COLORS.muted, fontSize: 11,
                      marginTop: 8
                    }}>{insight.title}</div>
                    <div style={{
                      color: insight.color, fontWeight: 800,
                      fontSize: 18, marginTop: 4
                    }}>{insight.value}</div>
                    <div style={{
                      color: COLORS.muted, fontSize: 11, marginTop: 4
                    }}>{insight.detail}</div>
                  </div>
                ))}
              </div>
            </div>
          </>
        )}

        {/* Footer */}
        <div style={{
          marginTop: 40, textAlign: "center",
          color: COLORS.muted, fontSize: 12,
          borderTop: `1px solid ${COLORS.border}`, paddingTop: 20
        }}>
          Built with Python • Apache Spark • Hadoop • MySQL • Flask • React
          <br />
          Data: Yahoo Finance API • 10 Indian Companies • 2024-2025
        </div>

      </div>
    </div>
  );
}