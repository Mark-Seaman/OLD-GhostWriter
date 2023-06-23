from os import getenv
from pathlib import Path
from re import match

from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

from publish.files import copy_files, create_directory
from publish.import_export import copy_static_files
from publish.publication import all_pubs, build_pubs, get_pub, get_pub_info
from publish.text import text_join, text_lines

from .pub_dev import pub_edit, pub_path

usage = '''

usage:
    build
    test

    project GhostWriter writer
    chapter GhostWriter Chapter1
    doc GhostWriter Chapter1 A-Outline.md
    edit GhostWriter Chapter1
    publish GhostWriter Chapter1 FinalVerson.md

    files GhostWriter Chapter1
    ai GhostWriter Chapter1 Outline1
    md GhostWriter Chapter1 Outline1
    txt GhostWriter Chapter1 Outline1

    # outline GhostWriter Chapter1 Outline1
    # expand GhostWriter Chapter1 Outline1

'''

def ai_script(args):
    if not args[2:]:
        return 'usage: ai pub chapter doc'
    pub_name, chapter, doc = args
    return f'Running ai on {pub_path(pub_name,chapter,doc)}'


def build_script(args):
    # if args:
    #     return 'usage: build'
    text = build_pubs(True, True)
    return f'Build all pubs: {text}'


def chapter_script(args):
    # Function to handle "chapter" command
    # ...
    if not args[1:]:
        return 'usage: chapter pub-name chapter-name'
    pub, chapter = args
    chapter_path = pub_path(pub, chapter)
    create_directory(chapter_path)
    # copy_files(pub_path(pub, 'Storyboard'), chapter_path)
    return f'chapter ({chapter_path})'


def create_outline(args):
    path = pub_path(args[0], args[1], args[2])
    text = markdown_to_outline(path.read_text())
    if args[3:]:
        text = extract_outline(text, args[3])
    return text


def doc_script(args, edit=False):
    if not args[2:]:
        return 'usage: doc pub-name chapter-name doc-name'
    pub, chapter, doc = args[:3]
    path = pub_path(pub, chapter, doc)
    # edit = False
    if edit:
        pub_edit(pub=pub, chapter=chapter, doc=doc)
    return f'doc({path})'


def execute_pub_script(args):
    if not args:
        return 'usage: script script-file'
    script = Path(args[0])
    if not script.exists():
        return f'SCRIPT not found: (script)'
    commands = text_lines(script.read_text())
    commands = [pub_script(c.strip().split(' ')) for c in commands if c.strip()]
    return text_join(commands)


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


def project_script(args):
    def make_json(pub_dir):
        pub_name = pub_dir
        pub_root = pub_path() / pub_dir
        pub_root.mkdir(exist_ok=True, parents=True)
        js = pub_root / f'pub.json'
        if not js.exists():
            data = dict(pub_name=pub_name, pub_dir=pub_dir,
                        tag_line='AI tools for Authors')
            json = render_to_string('pub_script/pub.json', data)
            js.write_text(json)
        return f'JSON file: {js}\n'

    text = f"Create Pub: {args[0]}\n"
    if not args:
        text += 'usage: project pub-name'
        return text 
    text += make_json(args[0])
    return text

# def pub_json_path(name, doc_path):
#     path = Path(doc_path)
#     path.mkdir(exist_ok=True, parents=True)
#     json1 = Path(f'static/js/{name}.json')
#     json2 = path/'pub.json'
#     json3 = path.parent/'pub.json'
#     if json2.exists():
#         if path.name == 'Pub':
#             json2.rename(json3)
#             return json3
#         return json2
#     if json3.exists():
#         return json3
#     if json1.exists():
#         print("COPY FILE", json1, json2)
#         copyfile(json1, json2)
#         return json1
#     return json2

def publish_script(args):
    if not args:
        return 'usage: publish pub-name'
    pub_name = args[0]
    pub = get_pub(pub_name)
    text = f'\npublish {pub_name}\n'
    images = Path(pub.doc_path).parent/'Images'
    if images.exists():
        text += f'copy the "{pub.image_path}" directory from "{images}"\n'
        copy_static_files(pub)
    text += 'rebuild the Pub/Index.md file to match the new contents from "_content.csv" \n'
    return text


def pub_script(command_args, edit=True):
    if not command_args:
        return "Invalid command: {}".format(command_args) + usage
    command = command_args[0]
    args = command_args[1:]
    if command == 'build':
        output = build_script(args)
    elif command == 'project':
        output = project_script(args)
    elif command == 'chapter':
        output = chapter_script(args)
    elif command == 'doc':
        output = doc_script(args, edit)
    # elif command == 'edit':
    #     output = edit_script(args)
    # elif command == 'expand':
    #     output = 'not implemented'
    elif command == 'files':
        output = files_script(args)
    elif command == 'outline':
        output = create_outline(args)
    elif command == 'publish':
        output = publish_script(args)
    elif command == 'script':
        output = execute_pub_script(args)
    elif command == 'test':
        output = test_script(args)
    else:
        output = "Invalid command: {}".format(command) + usage
    return output


def test_script(args):
    # if args:
    #     return 'usage: test'

    text = publish_script(args)

    # text = f'Pubs:\n\n{[str(p) for p in all_pubs()]}\n'
    # text += get_pub_info(args[0])
    
    return f'Test all pubs:\n\n{text}'

