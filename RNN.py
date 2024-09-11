import tensorflow as tf 
from tensorflow.keras import Sequential 
from tensorflow.keras.layers import Dense
import yfinance as yf 
import matt
#Get data 
data = yf.download(tickers = 'AAPL', start='2010-01-11',end='2011-01-11')#Years worth of data 
print (data)
#Predict day number 9
data['Target']  = data['Adj Close']- data.Open
data['Target'] = data['Target'] .shift(-1)

print ()
print (data)
#Create CNN

print ()
priceList=  data['Adj Close']
dateList  = data.index
