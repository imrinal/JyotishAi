from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend to call backend

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    # Later: process birth details, calculate astrology, get predictions.
    print("[DEBUG] Received data:", data)
    return jsonify({"status": "success", "message": "Prediction will go here!"})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    # Later: process follow-up questions with AI model.
    print("[DEBUG] Chat message:", data)
    return jsonify({"status": "success", "message": "Chat response will go here!"})

if __name__ == '__main__':
    app.run(debug=True)
