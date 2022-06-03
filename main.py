# Copyright 2022 by Georgios Charitos.
# All rights reserved.

import xlsxwriter
import sys
from datetime import datetime
from StockPrices import StockPrices

def add_zero_prefix_if_less_than_ten(integer):
    if integer < 10:
        integerStr = '0' + str(integer)
    else:
        integerStr = str(integer)
    return integerStr

def main():
    stockPrices = StockPrices(sys.argv)

    stock_symbols = ['ENPH','OTLY','PLTR','ZM','COIN','DKNG','AMD','RDFN','NFLX','JWN',
                     'TTD','SQ','CRSR','AMZN','PYPL','HNST','ADBE','SBUX','NVDA','NKE',
                     'SHOP','W','JPM','V','TTCF','GS','ETSY','MSFT','DIS','ABNB','SAM',
                     'FB','GOOGL','BRK-B','WBA','NET','AAPL','KO','TSLA','BYND','CSCO']

    stocks_list = stockPrices.request_stock_prices(stock_symbols)

    dateTimeObj = datetime.now()
    dateTimeStr = add_zero_prefix_if_less_than_ten(dateTimeObj.year) + '-' + add_zero_prefix_if_less_than_ten(dateTimeObj.month) + '-' + add_zero_prefix_if_less_than_ten(dateTimeObj.day)
    dateTimeStr = dateTimeStr + '_' + add_zero_prefix_if_less_than_ten(dateTimeObj.hour) + '.' + add_zero_prefix_if_less_than_ten(dateTimeObj.minute) + '.' + add_zero_prefix_if_less_than_ten(dateTimeObj.second)
    workbook = xlsxwriter.Workbook('Stocks_' + dateTimeStr + '.xlsx')
    worksheet = workbook.add_worksheet()

    for row_num, stock in enumerate(stocks_list):
        worksheet.write('A' + str(row_num + 1), stock.symbol)
        worksheet.write('B' + str(row_num + 1), stock.name)
        worksheet.write('C' + str(row_num + 1), stock.price)

    workbook.close()


if __name__ == '__main__':
    main()
