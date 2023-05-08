from os import getenv
from pathlib import Path

import openai
from .pub_script import pub_path
from config.settings import BASE_DIR

from .files import read_file, write_file

def transform_prompt(text):
    openai.api_key = getenv("OPENAI_API_KEY")
    messages = [
        dict(role='system', content='You are an assistant'),
        dict(role='user', content=f'write a summary of this [content]\n\n{text}')
    ]
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, max_tokens=1000)
    return response['choices'][0]['message']['content']


def apply_prompt(out_file, prompt):
    text = transform_prompt(prompt)
    write_file(pub_path(out_file), text)


def create_prompt(**kwargs):
    context = kwargs.get('context')
    content = kwargs.get('content')
    task = kwargs.get('task')
    if task:
        text = read_file(pub_path(context))
        text += read_file(pub_path(content))
        text += read_file(pub_path(task))
        prompt = str(task)+'.ai'
        write_file(prompt, text)
        return text


def do_gpt_task(args):
    if not args[1:]:
        return 'usage: chat output task [content] [context]'
    if not args[2:]:
        prompt = create_prompt(task=args[1])
    elif not args[3:]:
        prompt = create_prompt(task=args[1], content=args[2])
    else:
        prompt = create_prompt(task=args[1], content=args[2], context=args[3])
    if prompt:
        apply_prompt(args[0], prompt)
    return f'Prompt: output={args[0]} task={args[1]} prompt={prompt} content,context={args[2:]}'

