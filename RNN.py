import numpy as np
import yfinance as yf 
import tensorflow as tf 
from tensorflow.keras import Sequential 
from tensorflow.keras.layers import LSTM, Dense
from sklearn.model_selection import train_test_split

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

def run(sampleList, targetList, sequenceLength):
    #Shape the sampleList to fit the LSTM layer in the neural 
    # Before reshaping: 2D array consisting of  (number_of_samples, sequence_length)
    #After shaping: 3D array (samples, time_steps, features)
    sampleList = np.reshape(sampleList, (sampleList.shape[0], sampleList.shape[1],1))

    #Split the data 
    sampleTrain, sampleTest, targetTrain, targetTest = train_test_split(sampleList, targetList, test_size=0.2,random_state=42)

    #Build the model
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(sequenceLength,1)))
    model.add(Dense(1))

    #Compile the model
    model.compile(optimizer='adam', loss='mean_squared_error')

    #Train the model with our data 
    model.fit(sampleTrain, targetTrain, epochs=100, batch_size=1, verbose=1 )

    #Create loss function - Tracks the difference between the predicted and the actual value (ground truth)
    loss = model.evaluate(sampleTest, targetTest)
    print ("The loss accuracy: ", loss)
    nextPrice = model.predict(sampleTest)
    print ("The next price is: ",nextPrice[-1])
    #217


def main():
    sequenceLength = 10 #Yet to be optimised 
    priceList = GetDataSet()
    sampleList, targetList = FormatData(priceList, sequenceLength)
    run (sampleList, targetList, sequenceLength)

main()
#Description- This project uses the Long Short Term Memory (LSTM) algorithm to weight short term fluctuations in changes in stock prices against long term trends. This model incorporates neural networks and machine learning to accurately use past data to predict future stock prices.
#Next steps
# 1. Link up this code with the website 