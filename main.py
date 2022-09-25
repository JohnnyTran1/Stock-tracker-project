import streamlit as st
import pandas as pd

from bs4 import BeautifulSoup as bs
import requests

def get_spy():
    url = 'https://www.slickcharts.com/sp500'
    request = requests.get(url,headers={'User-Agent': 'Mozilla/5.0'})
    soup = bs(request.text, "lxml")
    stats = soup.find('table',class_='table table-hover table-borderless table-sm')
    df =pd.read_html(str(stats))[0]
    df['PercentageChg'] = df['% Chg'].str.strip('()-%')
    df['PercentageChg'] = pd.to_numeric(df['PercentageChg'])
    df['Chg'] = pd.to_numeric(df['Chg'])
    return df

def get_qqq():
    df = pd.DataFrame()
    urls = ['https://www.dividendmax.com/market-index-constituents/nasdaq-100',
    'https://www.dividendmax.com/market-index-constituents/nasdaq-100?page=2',
    'https://www.dividendmax.com/market-index-constituents/nasdaq-100?page=3']
    for url in urls:
        request = requests.get(url,headers={'User-Agent': 'Mozilla/5.0'})
        soup = bs(request.text, "lxml")
        stats = soup.find('table',class_='mdc-data-table__table')
        temp =pd.read_html(str(stats))[0]
        df = df.append(temp)
        df.rename(columns={'Market Cap':'Market Cap $bn'},inplace=True)
        df['Market Cap $bn'] = df['Market Cap $bn'].str.strip("£$bn")
        df['Market Cap $bn'] = pd.to_numeric(df['Market Cap $bn'])
        df = df.sort_values('Market Cap $bn',ascending=False)
    return df

if __name__ == "__main__":
    st.set_page_config(page_title="My Webpage", page_icon=":tada:", layout="wide")
    st.subheader("Hi, I am Johnny Tran :wave:")
    st.title("A date list of all S&P 500 symbols")
    st.write("[Learn More >](https://www.slickcharts.com/sp500)")
    df = get_spy()
    print(df)
    st.dataframe(df)
