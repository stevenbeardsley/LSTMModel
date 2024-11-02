import numpy as np
import yfinance as yf
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.model_selection import train_test_split
import sys

# Get data with dynamic ticker and date range
def GetDataSet(ticker, start_date, end_date):
    data = yf.download(tickers=ticker, start=start_date, end=end_date)
    data['Target'] = data['Adj Close'] - data['Open']
    data['Target'] = data['Target'].shift(-1)
    priceList = data['Target'].dropna()  # Drop NaNs after shifting
    return priceList

# Format data into sequences and targets for LSTM
def FormatData(data, sequenceLength):
    data = data.to_frame()
    data.columns = ['Target']
    data["Target"] = (data["Target"] - data["Target"].min()) / (data["Target"].max() - data["Target"].min())
    priceList = list(data['Target'])
    
    sampleList, targetList = [], []
    for x in range(len(priceList) - sequenceLength):
        sampleList.append(priceList[x:x+sequenceLength])
        targetList.append(priceList[x+sequenceLength])
    
    sampleList = np.array(sampleList)
    targetList = np.array(targetList)
    return sampleList, targetList

# Run the LSTM model
def run(sampleList, targetList, sequenceLength):
    sampleList = np.reshape(sampleList, (sampleList.shape[0], sampleList.shape[1], 1))
    sampleTrain, sampleTest, targetTrain, targetTest = train_test_split(sampleList, targetList, test_size=0.2, random_state=42)
    
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(sequenceLength, 1)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    
    model.fit(sampleTrain, targetTrain, epochs=10, batch_size=1, verbose=1)
    
    loss = model.evaluate(sampleTest, targetTest)
    print("The loss accuracy:", loss)
    
    nextPrice = model.predict(sampleTest)
    print("The next price is:", nextPrice[-1])
    return nextPrice[-1][0]  # Return the last prediction value

def main():
    # Read command line arguments for ticker and date range
    ticker = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    start_date = sys.argv[2] if len(sys.argv) > 2 else "2010-01-11"
    end_date = sys.argv[3] if len(sys.argv) > 3 else "2011-01-11"
    
    sequenceLength = 10
    priceList = GetDataSet(ticker, start_date, end_date)
    sampleList, targetList = FormatData(priceList, sequenceLength)
    price = run(sampleList, targetList, sequenceLength)
    
    return price

if __name__ == "__main__":
    prediction = main()
    print(prediction)  # Print the final prediction for Flask to capture
