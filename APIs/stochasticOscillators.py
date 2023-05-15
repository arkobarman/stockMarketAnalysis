import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.axes import Axes
from matplotlib.patches import Rectangle

import mplfinance as mpf

from APIs import general_APIs as general

plt.style.use('seaborn-darkgrid')

# Stochastic K
def STOK(dataFr, n=14):
    close = dataFr['close']
    low = dataFr['low']
    high = dataFr['high']
    STO_K = ( (close - low.rolling(n).min()) / (high.rolling(n).max() - low.rolling(n).min()) ) * 100
    return STO_K

# Stochastic D
def STOD(dataFr, n1=14, n2=3):
    STO_K = STOK(dataFr, n=n1)
    STO_D = STO_K.rolling(n2).mean()
    return STO_D

def calculateAndPlotOverbought(dataFr, colName, ax0, ax1, overbought_th=80):
    '''
    dataFr = data frame containing all information
    colName = column name in data frame to use for calculations
    overbought_th = threshold to consider overbought
    ax0 = axis for stock prices plot
    ax1 = axis for %K and %D plot
    '''
    # Calculate overbought & strong region (%K goes above overbought_th and stays above overbought_th)
    dataFr['overbought'] = dataFr[colName].gt(overbought_th)
    
    # add overbought rectangles to plot + dotted lines when %K falls below resistance (overbought_th)
    overbought = False
    start_date = None
    stop_date = None
    count = -1
    for (date, overbought_on_day) in zip(tuple(dataFr['Date'].to_list()),
                                         tuple(dataFr['overbought'].to_list())):
        count += 1
        if overbought:
            if overbought_on_day:
                continue
            else:
                stop_date = count
                overbought = False
                # Draw rectangle here
                ax1.add_patch(Rectangle((start_date, overbought_th), 
                                        stop_date-start_date, 
                                        100 - overbought_th,
                                        facecolor = 'orange',
                                        fill=True,
                                        alpha=0.35))
                
                # Draw dotted red lines at stop date (%K falls below resistance)
                ax0.axvline(x=stop_date, linestyle='--', color='red', linewidth=0.75)
                ax1.axvline(x=stop_date, linestyle='--', color='red', linewidth=0.75)
                
        else:
            if overbought_on_day:
                start_date = count
                overbought = True
                
    if overbought:
        stop_date = count
        # Draw rectangle here
        ax1.add_patch(Rectangle((start_date, overbought_th), 
                                stop_date-start_date, 
                                100 - overbought_th,
                                facecolor = 'orange',
                                fill=True,
                                alpha=0.35))
        
        # Draw dotted red lines at stop date (%K falls below resistance)
        ax0.axvline(x=stop_date, linestyle='--', color='red', linewidth=0.75)
        ax1.axvline(x=stop_date, linestyle='--', color='red', linewidth=0.75)
        
        
def calculateAndPlotOversold(dataFr, colName, ax0, ax1, oversold_th=20):
    '''
    dataFr = data frame containing all information
    colName = column name in data frame to use for calculations
    oversold_th = threshold to consider oversold
    ax0 = axis for stock prices plot
    ax1 = axis for %K and %D plot
    '''
    # Calculate oversold & weak region (%K goes below oversold_th and stays below oversold_th)
    dataFr['oversold'] = dataFr[colName].lt(oversold_th)
    
    # add oversold rectangles to plot + dotted lines when %K rises above support (oversold_th)
    oversold = False
    start_date = None
    stop_date = None
    count = -1
    for (date, oversold_on_day) in zip(tuple(dataFr['Date'].to_list()),
                                       tuple(dataFr['oversold'].to_list())):
        count += 1
        if oversold:
            if oversold_on_day:
                continue
            else:
                stop_date = count
                oversold = False
                # Draw rectangle here
                ax1.add_patch(Rectangle((start_date, 0), 
                                        stop_date-start_date, 
                                        oversold_th,
                                        facecolor = 'purple',
                                        fill=True,
                                        alpha=0.35))
                
                # Draw dotted red lines at stop date (%K falls below resistance)
                ax0.axvline(x=stop_date, linestyle='--', color='green', linewidth=0.75)
                ax1.axvline(x=stop_date, linestyle='--', color='green', linewidth=0.75)
                
        else:
            if oversold_on_day:
                start_date = count
                oversold = True
                
    if oversold:
        stop_date = count
        # Draw rectangle here
        ax1.add_patch(Rectangle((start_date, 0), 
                                stop_date-start_date, 
                                oversold_th,
                                facecolor = 'purple',
                                fill=True,
                                alpha=0.35))
        
        # Draw dotted red lines at stop date (%K falls below resistance)
        ax0.axvline(x=stop_date, linestyle='--', color='green', linewidth=0.75)
        ax1.axvline(x=stop_date, linestyle='--', color='green', linewidth=0.75)

# Compute and plot stochastic %K and %D
def computeAndPlotFastStochasticOscillator(companyName='GOOG', n1=14, n2=3, start='2019-10-31', every_nth = 20):
    # Load dataframe for company
    dataFr = general.loadCompanyData(companyName, start=start)
    
    dataFr['%K'] = STOK(dataFr, n1)
    dataFr['%D'] = STOD(dataFr, n1, n2)
    
    fig = plt.figure(figsize=(20,15))
    # set height ratios for sublots
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1]) 

    # the first subplot
    ax0 = plt.subplot(gs[0])
