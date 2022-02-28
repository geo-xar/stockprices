# Copyright 2022 by Georgios Charitos.
# All rights reserved.

import xlsxwriter
import sys
from StockPrices import StockPrices

def main():
    stockPrices = StockPrices(sys.argv)

    stock_symbols = ['MTTR','AFRM','PYPL','SHOP','FB','LMND','SQ','BYND','PLTR','NFLX','HOOD',
                     'TSLA','COIN','SOFI','ETSY','ZM','HNST','BABA','WBA','SAM','ADSK','AMD',
                     'NVDA','TTCF','ADBE','GS','SBUX','JPM','JWN','OTLY','NKE','AMZN','AAPL',
                     'DKNG','GOOGL','MSFT','BRK-B','ABNB','DIS','KO','V','ENPH','NET','CRSR']

    stocks_list = stockPrices.request_stock_prices(stock_symbols)

    workbook = xlsxwriter.Workbook('Stocks.xlsx')
    worksheet = workbook.add_worksheet()

    for row_num, stock in enumerate(stocks_list):
        worksheet.write('A' + str(row_num), stock.symbol)
        worksheet.write('B' + str(row_num), stock.name)
        worksheet.write('C' + str(row_num), str(stock.price))

    workbook.close()

    #for stock in stocks_list:
    #    print(f"{stock.symbol}, {stock.name}, {stock.price}")


if __name__ == '__main__':
    main()
