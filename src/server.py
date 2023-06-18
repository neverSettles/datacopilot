import openai
import os
import json

from flask import Flask, jsonify, request
from dotenv import load_dotenv

from processor import process
from s3 import handler


# Set up your OpenAI API credentials
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"Choo Choo": "Navigate to /suggest to get outputs! 🚅"})

@app.route('/suggest', methods=['POST'])
def suggest():
    content_type = request.headers.get('Content-Type')
    if (content_type != 'application/json'):
        return 'Content-Type not supported!'

    body = json.loads(request.json)
    # body = {
    #     'objective': 'What are the best colors?',
    #     'requestId': '12345'
    # }

    # get all csv files from aws, save them locally.
    csv_files = handler.download_csvs_from_s3(body.requestId)

    # execute
    process.execute(body.objective, csv_files, body.requestId)
    return jsonify({f"Choo Choo": "Hello krishna {body}".format(body=body)})



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.getenv("PORT", default=5000))
