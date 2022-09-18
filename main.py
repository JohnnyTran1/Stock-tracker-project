import pandas as pd
# import streamlit as st

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

if __name__ == "__main__":
    df = get_spy()
    print(df)
    # print(df.iloc[0].PercentageChg)