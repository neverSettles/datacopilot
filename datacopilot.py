import openai
import os
from typing import List
import langchain
import csv

# Set up your OpenAI API credentials
key = os.getenv("OPENAI_API_KEY")
openai.api_key = key

def call_openai_api(system_prompt, user_prompt):
    # Define the parameters for the completion

    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    max_tokens=3000,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ])

    # Retrieve the generated text from the API response
    generated_text = response.choices[0].message.content.strip()

    return generated_text

def execute_python_code(code):
    try:
        exec(code)
        return "Execution successful"
    except Exception as e:
        return f"Execution failed: {str(e)}"


def read_csv_first_n_lines(file_path: str, n: int) -> List[str]:
    lines: List[str] = []
    with open(file_path, 'r') as csv_file:
        for line in range(n):
            lines.append(csv_file.readline())
    return lines

# Example usage
csv_path = 'data/chats.csv'
n_lines = 10
raw = read_csv_first_n_lines(csv_path, n_lines)

question = "Who are the most active users"

sys_prompt = """
My data looks like this:
{raw}

Write some python code with pandas to transform the data such that it answers the user's question.
The code should create the file if the file does not exist.
Make it only output runnable python code.
The code should create the file in the './output/' folder.
Give me only pyton code and nothing else. I will run the output of what you reply.
""".format(raw=str(raw))

user_prompt = """
My question is:
{question}
""".format(question=question)

print(sys_prompt,user_prompt,'\n')
openai_response = call_openai_api(sys_prompt, user_prompt)
print(openai_response)

# Example usage
execution_result = execute_python_code(openai_response)
print(execution_result)
