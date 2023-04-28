import os
from pathlib import Path

import dotenv
import openai
from config.settings import BASE_DIR

from .files import read_file, write_file

path = Path(BASE_DIR)/'config/.env'
if path.exists():
    dotenv.read_dotenv(path)
    openai.api_key = os.getenv("OPENAI_API_KEY")
    print(os.getenv("OPENAI_API_KEY"))
else:
    print('BAD CONFIG')


def transform_prompt(text):
    messages = [
        dict(role='system', content='You are an assistant'),
        dict(role='user', content=f'write summary of this [content]\n\n{text}')
    ]
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, max_tokens=50)
    print(response['choices'][0]['message']['content'])

def ghost_prompt(in_file, out_file):
    d = '/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/SoftwareEngineering/AI'
    in_file = f'{d}/Milestones.md'
    out_file = f'{d}/Response.md'
    print(f'Request {in_file}, Response: {out_file}')
    text = read_file(in_file)
    text = transform_prompt(text)
    write_file(out_file, text)
