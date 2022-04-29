import streamlit as st
import yfinance as yf
from datetime import date

START = "2015-01-01"
END = date.today().strftime("%Y-%M-%D")

st.title("Nairobi Forex Corner")

stocks = ("AAPL", "AMD", "AMZN", "FB", "GOOG", "MSFT", "NFLX", "NVDA", "QCOM", "TSLA")
stocks_select_box = st.selectbox("Select stock:", stocks)

stocks_data = yf.Ticker(stocks_select_box)

stocks_dataframe = stocks_data.history(period = "id", start = START, end = "2021-12-31")

st.write("### Close Values")
st.line_chart(stocks_dataframe["Close"])

st.write(" *** ")

st.write("### Volume Chart")
st.line_chart(stocks_dataframe["Volume"])