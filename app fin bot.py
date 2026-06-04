import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from ta.momentum import RSIIndicator

st.set_page_config(
    page_title="AI Financial Advisor",
    layout="wide"
)

st.title("💰 AI Financial Advisor Platform")

# =========================
# USER PROFILE
# =========================

st.sidebar.header("Financial Profile")

income = st.sidebar.number_input(
    "Monthly Income ₹",
    0,
    1000000,
    50000
)

expenses = st.sidebar.number_input(
    "Monthly Expenses ₹",
    0,
    1000000,
    25000
)

goal = st.sidebar.number_input(
    "Savings Goal ₹",
    0,
    100000000,
    1000000
)

risk = st.sidebar.selectbox(
    "Risk Appetite",
    ["Low", "Medium", "High"]
)

savings = income - expenses

# =========================
# DASHBOARD
# =========================

st.header("📊 Financial Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("Income", f"₹{income:,.0f}")
col2.metric("Expenses", f"₹{expenses:,.0f}")
col3.metric("Savings", f"₹{savings:,.0f}")

if income > 0:
    rate = savings / income * 100
    st.success(f"Savings Rate: {rate:.2f}%")

# =========================
# LIVE NIFTY
# =========================

st.header("📈 NIFTY 50 Live")

try:

    nifty = yf.download(
        "^NSEI",
        period="5d",
        progress=False,
        auto_adjust=True
    )

    latest_nifty = float(nifty["Close"].iloc[-1])

    st.metric(
        "NIFTY 50",
        f"{latest_nifty:,.2f}"
    )

except:
    st.warning("NIFTY Data unavailable")

# =========================
# NSE STOCKS
# =========================

st.header("📈 NSE Stock Analyzer")

stocks = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "ITC.NS",
    "SBIN.NS",
    "LT.NS",
    "BHARTIARTL.NS",
    "AXISBANK.NS",
    "MARUTI.NS",
    "TATAMOTORS.NS",
    "WIPRO.NS",
    "HCLTECH.NS"
]

selected_stock = st.selectbox(
    "Select Stock",
    stocks
)

try:

    df = yf.download(
        selected_stock,
        period="1y",
        progress=False,
        auto_adjust=True
    )

    current_price = float(df["Close"].iloc[-1])

    st.metric(
        "Current Price",
        f"₹{current_price:.2f}"
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["Close"],
            mode="lines",
            name="Close"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

except:
    st.error("Unable to load stock data")

# =========================
# AI STOCK RECOMMENDATION
# =========================

st.header("🤖 AI Stock Recommendation")

if st.button("Generate Recommendations"):

    recommendations = []

    for stock in stocks:

        try:

            data = yf.download(
                stock,
                period="6mo",
                progress=False,
                auto_adjust=True
            )

            if len(data) < 50:
                continue

            data["MA20"] = data["Close"].rolling(20).mean()
            data["MA50"] = data["Close"].rolling(50).mean()

            rsi = RSIIndicator(
                close=data["Close"]
            ).rsi()

            latest_rsi = float(rsi.iloc[-1])

            ma20 = float(data["MA20"].iloc[-1])
            ma50 = float(data["MA50"].iloc[-1])

            signal = "HOLD"

            if ma20 > ma50 and latest_rsi < 70:
                signal = "BUY"

            elif latest_rsi > 70:
                signal = "SELL"

            recommendations.append(
                [
                    stock,
                    round(latest_rsi, 2),
                    signal
                ]
            )

        except:
            pass

    rec_df = pd.DataFrame(
        recommendations,
        columns=[
            "Stock",
            "RSI",
            "Signal"
        ]
    )

    st.dataframe(rec_df)

# =========================
# SIP CALCULATOR
# =========================

st.header("💵 SIP Calculator")

sip = st.number_input(
    "Monthly SIP",
    500,
    100000,
    5000
)

years = st.slider(
    "Years",
    1,
    30,
    10
)

returns = st.slider(
    "Expected Return %",
    5,
    20,
    12
)

months = years * 12

future_value = sip * (
    (((1 + returns/100/12) ** months) - 1)
    /
    (returns/100/12)
) * (1 + returns/100/12)

st.success(
    f"Future Value: ₹{future_value:,.0f}"
)

# =========================
# ETF SECTION
# =========================

st.header("📊 ETF Recommendations")

etfs = {
    "NIFTYBEES.NS": "Index ETF",
    "BANKBEES.NS": "Bank ETF",
    "ITBEES.NS": "IT ETF",
    "GOLDBEES.NS": "Gold ETF"
}

etf_rows = []

for etf, desc in etfs.items():

    try:

        data = yf.download(
            etf,
            period="5d",
            progress=False,
            auto_adjust=True
        )

        price = float(data["Close"].iloc[-1])

        etf_rows.append(
            [etf, desc, round(price, 2)]
        )

    except:
        pass

st.dataframe(
    pd.DataFrame(
        etf_rows,
        columns=[
            "ETF",
            "Category",
            "Price"
        ]
    )
)

# =========================
# BITCOIN
# =========================

st.header("₿ Bitcoin Tracker")

try:

    btc = yf.download(
        "BTC-USD",
        period="6mo",
        progress=False,
        auto_adjust=True
    )

    btc_price = float(
        btc["Close"].iloc[-1]
    )

    st.metric(
        "Bitcoin",
        f"${btc_price:,.0f}"
    )

    fig2 = go.Figure()

    fig2.add_trace(
        go.Scatter(
            x=btc.index,
            y=btc["Close"]
        )
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

except:
    st.warning("Bitcoin data unavailable")

# =========================
# FINANCIAL ADVISOR
# =========================

st.header("🧠 AI Financial Advisor")

if savings <= 0:

    st.error(
        "Reduce expenses and build an emergency fund."
    )

elif savings < 10000:

    st.warning("""
    Suggested:
    - Fixed Deposit
    - Emergency Fund
    - Liquid Fund
    """)

elif savings < 30000:

    st.info("""
    Suggested Portfolio:
    - 50% SIP
    - 30% ETF
    - 20% Gold ETF
    """)

else:

    st.success("""
    Suggested Portfolio:
    - 40% Stocks
    - 30% Mutual Funds
    - 20% ETF
    - 10% Bitcoin
    """)

# =========================
# GOAL TRACKER
# =========================

st.header("🎯 Goal Planning")

if savings > 0:

    months_needed = goal / savings

    st.write(
        f"Goal Achievement Time: {months_needed:.1f} Months"
    )

# =========================
# RISK PORTFOLIO
# =========================

st.header("📋 Risk-Based Allocation")

if risk == "Low":

    st.write({
        "Debt Funds": 50,
        "ETF": 20,
        "Gold": 20,
        "Cash": 10
    })

elif risk == "Medium":

    st.write({
        "Mutual Funds": 40,
        "Stocks": 30,
        "ETF": 20,
        "Gold": 10
    })

else:

    st.write({
        "Stocks": 50,
        "ETF": 20,
        "Mutual Funds": 20,
        "Bitcoin": 10
    })