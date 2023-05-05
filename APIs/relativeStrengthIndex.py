import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.axes import Axes

from APIs import general_APIs as general

# https://stackoverflow.com/questions/57006437/calculate-rsi-indicator-from-pandas-dataframe


# Rolling Moving Average
def rma(x, n, y0):
        a = (n-1) / n
        ak = a**np.arange(len(x)-1, -1, -1)
        return np.append(y0, np.cumsum(ak * x) / ak / n + y0 * a**np.arange(1, len(x)+1))
    
def getRSI(companyName='GOOG', start='2020-01-01', n=14, every_nth=20):
    # Load dataframe for company
    dataFr = general.loadCompanyData(companyName, start=start)
    dataFr.index = range(len(dataFr))
    

    dataFr['change'] = dataFr['Close'].diff()
    dataFr['gain'] = dataFr.change.mask(dataFr.change < 0, 0.0)
    dataFr['loss'] = -dataFr.change.mask(dataFr.change > 0, -0.0)
    dataFr.loc[n:,'avg_gain'] = rma( dataFr.gain[n+1:].values, n, dataFr.loc[:n, 'gain'].mean())
    dataFr.loc[n:,'avg_loss'] = rma( dataFr.loss[n+1:].values, n, dataFr.loc[:n, 'loss'].mean())
    dataFr['rs'] = dataFr.avg_gain / dataFr.avg_loss
    dataFr['rsi_14'] = 100 - (100 / (1 + dataFr.rs))
    
    
    # Plot data
    fig = plt.figure(figsize=(20,15))
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
    lowerError = [a-min(a,b) for a, b in zip(closeList, lowList)]
    upperError = [max(a,b)-b for a, b in zip(highList, closeList)]
    ax0.errorbar(x=dateList, y=closeList, yerr=[lowerError, upperError], fmt='o')
    for n, label in enumerate(ax0.xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)
    plt.xticks(rotation=45, ha="right");
    ax0.tick_params(axis='y', labelsize=20)
    ax0.tick_params(axis='x', labelsize=16)
    
    # the second subplot
    ax1 = plt.subplot(gs[1], sharex=ax0)
    ax1.plot(dataFr['Date'].to_list(),
             dataFr['rsi_14'].to_list(),
             label='RSI',
             c='c');
    ax1.axhline(y=50, linestyle='-.', color='k')
    ax1.axhline(y=30, linestyle='-', color='g')
    ax1.axhline(y=70, linestyle='-', color='r')
    for n, label in enumerate(ax1.xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)
    plt.xticks(rotation=45, ha="right");
    plt.yticks([0, 30, 50, 70, 100])
    plt.legend(prop={'size': 15}, loc='upper left');
    ax1.tick_params(axis='y', labelsize=20)
    ax1.tick_params(axis='x', labelsize=16)
