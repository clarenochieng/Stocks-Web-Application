import streamlit as st
import yfinance as yf
import datetime as dt
from neuralprophet import NeuralProphet


TODAY = dt.date.today()
DEFAULT_START = TODAY - dt.timedelta(days=365)


def load_display_data(val):
    df = yf.download(val, START, TODAY)
    df = df.reset_index()
    return df

def load_prediction_data(val):
    df = yf.download(val)
    df = df.reset_index()
    return df

def display(val):
    st.header(val)
    st.line_chart(stocks_dataframe[val])

feature_option = st.sidebar.selectbox("Select a feature: ", ("View historical data", "Predict future prices"))

START = st.sidebar.date_input("Select start date: ", DEFAULT_START)
END = st.sidebar.date_input("Select end date: ", TODAY)

if START < END:
    st.sidebar.success(f'Start date: {START}')
    st.sidebar.success(f'End date: {END}')
else:
    st.sidebar.error("Start date has to come before end date.")

st.title("Nairobi Forex Corner")

stocks = ("AAPL", "AMD", "AMZN", "FB", "GOOG", "MSFT", "NFLX", "NVDA", "QCOM", "TSLA")

stock_option = st.selectbox("Select stock:", stocks)   

if feature_option == "View historical data":

    charts = ("Open", "Close", "High", "Low", "Volume")

    chart_option = st.selectbox("Select chart:", charts) 

    stocks_data = yf.Ticker(stock_option)

    stocks_dataframe = stocks_data.history(period='id', start=START, end=END)

    display(chart_option)

    st.write(" *** ")

elif feature_option == "Predict future prices":

    stocks_data = yf.Ticker(stock_option)

    stocks_dataframe = stocks_data.history(period='id', start = DEFAULT_START, end = END)

    data = load_prediction_data(stock_option)

    data_ = data[["Date", "Close"]]

    data_.columns = ["ds", "y"]

    model = NeuralProphet()

    model.fit(data_)

    future = model.make_future_dataframe(data_, periods=30)

    forecast = model.predict(future)

    fig = model.plot(forecast)

    st.write(fig)
