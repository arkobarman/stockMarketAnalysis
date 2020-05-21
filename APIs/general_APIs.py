import os
import pandas as pd

def loadCompanyData(companyName='GOOG'):
    filepath = os.path.join('data', '{}.csv'.format(companyName))
    
    if not os.path.exists(filepath):
        raise ValueError('Data for companyName = {} does not exist!!!'.format(companyName))
        
    dataFr = pd.read_csv(filepath)
    
    return dataFr