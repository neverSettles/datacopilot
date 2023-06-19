import openai
import os

from flask import Flask, jsonify, request
from dotenv import load_dotenv

from processor import process
from s3 import s3handler


# Set up OpenAI API credentials
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"Choo Choo": "Make a post request to /suggest to get output 🚅"})

@app.route('/suggest', methods=['POST'])
def suggest():
    content_type = request.headers.get('Content-Type')
    if (content_type != 'application/json'):
        return 'Content-Type not supported!'

    print(request.json)
    body = request.json
    uuid = body['requestId']
    objective = body['objective']

    # get all csv files from aws, save them locally.
    csv_files = s3handler.download_csvs_from_s3(uuid, './downloaded/')

    # execute
    image_filename = process.execute(question=objective, csv_files=csv_files, uuid=uuid)
    upload_suceeded, s3_path = s3handler.upload_file_to_s3(uuid=uuid, local_filepath=image_filename)
    if not upload_suceeded:
        return "", 404
    return jsonify({'image_s3_path': s3_path}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.getenv("PORT", default=5000))
