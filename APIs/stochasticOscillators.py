import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.axes import Axes

import mplfinance as mpf

from APIs import general_APIs as general

plt.style.use('seaborn-darkgrid')

# Stochastic K
def STOK(dataFr, n=14):
    close = dataFr['Close']
    low = dataFr['Low']
    high = dataFr['High']
    STOK = ( (close - low.rolling(n).min()) / (high.rolling(n).max() - low.rolling(n).min()) ) * 100
    return STOK

# Stochastic D
def STOD(dataFr, n1=14, n2=3):
    close = dataFr['Close']
    low = dataFr['Low']
    high = dataFr['High']
    STOK = ( (close - low.rolling(n1).min()) / (high.rolling(n1).max() - low.rolling(n1).min()) ) * 100
    STOD = STOK.rolling(n2).mean()
    return STOD


# Compute and plot stochastic %K and %D
def computeAndPlotFastStochasticOscillator(companyName='GOOG', n1=14, n2=3, start='2019-10-31', every_nth = 20):
    # Load dataframe for company
    dataFr = general.loadCompanyData(companyName, start=start)
    
    dataFr['%K'] = STOK(dataFr, n1)
    dataFr['%D'] = STOD(dataFr, n1, n2)
    
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
             dataFr['%K'].to_list(),
             label='Fast %K',
             c='r');
    ax1.plot(dataFr['Date'].to_list(),
             dataFr['%D'].to_list(),
             label='Fast %D',
             c='k');
    ax1.axhline(y=50, linestyle='-.')
    ax1.axhline(y=20, linestyle='-')
    ax1.axhline(y=80, linestyle='-')
    for n, label in enumerate(ax1.xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)
    plt.xticks(rotation=45, ha="right");
    plt.yticks([0, 20, 50, 80, 100])
    plt.legend(prop={'size': 14});
    
    
# Compute and plot slow stochastic %K and %D
def computeAndPlotSlowStochasticOscillator(companyName='GOOG', n1=14, n2=3, start='2019-10-31', every_nth = 20):
    # Load dataframe for company
    dataFr = general.loadCompanyData(companyName, start=start)
    
    dataFr['fast_%K'] = STOK(dataFr, n1)
    # SMA
    dataFr['slow_%K'] = dataFr['fast_%K'].rolling(n2).mean()
    dataFr['slow_%D'] = dataFr['slow_%K'].rolling(n2).mean()
    
    fig = plt.figure(figsize=(20,10))
    # set height ratios for sublots
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1]) 

    # the fisrt subplot
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
             dataFr['slow_%K'].to_list(),
             label='Slow %K',
             c='r');
    ax1.plot(dataFr['Date'].to_list(),
             dataFr['slow_%D'].to_list(),
             label='Slow %D',
             c='k');
    ax1.axhline(y=50, linestyle='-.')
    ax1.axhline(y=20, linestyle='-')
    ax1.axhline(y=80, linestyle='-')
    for n, label in enumerate(ax1.xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)
    plt.xticks(rotation=45, ha="right");
    plt.yticks([0, 20, 50, 80, 100])
    plt.legend(prop={'size': 14});
    
#     mpf.plot(dataFr)

# Compute and plot full stochastic %K and %D
def computeAndPlotFullStochasticOscillator(companyName='GOOG', n1=14, n2=3, n3=3, start='2019-10-31', every_nth = 20):
    # Load dataframe for company
    dataFr = general.loadCompanyData(companyName, start=start)
    
    dataFr['fast_%K'] = STOK(dataFr, n1)
    # SMA
    dataFr['full_%K'] = dataFr['fast_%K'].rolling(n2).mean()
    dataFr['full_%D'] = dataFr['full_%K'].rolling(n3).mean()
    
    fig = plt.figure(figsize=(20,10))
    # set height ratios for sublots
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1]) 

    # the fisrt subplot
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
             dataFr['full_%K'].to_list(),
             label='Full %K',
             c='r');
    ax1.plot(dataFr['Date'].to_list(),
             dataFr['full_%D'].to_list(),
             label='Full %D',
             c='k');
    ax1.axhline(y=50, linestyle='-.')
    ax1.axhline(y=20, linestyle='-')
    ax1.axhline(y=80, linestyle='-')
    for n, label in enumerate(ax1.xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)
    plt.xticks(rotation=45, ha="right");
    plt.yticks([0, 20, 50, 80, 100])
    plt.legend(prop={'size': 14});
    
#     mpf.plot(dataFr)

