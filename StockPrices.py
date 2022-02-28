import requests
import sys

class Stock: 
    def __init__(self, symbol, name, price): 
        self.symbol = symbol 
        self.name = name
        self.price = price

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

    def request_stock_prices(self, stock_symbols):
        """
        Request the stock prices using Yahoo Finance API.
        Return a stocks list.
        """
        yfApiUrl = 'https://yfapi.net/v6/finance/quote'
        headers = {"x-api-key": self.api_key}
        stock_symbols_str = ''
        for symbol in stock_symbols:
            stock_symbols_str = stock_symbols_str + symbol + ','
        stock_symbols_str = stock_symbols_str[:-1]

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
                    stocks_list.append(Stock(symbol, display_name, regular_market_price))

                return stocks_list

            else: # status code != 200 success
                print(f"Response status code: {result.status_code}")
                sys.exit(1)
