# Instructions

Run the following:

## Setup API key
Create a file named `.env` in the root of this repository 

On the first line, put: 

```OPENAI_API_KEY=YOURKEYHERE```

save the file.

## Setup virtual environment

```
python3 -m venv copilotenv
source copilotenv/bin/activate
pip install -r requirements.txt
```

Download the kaggle dataset:
https://www.kaggle.com/datasets/yasserh/instacart-online-grocery-basket-analysis-dataset
and unzip the files into the './data/instacart/' directory.

## Run the code
```
python datacopilot.py
```
