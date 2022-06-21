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

    # Create the dashboard
    st.set_page_config(layout="wide")
    st.title("Stock Prices Application")

    # request real time stock data and display it
    if "real_time_stocks_df" not in st.session_state:
        st.session_state.real_time_stocks_df = stock_prices.request_real_time_stock_prices(stock_symbols)
    date_time_now_str = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
    st.header(f"Real time stock prices retrieved at {date_time_now_str}:")
    st.dataframe(st.session_state.real_time_stocks_df)

    # output them into an excel spreadsheet (commented out)
    # workbook_name = 'Stocks_' + date_time_now_str + '.xlsx'
    # real_time_stocks_df.to_excel(workbook_name)

    # request historical stock data and display it
    st.header(f"Historical stock data:")
    st.subheader("Please select a different time interval and range if required:")
    valid_intervals = ["1d", "1wk", "1mo", "1m", "5m", "15m"]
    interval = st.selectbox("Time Interval", valid_intervals)
    valid_ranges = ["1y", "5y", "max", "1d", "5d", "1mo", "3mo", "6mo"]
    time_range = st.selectbox("Time Range", valid_ranges)

    if ("stock_history_dict_of_dfs", interval, time_range) not in st.session_state:
        st.session_state[("stock_history_dict_of_dfs", interval, time_range)] = \
            stock_prices.request_historical_stock_prices(stock_symbols, interval, time_range)

    st.subheader("Select company's symbol to display historical stock price chart:")
    symbol = st.selectbox("Symbol", st.session_state[("stock_history_dict_of_dfs", interval, time_range)].keys())
    st.line_chart(st.session_state[("stock_history_dict_of_dfs", interval, time_range)][symbol])


if __name__ == '__main__':
    main()
