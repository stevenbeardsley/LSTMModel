from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

# Serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to handle the prediction request
@app.route('/predict-price', methods=['POST'])
def predict_price():
    ticker = request.form.get('ticker')  # Get the stock ticker from the request

    # Run the RNN.py script and pass the ticker as an argument
    try:
        # Run RNN.py with ticker as an argument (this assumes RNN.py is set up to take a command-line argument)
        result = subprocess.run(['python', 'RNN.py', ticker], capture_output=True, text=True)

        # Check for errors
        if result.returncode != 0:
            return jsonify({"response": "Error running the RNN script."})

        # Get the price prediction from the script output
        predicted_price = result.stdout.strip()
        return jsonify({"response": f"The predicted price for {ticker} is: {predicted_price}"})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
