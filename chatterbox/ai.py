from os import getenv
from pathlib import Path

import openai
from publish.pub import pub_path
from config.settings import BASE_DIR

from publish.files import read_file, write_file


def transform_prompt(prompt):
    openai.api_key = getenv("OPENAI_API_KEY")
    messages = [
        dict(role='user', content=prompt)
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages, max_tokens=1000)
    return response['choices'][0]['message']['content']


def apply_prompt(outfile, prompt):
    text = transform_prompt(prompt)
    write_file(outfile, text)


def create_prompt(**kwargs):
    prompt = ''

    context = kwargs.get('context')
    if context:
        prompt += read_file(pub_path(context))

    content = kwargs.get('content')
    if content:
        prompt += read_file(pub_path(content))

    task = kwargs.get('task')
    if task:
        prompt += read_file(pub_path(task))
        return prompt


def save_prompt(**kwargs):
    ai = kwargs.get('ai')
    if not Path(ai).exists():
        prompt = create_prompt(**kwargs)
        assert(prompt)
        write_file(ai, prompt)
        assert(Path(ai).exists())


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

def pub_ai(**kwargs):
    pub = kwargs.get('pub')
    chapter = kwargs.get('chapter')
    doc = kwargs.get('doc')
    path = pub_path(pub, chapter, doc)
    path2 = str(path).replace('.md','.ai')
    # editor = getenv("EDITOR")
    # system(f'{editor} {path} {path2}')
    print(f'chatgpt: {path} {path2}')
    url = f'/{pub}/{chapter}/{doc}'
    return url
