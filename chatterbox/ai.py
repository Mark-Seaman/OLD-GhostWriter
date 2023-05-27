from os import getenv
from pathlib import Path

import json
import openai

from publish.pub import pub_path
from config.settings import BASE_DIR

from publish.files import read_file, write_file
from publish.text import text_join


def transform_prompt(prompt):
    openai.api_key = getenv("OPENAI_API_KEY")

    conversation = [
        dict(role='user', content=prompt)
    ]

    while True:

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=conversation, 
            max_tokens=1000)
    
        message = response['choices'][0]['message']['content']
        conversation.append({"role": "assistant", "content": message})

        finish_reason = response['choices'][0]['finish_reason']
        if finish_reason != 'length':
            return ''.join([m['content'] for m in conversation if m['role']=='assistant'])
            # return json.dumps(conversation, indent=4)
    
    # return response['choices'][0]['message']['content']

    # return str(response['choices'])

    # conversation = [
    #     {"role": "system", "content": "You are a helpful assistant."},
    #     {"role": "user", "content": prompt}
    # ]

    # while True:
    #     response = openai.Completion.create(
    #         model="gpt-3.5-turbo",  # as of my knowledge cutoff in 2021, GPT-3.5 isn't available yet
    #         messages=conversation,
    #         max_tokens=100,
    #         temperature=0.5,
    #         top_p=1
    #     )
    #     message = response['choices'][0]['message']['content']

    #     if message.endswith('[continue]'):
    #         conversation.append({"role": "assistant", "content": message.replace('[continue]', '')})
    #     else:
    #         conversation.append({"role": "assistant", "content": message})
    #         break

    # return json.dumps(conversation, indent=4)


def update_with_ai(doc_file):
    prompt_file = str(doc_file).replace('.md','.ai')
    prompt = read_file(prompt_file)
    text = f'# {doc_file.name}\n\n' + transform_prompt(prompt)
    write_file(doc_file, text)

import openai

# def get_local_weather_report(location):
#     # Set up OpenAI API credentials
#     openai.api_key = 'YOUR_API_KEY'

#     # Create a prompt for the weather report
#     prompt = f"What's the weather like in {location} today?"

#     # Set the desired maximum tokens for the API response
#     max_tokens = 50

#     # Initialize the conversation
#     conversation = []

#     while True:
#         # Generate the API response
#         response = openai.Completion.create(
#             engine='davinci-codex',
#             prompt=prompt,
#             max_tokens=max_tokens,
#             temperature=0.7,
#             n=1,
#             stop=None,
#             context=conversation
#         )

#         # Extract the weather report from the API response
#         weather_report = response.choices[0].text.strip()

#         # Print the weather report
#         print(weather_report)

#         # Check if the response ends due to length
#         if response.choices[0].finish_reason == 'length':
#             break

#         # Extend the conversation with the API response
#         conversation.extend(response.choices[0].text.strip().split('\n'))

#         # Continue the prompt for the next iteration
#         prompt = ''

#     print("Weather report complete.")

# # Example usage
# get_local_weather_report("New York")

# def create_prompt(**kwargs):
#     prompt = ''
#     context = kwargs.get('context')
#     if context:
#         prompt += read_file(pub_path(context))
#     content = kwargs.get('content')
#     if content:
#         prompt += read_file(pub_path(content))
#     task = kwargs.get('task')
#     if task:
#         prompt += read_file(pub_path(task))
#         return prompt


# def save_prompt(**kwargs):
#     ai = kwargs.get('ai')
#     if not Path(ai).exists():
#         prompt = create_prompt(**kwargs)
#         assert(prompt)
#         write_file(ai, prompt)
#         assert(Path(ai).exists())


# def do_gpt_task(args):
#     if not args[1:]:
#         return 'usage: chat output task [content] [context]'
#     if not args[2:]:
#         prompt = create_prompt(task=args[1])
#     elif not args[3:]:
#         prompt = create_prompt(task=args[1], content=args[2])
#     else:
#         prompt = create_prompt(task=args[1], content=args[2], context=args[3])
#     if prompt:
#         apply_prompt(args[0], prompt)
#     return f'Prompt: output={args[0]} task={args[1]} prompt={prompt} content,context={args[2:]}'

def pub_ai(**kwargs):
    pub = kwargs.get('pub')
    chapter = kwargs.get('chapter')
    doc = kwargs.get('doc')
    doc_file = pub_path(pub, chapter, doc)
    update_with_ai(doc_file)

    # prompt_file = str(doc_file).replace('.md','.ai')
    # prompt = read_file(prompt_file)
    # print(f'chatgpt: {doc_file} {prompt}')
    # apply_prompt(doc_file, prompt)

    url = f'/{pub}/{chapter}/{doc}'
    return url
