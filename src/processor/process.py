import openai
from typing import List
import shelve
import os
from pathlib import Path
from dotenv import load_dotenv
import matplotlib
matplotlib.use('Agg')

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

# Currently the output of this is this: (Which sucks) - why is it the case?
# Please, provide the Python code to accomplish the above tasks.
# # 1. Import all necessary libraries
# import pandas as pd
# import numpy as np
# from sklearn.preprocessing import StandardScaler, OneHotEncoder
# from sklearn.feature_selection import SelectKBest, chi2

# # 2. Load the datasets into dataframes
# order_products_prior = pd.read_csv('./data/grocery/order_products__prior.csv')
# orders = pd.read_csv('./data/grocery/orders.csv')
# products = pd.read_csv('./data/grocery/products.csv')

# def call_openai_api(prompt):
#     response = openai.ChatCompletion.create(
#         model='gpt-4',
#         messages=[{"role":"system", "content":str(prompt)}],
#         max_tokens=100,
#         temperature=0.7,
#         n=1,
#         stop=None,
#     )
#     completion = response.choices[0].message.content.strip()
#     all_but_first = completion.split('\n')[1:]
#     return '\n'.join(all_but_first)

def execute_python_code(code):
    try:
        exec(code)
        return "Execution successful"
    except Exception as e:
        return f"Execution failed: {str(e)}"

def get_file_num_lines(file_path: str) -> int:
    with open(file_path, "rb") as f:
        num_lines = sum(1 for _ in f)
    return num_lines

def read_csv_first_n_lines(file_path: str, n: int) -> List[str]:
    lines: List[str] = []
    with open(file_path, 'r') as csv_file:
        for _ in range(n):
            lines.append(csv_file.readline())
    return lines

def execute_prompt(prompt, initial_code, idx):
    openai_response = call_openai_api(prompt)
    print(openai_response)

    # Save the prompt to a file named code
    with open(f'./output/exp{idx}/code.py', 'w') as code:
        code.write(openai_response)
    
    return execute_python_code(initial_code + openai_response)


def execute_continuously(prompt, initial_code, idx):
    print(prompt)
    Path(f"./output/exp{idx}/").mkdir(parents=True, exist_ok=True)
    execution_result = execute_prompt(prompt, initial_code, idx)
    while 'failed' in execution_result:
        print(execution_result)
        print('retrying')
        execution_result = execute_prompt(prompt, initial_code, idx)
    
    return f'./output/exp{idx}/answer.png'


def execute(question:str, csv_files: List[str], uuid: str):
    n_lines = 2
    csv_path = csv_files[0]
    
    raw = read_csv_first_n_lines(csv_path, n_lines)
    file_length = get_file_num_lines(csv_path)

    printed_raw = ''.join(map(str, raw[:n_lines]))

    e2e_prompt = open("prompt_templates/e2e.prompt").read()
    prompt = e2e_prompt.format(n=n_lines, raw=printed_raw, row_count=file_length, csv_path=csv_path, question=question, idx=uuid)

    return execute_continuously(prompt, '', uuid)

def execute_mutliple(question:str, uuid: str, csv_files: List[str]):
    files_prompt_template = open("prompt_templates/pandas_transform/files.prompt").read()
    mutli_prompt_template = open("prompt_templates/pandas_transform/main.prompt").read()
    base_python_template = open("prompt_templates/pandas_transform/pandas_transform.prompt").read()

    files_prompt = ''

    for csv_file in csv_files:
        files_prompt += files_prompt_template.format(
            file_name=csv_file,
            n_rows=get_file_num_lines(csv_file),
            first_two_rows=''.join(map(str, read_csv_first_n_lines(csv_file, 2)))
        ) + '\n'
        

    multi_prompt = mutli_prompt_template.format(
        file_count=len(csv_files), 
        files_prompt=files_prompt, 
        question=question, 
        idx=uuid
    )

    return execute_continuously(multi_prompt, '', uuid)

def process_only_run():
    with shelve.open('localdb') as db:
            if 'file_count' not in db:
                db['file_count'] = 1
            idx = db['file_count']
            db['file_count'] += 1
        
        # Set up OpenAI API credentials
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
        
    execute_mutliple(
        question="How can we predict what the next item a user will order will be?",
        csv_files=[
            # './data/churn_modeling/Churn_Modelling.csv'
            # './data/itchurn/IT_customer_churn.csv'
            './data/grocery/order_products__prior.csv',
            './data/grocery/orders.csv',
            # './data/grocery/aisles.csv',
            './data/grocery/products.csv',
            # './data/grocery/departments.csv',
            # './data/grocery/order_products__train.csv'
        ],
        uuid=idx
    )

if __name__ == '__main__':
    for _ in range(5):
        process_only_run()