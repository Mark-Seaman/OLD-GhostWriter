import os
from pathlib import Path

import dotenv
import openai
from config.settings import BASE_DIR

from .files import read_file, write_file

def transform_prompt(text):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    messages = [
        dict(role='system', content='You are an assistant'),
        dict(role='user', content=f'write a summary of this [content]\n\n{text}')
    ]
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, max_tokens=250)
    return response['choices'][0]['message']['content']

def ghost_prompt(in_file, out_file):
    # d = '/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/SoftwareEngineering/AI'
    text = read_file(in_file)
    text = transform_prompt(text)
    print(text)
    write_file(out_file, text)
