import streamlit as st
import yfinance as yf
import datetime as dt
from fbprophet import Prophet

option = st.sidebar.selectbox("What do you want to do?", ("View historical data", "Predict future prices"))

stocks = ("AAPL", "AMD", "AMZN", "FB", "GOOG", "MSFT", "NFLX", "NVDA", "QCOM", "TSLA")
stock_option = st.selectbox("Select stock:", stocks)

TODAY = dt.date.today()
DEFAULT_START = TODAY - dt.timedelta(days=365)
START = st.sidebar.date_input("Select start date: ", DEFAULT_START)
END = st.sidebar.date_input("Select end date: ", TODAY)

if START < END:
    st.sidebar.success(f'Start date: {START}')
    st.sidebar.success(f'End date: {END}')
else:
    st.sidebar.error("End date cannot come before start date.")

st.title("Nairobi Forex Corner")

data = yf.download(stock_option, START, TODAY).reset_index()

data[["ds", "y"]] = data[["Date", "Close"]]

model = Prophet()

model.fit(data)

future = model.make_future_dataframe(periods = 365)

forecast = model.predict(future)

if option == "View historical data":

    stocks_data = yf.Ticker(stock_option)

    stocks_dataframe = stocks_data.history(period="id", start=START, end=END)

    st.header("Open")
    st.line_chart(stocks_dataframe["Open"])

    st.header("Close")
    st.line_chart(stocks_dataframe["Close"])

    st.write(" *** ")

    st.write("### High Values")
    st.line_chart(stocks_dataframe["High"])

    st.write("### Low Values")
    st.line_chart(stocks_dataframe["Low"])

    st.write(" *** ")

    st.write("### Volume Chart")
    st.line_chart(stocks_dataframe["Volume"])

elif option == "Predict future prices":
    fig = model.plot(forecast)
    st.write(fig)