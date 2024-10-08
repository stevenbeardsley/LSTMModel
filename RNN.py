import tensorflow as tf 
from tensorflow.keras import Sequential 
from tensorflow.keras.layers import Dense
import yfinance as yf 

#Get data 
def GetDataSet():
    data = yf.download(tickers = 'AAPL', start='2010-01-11',end='2011-01-11')#Years worth of data 

    #Predict day number 9
    data['Target']  = data['Adj Close']- data.Open
    data['Target'] = data['Target'] .shift(-1)

    print ("This is the data ")
    print (data)
    #Create CNN
    print ("this is each bit in 5 days:")
    priceList=  data['Adj Close']
    dateList  = data.index
    
#This Function is to take 5 days worth of reference price, and the next day (target) and return them 
def FormatData(dataset):
    data["Target"] = (data["Target"] - data["Target"].min())/(data["Target"].max() - data["Target"].min())
    price_list = list(data['Target'])
    print(price_list[0])
    print(data["Target"])
    prices = []
    for date in dataset["Target"]:
        prices.append(date)
    #** With this list iterate over it picking five elements and a 'target element'and put it into another function called Calculate****

def CalculateTarget(data, target):
    targetGuess = 0

    return targetGuess
def main():
    GetDataSet()
    FormatData()#Return the list of 5 and the target, assigned to two variables data, target
    ##Add a function call to calculate target with the 5 days of data list and target 


#Description- This project uses the Long Short Term Memory (LSTM) algorithm to weight short term fluctuations in changes in stock prices against long term trends. This model incorporates neural networks and machine learning to accurately use past data to predict future stock prices.
