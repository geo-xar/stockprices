# Copyright 2022 by Georgios Charitos.
# All rights reserved.

import xlsxwriter
import sys
from datetime import datetime
from StockPrices import StockPrices

def main():
    stockPrices = StockPrices(sys.argv)

    stock_symbols = ['MTTR','AFRM','SHOP','LMND','PYPL','FB','BYND','ZM','PLTR','NFLX','COIN','HOOD','SOFI',
                     'BABA','AMD','HNST','TSLA','SQ','ADSK','OTLY','SAM','JPM','NVDA','GS','ADBE','ABNB',
                     'WBA','NKE','DKNG','AMZN','SBUX','TTCF','ETSY','DIS','V','MSFT','AAPL','GOOGL',
                     'BRK-B','NET','KO','CRSR','JWN','ENPH']

    stocks_list = stockPrices.request_stock_prices(stock_symbols)

    dateTimeObj = datetime.now()
    dateTimeStr = str(dateTimeObj.year) + 'y' + str(dateTimeObj.month) + 'm' + str(dateTimeObj.day) + 'd' + str(dateTimeObj.hour) + 'h' + str(dateTimeObj.minute) + 'm' + str(dateTimeObj.second) + 's'
    workbook = xlsxwriter.Workbook('Stocks' + dateTimeStr + '.xlsx')
    worksheet = workbook.add_worksheet()

    for row_num, stock in enumerate(stocks_list):
        worksheet.write('A' + str(row_num + 1), stock.symbol)
        worksheet.write('B' + str(row_num + 1), stock.name)
        worksheet.write('C' + str(row_num + 1), str(stock.price))

    workbook.close()


if __name__ == '__main__':
    main()
