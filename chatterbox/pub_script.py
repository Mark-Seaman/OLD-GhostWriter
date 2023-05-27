from os import getenv, system
from pathlib import Path
from re import match

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from chatterbox.ai import apply_prompt, do_gpt_task
from publish.files import copy_files, read_file, recursive_files
from publish.pub import pub_path
from publish.text import include_files, text_join, text_lines

'''
Writer Script

Examples:
- project SoftwareEngineering
- chapter SoftwareEngineering 08
- gpt  SoftwareEngineering 08 Outline.md
- publish SoftwareEngineering 08
- edit SoftwareEngineering 08

'''


def chapter_script(args):
    # Function to handle "chapter" command
    # ...
    if not args[1:]:
        return 'usage: chapter pub-name chapter-name'
    pub, chapter = args
    chapter_path = pub_path(pub, chapter)
    chapter_path.mkdir(parents=True, exist_ok=True)
    copy_files(pub_path(pub, 'Storyboard'), chapter_path)
    return chapter_path


def chatgpt_script(args):
    if args[2:]:
        out_file = pub_path(args[0], args[1], args[2])
        task = str(out_file).replace('.md', '.ai')
        prompt = read_file(task)
        prompt = include_files(prompt, out_file.parent)
        # print(prompt)
        apply_prompt(out_file, prompt)
        edit_script(['edit'] + args)
        return f'created {out_file}'
    else:
        return 'usage: pub gpt GhostWriter Chapter1 Outline.md'


def create_outline(args):
    path = pub_path(args[0], args[1], args[2])
    text = markdown_to_outline(path.read_text())
    if args[3:]:
        text = extract_outline(text, args[3])
    return text


def edit_script(args):
    # Function to handle "edit" command
    # ...
    if not args:
        return 'usage: pub-name chapter-name'
    path = pub_path(args[0], args[1])
    editor = getenv("EDITOR")
    system(f'{editor} {path}')
    return f'edit {editor} {path}'


def extract_outline(text, section_number):
    lines = text.split('\n')
    outline = ''
    matching = False
    for line in lines:
        i = len(line)-len(line.lstrip())
        if matching == True:
            if indent >= i:
                return outline
            outline += line[indent:]+'\n'
        elif line.lstrip().startswith(section_number):
            matching = True
            indent = i
            outline += line[indent:]+'\n'
    return outline


def files_script(args):
    if not args:
        return 'usage: files pub-name'
    pub_root = Path(f'{getenv("SHRINKING_WORLD_PUBS")}/{args[0]}')
    # print(pub_root)
    files = pub_root.rglob('*')
    files = [str(f).replace(str(pub_root)+'/', '    ')
             for f in files if f.is_file()]
    return f'Files:\n\n{text_join(files)}'


def markdown_to_outline(text):
    # Define a regular expression pattern to match headings
    heading_pattern = r'^(#+)\s+(.*)'
    lines = text.split('\n')
    outline = ''
    for line in lines:
        # Check if the line matches the heading pattern
        x = match(heading_pattern, line)
        if x:
            # Extract the heading level and text
            level = len(x.group(1))
            text = x.group(2)
            # Add the heading to the outline with the appropriate indentation
            outline += '    ' * (level - 1) + text + '\n'
    return outline


pub_js = '''
{
    "name": "",
    "site_title": "",
    "site_subtitle": "",
    "domain": "https://shrinking-world.com",
    "url": "/analytics",
    "title": "",
    "author": "Mark Seaman",
    "description": "",
    "css": "/static/css/book.css",
    "doc_path": "Documents/Shrinking-World-Pubs//Pub",
    "image_path": "/static/images/Shrinking-World-Pubs/",
    "cover_image": "/static/images/Shrinking-World-Pubs//Cover.png",
    "cover_title": false,
    "pub_type": "private",
    "menu": "static/js/nav_blog.json",
    "auto_contents": false,
    "auto_index": true,
    "simple_index": true
}
'''


def project_script(args):
    def make_json(pub_root, pub_name):
        js = pub_root / f'{pub_name}.json'
        if not js.exists():
            js.write_text(pub_js)

    if not args:
        return 'usage: project pub-dir pub-name'
    pub_root = pub_path(args[0])

    (pub_root/'AI').mkdir(parents=True, exist_ok=True)
    (pub_root/'Pub').mkdir(parents=True, exist_ok=True)
    (pub_root/'Images').mkdir(parents=True, exist_ok=True)

    make_json(pub_path(args[0]), args[1])
    return str(pub_root)


def publish_script(args):
    # Function to handle "edit" command
    # ...
    if not args[1:]:
        return 'usage: publish pub-name chapter-name'
    pub_name, chapter = args
    return f'''\npublish {pub_name} {chapter}
        - copy the latest version of the chapter draft into the "Pub" directory
        - rebuild the Pub/Index.md file to match the new contents from "_content.csv" 
        '''


usage = '''

usage:
    project GhostWriter
    chapter GhostWriter Chapter1
    gpt GhostWriter Chapter1 Outline.md
    publish GhostWriter Chapter1 FinalVerson.md
    edit GhostWriter Chapter1
    files GhostWriter Chapter1
    ai GhostWriter Chapter1 Outline1
    md GhostWriter Chapter1 Outline1
    txt GhostWriter Chapter1 Outline1
    outline GhostWriter Chapter1 Outline1
    expand GhostWriter Chapter1 Outline1
    draft GhostWriter Chapter1 Outline1

'''


def pub_script_command(command, args):
    if command == 'project':
        output = project_script(args)
    elif command == 'chapter':
        output = chapter_script(args)
    elif command == 'gpt':
        output = chatgpt_script(args)
    elif command == 'edit':
        output = edit_script(args)
    elif command == 'expand':
        output = 'not implemented'
    elif command == 'files':
        output = files_script(args)
    elif command == 'outline':
        output = create_outline(args)
    elif command == 'publish':
        output = publish_script(args)
    elif command == 'scriptor':
        output = scriptor_script(args)
    else:
        output = "Invalid command: {}".format(command) + usage
    return output


def scriptor_script(args):
    pub = args[0]
    pub_root = pub_path(pub)
    pub_script = read_file(pub_root / f'AI/Script/{pub}.ai')
    lines = text_lines(pub_script)
    text = f'pub_script_command: {pub}\n\n'
    for c in lines:
        if c.strip():
            x = c.split(' ')
            text += pub_script_command(x[0], x[1:])
    return f'SCRIPTOR: \n\n{text}'
