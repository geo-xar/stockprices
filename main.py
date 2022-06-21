# Copyright 2022 by Georgios Charitos.
# All rights reserved.

import sys
from datetime import datetime

import streamlit as st

from StockPrices import StockPrices


def main():
    stock_prices = StockPrices(sys.argv)

    stock_symbols = ['NET','SQ','AMZN','ABNB','BRK-B','META','W','SAM','RDFN','TSLA',
                     'CSCO','DIS','AAPL','BYND','WBA','KO','ETSY','AMD','GS','HNST',
                     'GOOGL','MSFT','ADBE','COIN','NVDA','JPM','V','PYPL','NKE','SHOP',
                     'CRSR','TTCF','SBUX','NFLX','TTD','JWN','PLTR','ENPH']

    # request real time stock data
    if "real_time_stocks_df" not in st.session_state:
        st.session_state.real_time_stocks_df = stock_prices.request_real_time_stock_prices(stock_symbols)
    # output them into an excel spreadsheet (commented out)
    date_time_now_str = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
    # workbook_name = 'Stocks_' + date_time_now_str + '.xlsx'
    # real_time_stocks_df.to_excel(workbook_name)

    # request historical stock data
    if "stock_history_dict_of_dfs" not in st.session_state:
        st.session_state.stock_history_dict_of_dfs = stock_prices.request_historical_stock_prices(stock_symbols)

    # Create the dashboard
    st.set_page_config(layout="wide")
    st.title("Stock Prices Application")

    st.header(f"Real time stock prices retrieved at {date_time_now_str}:")
    st.dataframe(st.session_state.real_time_stocks_df)

    st.header(f"Historical stock data:")
    st.subheader("Select company's symbol to display historical stock price chart:")
    symbol = st.selectbox("Symbol", st.session_state.stock_history_dict_of_dfs.keys())
    st.line_chart(st.session_state.stock_history_dict_of_dfs[symbol])


if __name__ == '__main__':
    main()
