# main.py
import streamlit as st
import pandas as pd
from utils import fetch_daily_stock_data

# --- PAGE CONFIG ---
st.set_page_config(page_title="Stock Tracker", layout="centered")

# --- THEME TOGGLE ---
theme = st.radio("Choose Theme", ["Light", "Dark"], horizontal=True)

# --- Apply Theme CSS ---
if theme == "Dark":
    st.markdown("""
        <style>
            body, .stApp {
                background-color: #0e1117;
                color: #fafafa;
            }
            .stTextInput > div > div > input {
                color: #fafafa;
                background-color: #262730;
            }
            .stTextInput label {
                color: #fafafa !important;
            }
            div[data-baseweb="radio"] * {
                color: #fafafa !important;
            }
            .stButton>button {
                background-color: #262730;
                color: #fafafa;
            }
            .stDataFrame, .stTable {
                color: #fafafa;
            }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
            body, .stApp {
                background-color: #ffffff;
                color: #000000;
            }
            .stTextInput > div > div > input {
                color: #000000;
                background-color: #f0f2f6;
            }
            .stTextInput label {
                color: #000000 !important;
            }
            div[data-baseweb="radio"] * {
                color: #000000 !important;
            }
            .stButton>button {
                background-color: #f0f2f6;
                color: #000000;
            }
            .stDataFrame, .stTable {
                color: #000000;
            }
        </style>
    """, unsafe_allow_html=True)

# --- TITLE ---
st.title("Stock Tracker")

# --- Compare Mode Toggle ---
compare_mode = st.checkbox("Compare with another stock?")

# --- Inputs ---
symbol1 = st.text_input("Enter a stock symbol (e.g., AAPL)", value="AAPL")
symbol2 = None
if compare_mode:
    symbol2 = st.text_input("Enter second stock symbol", value="TSLA")

# --- Helper to Process API Response ---
def process_stock_data(raw_data: dict, label="Stock"):
    ts = raw_data["Time Series (Daily)"]
    df = pd.DataFrame(ts).T
    df.index = pd.to_datetime(df.index)
    df = df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume"
    })
    df = df.astype(float)
    return df.sort_index()

# --- Fetch and Display ---
if symbol1 and (not compare_mode or symbol2):
    raw1 = fetch_daily_stock_data(symbol1)
    raw2 = fetch_daily_stock_data(symbol2) if compare_mode else None

    if "Time Series (Daily)" in raw1:
        df1 = process_stock_data(raw1, symbol1)
        chart_data = df1[["Close"]].rename(columns={"Close": f"{symbol1.upper()} Close"})

        if compare_mode and raw2 and "Time Series (Daily)" in raw2:
            df2 = process_stock_data(raw2, symbol2)
            # Align both to same dates
            chart_data = chart_data.join(df2["Close"].rename(f"{symbol2.upper()} Close"), how="inner")

        st.line_chart(chart_data)

        st.subheader(f"{symbol1.upper()} Recent Data")
        st.dataframe(df1.tail(10))

        if compare_mode and raw2 and "Time Series (Daily)" in raw2:
            st.subheader(f"{symbol2.upper()} Recent Data")
            st.dataframe(df2.tail(10))

    elif "Note" in raw1:
        st.warning("oopsie: API rate limit exceeded. Try again in about 60 seconds.")
    elif "Error Message" in raw1:
        st.error(f" Error for {symbol1}: {raw1['Error Message']}")
    elif "Information" in raw1:
        st.warning("Info: API limit reached or invalid key.")
    else:
        st.error(" Failed to fetch data. Please check your API key and stock symbol.")
