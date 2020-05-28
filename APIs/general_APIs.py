import os
import pandas as pd

import yfinance as yf

from datetime import date 
from datetime import timedelta 

def loadCompanyData(companyName='GOOG', start='2019-10-31'):

    # Get today's date
    today = date.today()
    
    # Get yesterday's date
    yesterday = today - timedelta(days = 1) 
    
    # get data on this ticker
    tickerData = yf.Ticker(companyName)

    # get the historical prices for this ticker
    tickerFr = tickerData.history(period='1d', start=start, end=yesterday)
    
    # Insert a date column
    dates = tickerFr.index.values
    dateList = []
    for stockDate in dates:
        dateList.append(stockDate.astype(str)[:10])
    tickerFr['Date'] = dateList

    # return your data
    return tickerFr