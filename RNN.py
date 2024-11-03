import numpy as np
import yfinance as yf 
import tensorflow as tf 
from tensorflow.keras import Sequential 
from tensorflow.keras.layers import LSTM, Dense
from sklearn.model_selection import train_test_split
import sys

#Get data 
def GetDataSet():
    #Task 1: Create a input for the website to allow for more stocks to be tested - maybe also add dates into the input list who knows 
    data = yf.download(tickers = 'AAPL', start='2010-01-11',end='2011-01-11')#Years worth of data 
    data['Target']  = data['Adj Close']- data.Open
    data['Target'] = data['Target'] .shift(-1)

    priceList=  data['Target']
    dateList  = data.index
    return priceList 
    
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
    #print ("The loss accuracy: ", loss)
    nextPrice = model.predict(sampleTest)
    #print ("The next price is: ",nextPrice[-1])
    return nextPrice[-1] 

def main():
    # Read command line arguments for ticker and date range
    ticker = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    start_date = sys.argv[2] if len(sys.argv) > 2 else "2010-01-11"
    end_date = sys.argv[3] if len(sys.argv) > 3 else "2011-01-11"
    
    sequenceLength = 10  
    priceList = GetDataSet()
    sampleList, targetList = FormatData(priceList, sequenceLength)
    price = run (sampleList, targetList, sequenceLength)
    
    return price

if __name__ == "__main__":
    prediction = main()
    print(prediction)  # Print the final prediction for Flask to capture

#Description- This project uses the Long Short Term Memory (LSTM) algorithm to weight short term fluctuations in changes in stock prices against long term trends.
# This model incorporates neural networks and machine learning to accurately use past data to predict future stock prices.
