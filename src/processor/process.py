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

def execute_prompt(prompt, idx):
    openai_response = call_openai_api(prompt)
    print(openai_response)

    # Save the prompt to a file named code
    with open(f'./output/exp{idx}/code.py', 'w') as code:
        code.write(openai_response)
    
    return execute_python_code(openai_response)


def execute_continuously(prompt, idx):
    print(prompt)
    Path(f"./output/exp{idx}/").mkdir(parents=True, exist_ok=True)
    execution_result = execute_prompt(prompt, idx)
    while 'failed' in execution_result:
        print(execution_result)
        print('retrying')
        execution_result = execute_prompt(prompt, idx)
    
    return f'./output/exp{idx}/answer.png'


def execute(question:str, csv_files: List[str], uuid: str):
    n_lines = 2
    csv_path = csv_files[0]
    
    raw = read_csv_first_n_lines(csv_path, n_lines)
    file_length = get_file_num_lines(csv_path)

    printed_raw = ''.join(map(str, raw[:n_lines]))

    e2e_prompt = open("prompt_templates/e2e.prompt").read()
    prompt = e2e_prompt.format(n=n_lines, raw=printed_raw, row_count=file_length, csv_path=csv_path, question=question, idx=uuid)

    return execute_continuously(prompt, uuid)

if __name__ == '__main__':
    with shelve.open('localdb') as db:
        if 'file_count' not in db:
            db['file_count'] = 1
        idx = db['file_count']
        db['file_count'] += 1
    
    # Set up OpenAI API credentials
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    execute(
        question="What product is ordered most often?",
        csv_files=[
            './data/grocery/order_products__prior.csv'
        ],
        uuid=idx
    )