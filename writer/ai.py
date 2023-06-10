from os import getenv
from pathlib import Path

import openai

from publish.files import read_file, write_file
from publish.text import include_files


def transform_prompt(prompt):
    openai.api_key = getenv("OPENAI_API_KEY")

    conversation = [
        dict(role='user', content=prompt)
    ]

    # Try up to ten times to transfer
    for i in range(10):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation,
            max_tokens=1000)

        message = response['choices'][0]['message']['content']
        conversation.append({"role": "assistant", "content": message})

        finish_reason = response['choices'][0]['finish_reason']
        if finish_reason != 'length':
            return ''.join([m['content'] for m in conversation if m['role'] == 'assistant'])

    # Return the failed conversation
    return ''.join([m['content'] for m in conversation if m['role'] == 'assistant'])


def update_with_ai(doc_file):
    prompt_file = str(doc_file).replace('.md', '.ai')
    prompt = include_files(read_file(prompt_file), doc_file.parent)
    text = f'# {doc_file.name}\n\n' + transform_prompt(prompt)
    # text = f'# {doc_file.name}\n\n' + prompt
    write_file(doc_file, text)


def pub_ai(**kwargs):
    pub = kwargs.get('pub')
    chapter = kwargs.get('chapter')
    doc = kwargs.get('doc')
    doc_file = pub_path(pub, chapter, doc)
    update_with_ai(doc_file)

    url = f'/{pub}/{chapter}/{doc}'
    return url
