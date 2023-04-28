import os
from pathlib import Path

# import dotenv
import openai

from .files import read_file, write_file

# if Path('config/.env').exists():
#     dotenv.read_dotenv('config/.env')

#     # Load your API key from an environment variable or secret management service
#     openai.api_key = os.getenv("OPENAI_API_KEY")

openai.api_key = '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'
# print(openai.Model.list())

def transform_prompt(text):
    messages = [
        dict(role='system', content='You are an assistant'),
        dict(role='user', content=f'write summary of this [content]\n\n{text}')
    ]
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, max_tokens=50)
    print(response['choices'][0]['message']['content'])
    # return response['choices'][0]

def ghost_prompt(request, response):
    # print(f'Request {request}, Response: {response}')
    text = read_file(request)
    text = transform_prompt(text)

    # write_file(response, text)
    # print(text)
