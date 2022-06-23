# Copyright 2022 by Georgios Charitos.
# All rights reserved.

import collections
import sys
from datetime import datetime

import pandas as pd
import requests


class StockPrices(object):
    """
    Class that retrieves and holds all the stock prices.
    """

    def __init__(self, sysArgs):
        """
        Retrieve API key from the main application arguments list.
        """
        if len(sysArgs) < 2:
            print("Please provide an API key as an application argument")
            sys.exit(1)

        self.api_key = sysArgs[1]

    def request_real_time_stock_prices(self, stock_symbols):
        """
        Request real time stock prices using Yahoo Finance API.
        Return a stocks dataframe.

        :param stock_symbols: Stock symbols list of stocks to be retrieved
        :returns: pd.Dataframe
        """
        yfApiUrl = 'https://yfapi.net/v6/finance/quote'
        headers = {"x-api-key": self.api_key}
        stock_symbols_str = ','.join(stock_symbols)

        try:
            response = requests.get(yfApiUrl, params={"region": "US", "lang": "en", "symbols": stock_symbols_str}, headers=headers)
        except requests.RequestException as e:
            print(f"An error has occurred while processing Yahoo Finance API - GET request.")
            sys.exit(1)
        else:

            if response.ok: # status code 200 success

                # retrieve response body as JSON
                data = response.json()

                stocks_list = []
                # iterate list of stocks
                for stock in data['quoteResponse']['result']:

                    # retrieve stock ticker symbol
                    symbol = stock['symbol']

                    # retrieve stock displayName
                    # certain stocks do not have a displayName
                    # in such cases try to retrieve their longName
                    if 'displayName' not in stock:
                        if 'longName' not in stock:
                            print(f"Cannot find neither displayName nor longName for {symbol} with payload {stock}")
                            sys.exit(1)
                        else:
                            display_name = stock['longName']
                    else:
                        display_name = stock['displayName']

                    regular_market_price = stock['regularMarketPrice']

                    # Store the stock details to a list
                    stocks_list.append((symbol, display_name, regular_market_price))

                # create a pandas dataframe from the stock list
                stocks_df = pd.DataFrame(stocks_list, columns=["Symbol", "Display Name", "Regular Market Price"])
                stocks_df.sort_values("Symbol", inplace=True, ignore_index=True)
                return stocks_df

            else: # status code != 200 success
                print(f"Response status code: {response.status_code}")
                sys.exit(1)

    def request_historical_stock_prices(self, stock_symbols, interval, time_range):
        """
        Request historical stock prices using Yahoo Finance API.
        Return a dictionary of stocks dataframes.

        :param stock_symbols: Stock symbols list of stocks to be retrieved
        :param interval: Time interval for values-breakpoints retrieval
        :param time_range: Time range for values-breakpoints retrieval
        :returns: dictionary of pd.Dataframes
        """
        yfApiUrl = 'https://yfapi.net/v8/finance/spark'
        headers = {"x-api-key": self.api_key}

        # symbols need to be split into chunks of 20 because API only accepts up to 20 symbols per request
        stock_symbol_chunks = [stock_symbols[x:x + 20] for x in range(0, len(stock_symbols), 20)]
        stock_symbol_chunks_str = [','.join(chunk) for chunk in stock_symbol_chunks]

        stock_dataframes_dict = {}
        for chunk in stock_symbol_chunks_str:
            try:
                response = requests.get(yfApiUrl, params={"interval": interval, "range": time_range, "symbols": chunk},
                                        headers=headers)
            except requests.RequestException as e:
                print(f"An error has occurred while processing Yahoo Finance API - GET request.")
                sys.exit(1)
            else:

                if response.ok: # status code 200 success

                    # retrieve response body as JSON
                    data = response.json()

                    # iterate list of stocks
                    for stock_name, stock_data in data.items():

                        # extract stock ticker symbol
                        symbol = stock_name

                        # extract timestamps
                        timestamps = stock_data['timestamp']
                        # convert them from integers to datetimes
                        timestamps = [datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
                                      for timestamp in timestamps]

                        # extract close values
                        close_values = stock_data['close']

                        # Store the stock details to the dict
                        stock_dataframes_dict[symbol] = pd.DataFrame(list(zip(timestamps, close_values)),
                                                                     columns=["Time Stamp", "Close Values"])
                        stock_dataframes_dict[symbol]["Time Stamp"] = pd.to_datetime(
                            stock_dataframes_dict[symbol]["Time Stamp"])
                        stock_dataframes_dict[symbol] = stock_dataframes_dict[symbol].set_index("Time Stamp")

                else: # status code != 200 success
                    print(f"Response status code: {response.status_code}")
                    sys.exit(1)

        # sort the dictionary by its keys
        stock_dataframes_dict = collections.OrderedDict(sorted(stock_dataframes_dict.items()))
        return stock_dataframes_dict
