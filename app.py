import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import yfinance as yf

st.title("S&P 500 App")

st.markdown("""
This app displays **S&P 500** data
The data can also be exported as a csv file
""")

st.sidebar.header("User Input Features")

# Web scrapping S&P data
@st.cache
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header=0)
    df = html[0]
    return df

df = load_data()
sector = df.groupby('GICS Sector')



