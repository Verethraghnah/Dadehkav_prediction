# pip install streamlit fbprophet yfinance plotly
import streamlit as st
from datetime import date
import requests
import numpy as np
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly
from plotly import graph_objs as go
import streamlit as st
import pandas as pd
import numpy as np
from fbprophet import Prophet
from fbprophet.diagnostics import performance_metrics
from fbprophet.diagnostics import cross_validation
from fbprophet.plot import plot_cross_validation_metric
import base64
from fbprophet.plot import add_changepoints_to_plot
from fbprophet.plot import plot_plotly
import plotly.offline as py
from fbprophet.plot import add_changepoints_to_plot
from fbprophet.plot import plot_components_plotly
from PIL import Image
import datetime as dt
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import neuralprophet
from PIL import Image
image = Image.open('banner.jpg')
st.image(image, caption='Dadehkav Stock Prediction App')
st.title('Stock Prediction App')

today = dt.date.today()

before = today - dt.timedelta(days=3653)
start_date = st.sidebar.date_input('Start date', before)
end_date = st.sidebar.date_input('End date', today)

if start_date < end_date:
    st.sidebar.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
else:
    st.sidebar.error('Error: End date must fall after start date.')

st.title("Forcaster")

function_list = ['fbprophet', 'Neural Networks']
sidebar_function = st.sidebar.selectbox("Choose the forecasting method", function_list)
crypotocurrencies = (
    'BTC-USD', 'ETH-USD', 'BNB-USD', 'ADA-USD', 'SAND-USD', 'MANA-USD', 'XRP-USD', 'LTC-USD', 'EOS-USD', 'XLM-USD',
    'TRX-USD','ETC-USD', 'SHIB-USD', 'DOGE-USD', 'TRX-USD', 'SOL-USD', 'FTM-USD', 'MATIC-USD')




selected_stock = st.selectbox('Select dataset for prediction', crypotocurrencies)

n_years = st.slider('Weeks of prediction:', 1, 4)
period = n_years * 7


@st.cache
def load_data(ticker):
    data = yf.download(ticker, start_date, end_date)
    data.reset_index(inplace=True)
    return data


data_load_state = st.text('Loading data...')
data = load_data(selected_stock)
data_load_state.text('Loading data... done!')

st.subheader('Raw data')
st.write(data.tail())

# Plot raw data
fig = px.line(data, x='Date', y='Close')
st.plotly_chart(fig)

# Prophet model
df_train = data[['Date', 'Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

if sidebar_function == "Neural Networks":
    st.write("running the code for Neural Networks..."
             "itmay take a while ")
    model = neuralprophet.NeuralProphet(seasonality_mode='multiplicative', daily_seasonality=False,
                                        weekly_seasonality='auto', yearly_seasonality='auto', n_forecasts=60,
                                        batch_size=32, epochs=100)
    metrics = model.fit(df_train, freq='D')
    future = model.make_future_dataframe(df_train, periods=period, n_historic_predictions=len(df_train))
    forecast = model.predict(future)
    st.write("Forecast Results")
    fign = model.plot(forecast)
    st.pyplot(fign)
    st.write("Forecast components")
    fig_comp = model.plot_components(forecast)
    st.write(fig_comp)
    fig_param = model.plot_parameters()
    st.pyplot(fig_param)

else:
    st.write("running the code for fbprophet..."
             "itmay take a while ")
    m = Prophet(seasonality_mode='multiplicative')
    m.add_seasonality(name='monthly', period=30.5, fourier_order=5)
    # m.add_country_holidays(country_name='US')
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)
    st.write("Forecast Results")
    figf = m.plot(forecast)
    st.plotly_chart(figf)
    st.write("Forecast components")
    figff = plot_components_plotly(m, forecast)
    st.write(figff)