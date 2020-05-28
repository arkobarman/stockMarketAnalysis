import pandas as pd
import matplotlib.pyplot as plt
from APIs import general_APIs as general

plt.style.use('seaborn-darkgrid')

# Tick interval on date axis when plotting
every_nth = 20

def getExponentialMovingAverage(dataFr, colName='Close', nDays=12):
    # Calculate SMA
    sma = dataFr[colName].rolling(nDays).mean()
    modifiedCol = dataFr[colName].copy()
    # Replace initial values with NA
    modifiedCol.iloc[0:nDays] = sma[0:nDays]
    
    dataFr['EMA_{}'.format(nDays)] = modifiedCol.ewm(span=nDays, adjust=False).mean()
    
    return dataFr

def getMACD(companyName='GOOG', nDays_short=12, nDays_long=26):
    # Load dataframe for company
    dataFr = general.loadCompanyData(companyName)
    
    # Create exponential moving average columns
    dataFr = getExponentialMovingAverage(dataFr, colName='Close', nDays=nDays_short)
    dataFr = getExponentialMovingAverage(dataFr, colName='Close', nDays=nDays_long)