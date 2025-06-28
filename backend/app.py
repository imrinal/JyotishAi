# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS # Import CORS

app = Flask(__name__)
CORS(app) # This enables CORS for all origins and routes.
          # For production, you might want to specify allowed origins for security:
          # CORS(app, origins=["https://your-vercel-domain.vercel.app"])
          # (Replace 'your-vercel-domain.vercel.app' with your actual Vercel domain)

# ... rest of your Flask routes and logic ...
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

# Keep this for local development, Vercel will ignore it:
if __name__ == '__main__':
    app.run(debug=True)