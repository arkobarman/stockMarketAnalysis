import os
import pandas as pd

from yahoo_fin.stock_info import get_data

from datetime import date 
from datetime import timedelta 

def loadCompanyData(companyName='GOOG', start='2019-10-31'):

    # get the historical prices for this ticker
    tickerFr = get_data(companyName, start_date=start, interval="1d")
    
    # Insert a date column
    dates = tickerFr.index.values
    dateList = []
    for stockDate in dates:
        dateList.append(stockDate.astype(str)[:10])
    tickerFr['Date'] = dateList

    # return your data
    return tickerFr