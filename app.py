import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import yfinance as yf
from PIL import Image

image = Image.open('logo.png')
st.image(image, use_column_width=True)

st.title("NASDAQ-100 App")

st.markdown("""
This app displays **NASDAQ 100** data
The data can also be exported as a csv file
""")

st.sidebar.header("User Input Features")

# Web scrapping NASDAQ data
@st.cache
def load_data():
    url = 'https://en.wikipedia.org/wiki/NASDAQ-100'
    html = pd.read_html(url, header=0)
    df = html[3]
    return df

df = load_data()
sector = df.groupby('GICS Sector')

# Sidebar: Sector selection
sorted_sector = sorted(df['GICS Sector'].unique())
selected_sector = st.sidebar.multiselect("Sector", sorted_sector, sorted_sector)

# Filter Data
df_selected_sector = df[(df['GICS Sector'].isin(selected_sector))]

st.header("Display Companies in Selected Sector")
st.write("Data Dimension: " + str(df_selected_sector.shape[0]) + " rows and " + str(df_selected_sector.shape[1]) + " columns")
st.dataframe(df_selected_sector)

# Donwnload SP500 data
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="NASDAQ100.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)

data = yf.download(
    tickers=list(df_selected_sector[:10].Ticker),
    start = "2020-01-01",
    end = "2020-12-30",
    interval = "1d",
    group_by = 'ticker',
    auto_adjust = True,
    prepost = True,
    threads = True,
    proxy = None
)

# Plot closing price
def price_plot(symbol):
    df = pd.DataFrame(data[symbol].Close)
    df['Date'] = df.index
    plt.fill_between(df.Date, df.Close, color='green', alpha=0.3)
    plt.plot(df.Date, df.Close, color='skyblue', alpha=0.8)
    plt.xticks(rotation=90)
    plt.title(symbol, fontweight='bold')
    plt.xlabel('Date', fontweight='bold')
    plt.ylabel('Closing Price', fontweight='bold')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    return st.pyplot()

number_slider = st.sidebar.slider("Number of Companies", 1, 5)

if st.button("Show Plots"):
    st.header("Closing Price")
    for i in list(df_selected_sector.Ticker)[:number_slider]:
        price_plot(i)


    