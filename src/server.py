from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"Choo Choo": "Navigate to /suggest to get outputs! 🚅"})

@app.route('/suggest')
def suggest():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.getenv("PORT", default=5000))