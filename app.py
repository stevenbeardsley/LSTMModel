from flask import Flask, render_template, request, jsonify
import RNN
#Flask operates as a very simple server to run the code on basically 
app = Flask(__name__)

# Sample stock prediction logic
stock_predictions = {
    "AAPL": "The stock is expected to rise by 5% in the next quarter.",
    "TSLA": "The stock may face a decline of 3% in the coming month.",
    "AMZN": "A steady growth of 2% is predicted over the next half-year."
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    ticker = request.form['ticker'].upper() #The stock symbol is already read so should be easy to parse it 
    prediction = stock_predictions.get(ticker, "No prediction available for the entered stock ticker.")
    newPrediction = RNN.main()
    return jsonify({'price' : newPrediction})

if __name__ == '__main__':
    app.run(debug=True)
