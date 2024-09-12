from flask import Flask, render_template, request, jsonify

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
    ticker = request.form['ticker'].upper()
    prediction = stock_predictions.get(ticker, "No prediction available for the entered stock ticker.")
    return jsonify(prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
