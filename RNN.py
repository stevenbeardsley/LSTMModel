import tensorflow as tf 
import numpy as np
from tensorflow.keras import Sequential 
from tensorflow.keras.layers import Dense
import yfinance as yf 

#Get data 
def GetDataSet():
    data = yf.download(tickers = 'AAPL', start='2010-01-11',end='2011-01-11')#Years worth of data 

    #Predict day number 9
    data['Target']  = data['Adj Close']- data.Open
    data['Target'] = data['Target'] .shift(-1)

    #Create CNN
    priceList=  data['Target']
    dateList  = data.index
    return priceList 
   #Error is that in getdataset there isn't a header called Target.
    
#This Function is to take 5 days worth of reference price, and the next day (target) and return them 
def FormatData(data, sequenceLength):
    data = data.to_frame()
    data.columns = ['Target'] + list(data.columns[1:])
    data["Target"] = (data["Target"] - data["Target"].min())/(data["Target"].max() - data["Target"].min())
    priceList = list(data['Target'])
    sampleList, targetList = [],[]
    for x in range (len(priceList) - sequenceLength):
        sampleList.append(priceList[x:x+sequenceLength])
        targetList.append(x+sequenceLength)
    sampleList = np.array(sampleList)
    targetList = np.array(targetList)
    return sampleList, targetList

def CalculateTarget(data, target):
    targetGuess = 0

    return targetGuess

def main():
    sequenceLength = 10
    priceList = GetDataSet()
    sampleList, targetList = FormatData(priceList, sequenceLength)
    
main()
#Description- This project uses the Long Short Term Memory (LSTM) algorithm to weight short term fluctuations in changes in stock prices against long term trends. This model incorporates neural networks and machine learning to accurately use past data to predict future stock prices.
