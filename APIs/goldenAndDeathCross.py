import pandas as pd
import matplotlib.pyplot as plt
from APIs import general_APIs as general

plt.style.use('seaborn-darkgrid')

def getMovingAverage(dataFr, colName='Close', nDays=50):
    dataFr['movingAverage_{}'.format(nDays)] = dataFr[colName].rolling(nDays).mean()
    
    return dataFr

def analyzeGoldenAndDeathCross(companyName='GOOG', 
                               nDays_short=50, 
                               nDays_long=200, 
                               start='2019-10-31', 
                               every_nth = 20):
    # Load dataframe for company
    dataFr = general.loadCompanyData(companyName, start=start)
    
    # Create moving average columns
    dataFr = getMovingAverage(dataFr, colName='Close', nDays=nDays_short)
    dataFr = getMovingAverage(dataFr, colName='Close', nDays=nDays_long)
    
    fig = plt.figure(figsize=(20,10))
    ax = fig.add_subplot(111)
    ax.plot(dataFr['Date'].to_list(),
            dataFr['Close'].to_list(),
            label='Closing');
    ax.plot(dataFr['Date'].to_list(),
            dataFr['movingAverage_{}'.format(nDays_short)].to_list(),
            label='{}-day SMA'.format(nDays_short),
            linewidth=3);
    ax.plot(dataFr['Date'].to_list(),
            dataFr['movingAverage_{}'.format(nDays_long)].to_list(),
            label='{}-day SMA'.format(nDays_long),
            linewidth=3);
    plt.xticks(rotation=45, ha="right");
    for n, label in enumerate(ax.xaxis.get_ticklabels()):
        if n % every_nth != 0:
            label.set_visible(False)
    plt.legend(prop={'size': 20})
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=16)