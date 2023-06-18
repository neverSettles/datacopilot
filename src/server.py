import openai
import os


from flask import Flask, jsonify
from dotenv import load_dotenv

from processor import process


# Set up your OpenAI API credentials
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"Choo Choo": "Navigate to /suggest to get outputs! 🚅"})

@app.route('/suggest')
def suggest():
    process.execute()
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.getenv("PORT", default=5000))
