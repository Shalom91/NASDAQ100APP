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

# Sidebar: Sector selection
sorted_sector = sorted(df['GICS Sector'].unique())
selected_sector = st.sidebar.multiselect("Sector", sorted_sector)

# Filter Data
df_selected_sector = df[(df['GICS Sector'].isin(selected_sector))]

st.header("Display Companies in Selected Sector")
st.write("Data Dimension: " + str(df_selected_sector.shape[0]) + " and " + str(df_selected_sector.shape[1]) + " columns")
st.dataframe(df_selected_sector)
