import openai
import os
from typing import List
import csv
from dotenv import load_dotenv

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

def read_csv_first_n_lines(file_path: str, n: int) -> List[str]:
    lines: List[str] = []
    with open(file_path, 'r') as csv_file:
        for line in range(n):
            lines.append(csv_file.readline())
    return lines

# Example usage
csv_path = 'data/chats.csv'
n_lines = 10
raw = read_csv_file(csv_path)


printed_raw = '\n'.join(map(str, raw[:5]))

question = "Who are the most active users"

prompt = """
The first {n} rows of my data look like:
START_DATA
{raw}
END_DATA
There are {row_count} rows in the csv in total. So take that into consideration when plotting any images.

The data is stored in {csv_path}

You are Jeff Dean. 
Write some python code with pandas to transform the data such that it answers the following question:
{question}
After the transformation of the data is done, the code should create the most relelvant matplotlib plot and save it to a file in output/imgs2/
The code should create an output csv file if the file does not exist.
Make sure the python code is always correct and runnable. Make sure the code is efficient.
The code should create the file in the './output/' folder.
The code should import all necessary libraries.
""".format(n=n_lines, raw=printed_raw, row_count=len(raw), csv_path=csv_path, question=question)

def execute_continuously(prompt):
    print(prompt)
    openai_response = call_openai_api(prompt)
    print(openai_response)
    execution_result = execute_python_code(openai_response)
    while 'failed' in execution_result:
        print(execution_result)
        print('retrying')
        openai_response = call_openai_api(prompt)
        print(openai_response)
        execution_result = execute_python_code(openai_response)


execute_continuously(prompt)
execute_continuously(prompt)
execute_continuously(prompt)
execute_continuously(prompt)
execute_continuously(prompt)
