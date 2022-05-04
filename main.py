import streamlit as st
import yfinance as yf
import datetime as dt
from neuralprophet import NeuralProphet


TODAY = dt.date.today()
DEFAULT_START = TODAY - dt.timedelta(days=365)


def load_data(val):
    df = yf.download(val, START, TODAY)
    df = df.reset_index()
    return df


feature_option = st.sidebar.selectbox("Select a feature", ("View historical data", "Predict future prices"))

START = st.sidebar.date_input("Select start date: ", DEFAULT_START)
END = st.sidebar.date_input("Select end date: ", TODAY)

if START < END:
    st.sidebar.success(f'Start date: {START}')
    st.sidebar.success(f'End date: {END}')
else:
    st.sidebar.error("End date cannot come before start date.")

stocks = ("AAPL", "AMD", "AMZN", "FB", "GOOG", "MSFT", "NFLX", "NVDA", "QCOM", "TSLA")
stock_option = st.selectbox("Select stock:", stocks)

st.title("Nairobi Forex Corner")

data = load_data(stock_option)

data.head()

data_ = data[["Date", "Close"]]

data_.columns = ["ds", "y"]

model = NeuralProphet()

model.fit(data_)

future = model.make_future_dataframe(data_, periods=365)

forecast = model.predict(future)

if feature_option == "View historical data":

    stocks_data = yf.Ticker(stock_option)

    stocks_dataframe = stocks_data.history(period='id', start=START, end=END)

    st.header("Open")
    st.line_chart(stocks_dataframe["Open"])

    st.header("Close")
    st.line_chart(stocks_dataframe["Close"])

    st.write(" *** ")

    st.header("High")
    st.line_chart(stocks_dataframe["High"])

    st.header("Low")
    st.line_chart(stocks_dataframe["Low"])

    st.write(" *** ")

    st.header("Volume")
    st.line_chart(stocks_dataframe["Volume"])

elif feature_option == "Predict future prices":
    fig = model.plot(forecast)
    st.write(fig)