#     ax0.plot(dataFr['Date'].to_list(),
#                 dataFr['Close'].to_list(),
#                 label='Closing');
    highList = dataFr['high'].to_list()
    lowList = dataFr['low'].to_list()
    dateList = dataFr['Date'].to_list()
    closeList = dataFr['close'].to_list()
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
             dataFr['%K'].to_list(),
             label='Fast %K',
             c='k');
    ax1.plot(dataFr['Date'].to_list(),
             dataFr['%D'].to_list(),
             label='Fast %D',
             c='r');
    ax1.axhline(y=50, linestyle='-.')
    ax1.axhline(y=20, linestyle='-')
    ax1.axhline(y=80, linestyle='-')
    for n, label in enumerate(ax1.xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)
    plt.xticks(rotation=45, ha="right");
    plt.yticks([0, 20, 50, 80, 100])
    plt.legend(prop={'size': 14});
    ax1.tick_params(axis='y', labelsize=20)
    ax1.tick_params(axis='x', labelsize=16)
    
    calculateAndPlotOverbought(dataFr=dataFr, colName='%K', ax0=ax0, ax1=ax1, overbought_th=80)
    calculateAndPlotOversold(dataFr=dataFr, colName='%K', ax0=ax0, ax1=ax1, oversold_th=20)
            
    
    
# Compute and plot slow stochastic %K and %D
def computeAndPlotSlowStochasticOscillator(companyName='GOOG', n1=14, n2=3, start='2019-10-31', every_nth = 20):
    # Load dataframe for company
    dataFr = general.loadCompanyData(companyName, start=start)
    
    dataFr['fast_%K'] = STOK(dataFr, n1)
    # SMA
    dataFr['slow_%K'] = dataFr['fast_%K'].rolling(n2).mean()
    dataFr['slow_%D'] = dataFr['slow_%K'].rolling(n2).mean()
    
    fig = plt.figure(figsize=(20,15))
    # set height ratios for sublots
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1]) 

    # the fisrt subplot
    ax0 = plt.subplot(gs[0])
#     ax0.plot(dataFr['Date'].to_list(),
#                 dataFr['Close'].to_list(),
#                 label='Closing');
    highList = dataFr['high'].to_list()
    lowList = dataFr['low'].to_list()
    dateList = dataFr['Date'].to_list()
    closeList = dataFr['close'].to_list()
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
             dataFr['slow_%K'].to_list(),
             label='Slow %K',
             c='k');
    ax1.plot(dataFr['Date'].to_list(),
             dataFr['slow_%D'].to_list(),
             label='Slow %D',
             c='r');
    ax1.axhline(y=50, linestyle='-.')
    ax1.axhline(y=20, linestyle='-')
    ax1.axhline(y=80, linestyle='-')
    for n, label in enumerate(ax1.xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)
    plt.xticks(rotation=45, ha="right");
    plt.yticks([0, 20, 50, 80, 100])
    plt.legend(prop={'size': 14});
    ax1.tick_params(axis='y', labelsize=20)
    ax1.tick_params(axis='x', labelsize=16)
    
    calculateAndPlotOverbought(dataFr=dataFr, colName='slow_%K', ax0=ax0, ax1=ax1, overbought_th=80)
    calculateAndPlotOversold(dataFr=dataFr, colName='slow_%K', ax0=ax0, ax1=ax1, oversold_th=20)
   

# Compute and plot full stochastic %K and %D
def computeAndPlotFullStochasticOscillator(companyName='GOOG', n1=14, n2=3, n3=3, start='2019-10-31', every_nth = 20):
    # Load dataframe for company
    dataFr = general.loadCompanyData(companyName, start=start)
    
    dataFr['fast_%K'] = STOK(dataFr, n1)
    # SMA
    dataFr['full_%K'] = dataFr['fast_%K'].rolling(n2).mean()
    dataFr['full_%D'] = dataFr['full_%K'].rolling(n3).mean()
    
    fig = plt.figure(figsize=(20,15))
    # set height ratios for sublots
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1]) 

    # the fisrt subplot
    ax0 = plt.subplot(gs[0])
#     ax0.plot(dataFr['Date'].to_list(),
#                 dataFr['Close'].to_list(),
#                 label='Closing');
    highList = dataFr['high'].to_list()
    lowList = dataFr['low'].to_list()
    dateList = dataFr['Date'].to_list()
    closeList = dataFr['close'].to_list()
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
             dataFr['full_%K'].to_list(),
             label='Full %K',
             c='k');
    ax1.plot(dataFr['Date'].to_list(),
             dataFr['full_%D'].to_list(),
             label='Full %D',
             c='r');
    ax1.axhline(y=50, linestyle='-.')
    ax1.axhline(y=20, linestyle='-')
    ax1.axhline(y=80, linestyle='-')
    for n, label in enumerate(ax1.xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)
    plt.xticks(rotation=45, ha="right");
    plt.yticks([0, 20, 50, 80, 100])
    plt.legend(prop={'size': 14});
    ax1.tick_params(axis='y', labelsize=20)
    ax1.tick_params(axis='x', labelsize=16)
    
    calculateAndPlotOverbought(dataFr=dataFr, colName='full_%K', ax0=ax0, ax1=ax1, overbought_th=80)
    calculateAndPlotOversold(dataFr=dataFr, colName='full_%K', ax0=ax0, ax1=ax1, oversold_th=20)

