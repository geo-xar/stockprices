# Copyright 2022 by Georgios Charitos.
# All rights reserved.

import xlsxwriter
import sys
from datetime import datetime
from StockPrices import StockPrices


def main():
    stock_prices = StockPrices(sys.argv)

    stock_symbols = ['NET','SQ','AMZN','ABNB','BRK-B','META','W','SAM','RDFN','TSLA',
                     'CSCO','DIS','AAPL','BYND','WBA','KO','ETSY','AMD','GS','HNST',
                     'GOOGL','MSFT','ADBE','COIN','NVDA','JPM','V','PYPL','NKE','SHOP',
                     'CRSR','TTCF','SBUX','NFLX','TTD','JWN','PLTR','ENPH']

    stocks_list = stock_prices.request_stock_prices(stock_symbols)

    date_time_str = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
    workbook = xlsxwriter.Workbook('Stocks_' + date_time_str + '.xlsx')
    worksheet = workbook.add_worksheet()

    for row_num, stock in enumerate(stocks_list):
        worksheet.write('A' + str(row_num + 1), stock.symbol)
        worksheet.write('B' + str(row_num + 1), stock.name)
        worksheet.write('C' + str(row_num + 1), stock.price)

    workbook.close()


if __name__ == '__main__':
    main()
