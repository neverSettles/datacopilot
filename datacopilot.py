import openai
import os
from typing import List
import csv
from dotenv import load_dotenv
import shelve
from pathlib import Path

load_dotenv()
# Set up your OpenAI API credentials
key = os.getenv("OPENAI_API_KEY")
openai.api_key = key

def call_openai_api(prompt):
    # Define the parameters for the completion
    params = {
        'model': 'text-davinci-003',  # The model you want to use
        'prompt': prompt,
        'max_tokens': 3000  # The maximum number of tokens to generate
    }

    # Call the OpenAI API
    response = openai.Completion.create(**params)

    # Retrieve the generated text from the API response
    generated_text = response.choices[0].text.strip()

    return generated_text

def execute_python_code(code):
    try:
        exec(code)
        return "Execution successful"
    except Exception as e:
        return f"Execution failed: {str(e)}"

def read_csv_file(filename):
    data = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return data

def get_file_num_lines(file_path: str) -> int:
    with open(file_path, "rb") as f:
        num_lines = sum(1 for _ in f)
    return num_lines

def read_csv_first_n_lines(file_path: str, n: int) -> List[str]:
    lines: List[str] = []
    with open(file_path, 'r') as csv_file:
        for line in range(n):
            lines.append(csv_file.readline())
    return lines

# Example usage
csv_path = './data/instacart/order_products__prior.csv'
n_lines = 5
raw = read_csv_first_n_lines(csv_path, n_lines)
file_length = get_file_num_lines(csv_path)

with shelve.open('localdb') as db:
    if 'file_count' not in db:
        db['file_count'] = 1
    idx = db['file_count']
printed_raw = ''.join(map(str, raw[:n_lines]))

question = "What product is ordered most often?"

def execute_prompt(prompt):
    openai_response = call_openai_api(prompt)
    print(openai_response)

    # Save the prompt to a file named code
    with open(f'./output/exp{idx}/code.py', 'w') as code:
        code.write(openai_response)
    
    return execute_python_code(openai_response)


def execute_continuously(prompt):
    print(prompt)
    Path(f"./output/exp{idx}/").mkdir(parents=True, exist_ok=True)

    

    execution_result = execute_prompt(prompt)
    while 'failed' in execution_result:
        print(execution_result)
        print('retrying')
        execution_result = execute_prompt(prompt)

iterations = 2
for i in range(iterations):
    with shelve.open('localdb') as db:
        idx = db['file_count']
        db['file_count'] += 1
    prompt = """
The first {n} rows of my data look like:
START_DATA
{raw}
END_DATA
There are {row_count} rows in the csv in total. So take that into consideration when plotting any images.

The data is stored in '{csv_path}'

You are Jeff Dean. 
Write some python code with pandas to transform the data such that it answers the following question:
{question}
After the transformation of the data is done,
The code should create the most relelvant matplotlib plot and save it to a file in the folder './output/exp{idx}/'.
Make sure the python code is always correct and runnable. Make sure the code is efficient.
The code should import all necessary libraries.
    """.format(n=n_lines, raw=printed_raw, row_count=file_length, csv_path=csv_path, question=question, idx=idx)

    execute_continuously(prompt)
