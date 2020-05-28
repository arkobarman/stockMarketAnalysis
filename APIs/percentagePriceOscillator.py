import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.axes import Axes

from APIs import general_APIs as general

plt.style.use('seaborn-darkgrid')

# Exponential moving average calculator
def getExponentialMovingAverage(dataFr, colName='Close', nDays=12):
    # Calculate SMA
    sma = dataFr[colName].rolling(nDays).mean()
    modifiedCol = dataFr[colName].copy()
    # Replace initial values with NA
    modifiedCol.iloc[0:nDays] = sma[0:nDays]
    
    dataFr['EMA_{}'.format(nDays)] = modifiedCol.ewm(span=nDays, adjust=False).mean()
    
    return dataFr

def getSignalLine(dataFr, colName='PPO', nDays=9, n2=26):
    # Calculate SMA
    sma = dataFr[colName].rolling(nDays).mean()
    modifiedCol = dataFr[colName].copy()
    # Replace initial values with NA
    modifiedCol.iloc[0:nDays+n2] = sma[0:nDays+n2]
    
    dataFr['SignalLine'.format(nDays)] = modifiedCol.ewm(span=nDays, adjust=False).mean()
    
    return dataFr

# Compute and plot percentage price oscillator
def computeAndPlotPercentagePriceOscillator(companyName='GOOG', start='2020-01-01', n1=12, n2=26, every_nth=20):
    # Load dataframe for company
    dataFr = general.loadCompanyData(companyName, start=start)
    
    dataFr = getExponentialMovingAverage(dataFr, nDays=n1)
    dataFr = getExponentialMovingAverage(dataFr, nDays=n2)
    
    dataFr['PPO'] = dataFr.apply(lambda row: (row['EMA_{}'.format(n1)] - row['EMA_{}'.format(n2)])*100/row['EMA_{}'.format(n2)], axis = 1)
    
    dataFr = getSignalLine(dataFr, colName='PPO', nDays=9, n2=n2)
    
    dataFr['PPO_histogram'] = dataFr.apply(lambda row: row['PPO'] - row['SignalLine'], axis=1)
    
    # Plot data
    fig = plt.figure(figsize=(20,10))
    # set height ratios for sublots
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1]) 

    # the first subplot
    ax0 = plt.subplot(gs[0])
#     ax0.plot(dataFr['Date'].to_list(),
#                 dataFr['Close'].to_list(),
#                 label='Closing');
    highList = dataFr['High'].to_list()
    lowList = dataFr['Low'].to_list()
    dateList = dataFr['Date'].to_list()
    closeList = dataFr['Close'].to_list()
    lowerError = [a-b for a, b in zip(closeList, lowList)]
    upperError = [a-b for a, b in zip(highList, closeList)]
    ax0.errorbar(x=dateList, y=closeList, yerr=[lowerError, upperError], fmt='o')
    for n, label in enumerate(ax0.xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)
    plt.xticks(rotation=45, ha="right");
    
    # the second subplot
    ax1 = plt.subplot(gs[1], sharex=ax0)
    ax1.plot(dataFr['Date'].to_list(),
             dataFr['PPO'].to_list(),
             label='PPO',
             c='r');
    ax1.plot(dataFr['Date'].to_list(),
             dataFr['SignalLine'].to_list(),
             label='Signal Line',
             c='k');
    ax1.bar(dataFr['Date'].to_list(),
            dataFr['PPO_histogram'].to_list(),
            label='PPO histogram',
            width=0.2,
            color='g')
    for n, label in enumerate(ax1.xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)
    plt.xticks(rotation=45, ha="right");
    plt.legend(prop={'size': 12}, loc='upper left');