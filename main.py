import streamlit as st
import yfinance as yf
import datetime

today = datetime.date.today()
default_start_date = today - datetime.timedelta(days=365)
start_date = st.sidebar.date_input("Select start date: ", default_start_date)
end_date = st.sidebar.date_input("Select end date: ", today)
if start_date < end_date:
    st.sidebar.success(f'Start date: {start_date}')
    st.sidebar.success(f'End date: {end_date}')
else:
    st.sidebar.error("End date cannot come before start date.")

st.title("Nairobi Forex Corner")

stocks = ("AAPL", "AMD", "AMZN", "FB", "GOOG", "MSFT", "NFLX", "NVDA", "QCOM", "TSLA")
stock_option = st.sidebar.selectbox("Select stock:", stocks)

stocks_data = yf.Ticker(stock_option)

stocks_dataframe = stocks_data.history(period="id", start=start_date, end=end_date)

st.write("### Close Values")
st.line_chart(stocks_dataframe["Close"])

st.write(" *** ")

st.write("### Volume Chart")
st.line_chart(stocks_dataframe["Volume"])
