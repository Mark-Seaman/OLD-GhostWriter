from os import getenv, system
from pathlib import Path
from re import match

from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

from publish.files import copy_files, create_directory
from publish.pub import pub_edit, pub_path
from publish.text import  text_join


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


def doc_script(args, edit=True):
    if not args[2:]:
        return 'usage: doc pub-name chapter-name doc-name'
    pub, chapter, doc = args
    path = pub_path(pub, chapter, doc)
    if edit:
        pub_edit(pub=pub, chapter=chapter, doc=doc)
    return f'doc({path})'


# def edit_script(args):
#     # Function to handle "edit" command
#     # ...
#     if not args:
#         return 'usage: pub edit pub-name'
#     path = pub_path(args[0])
#     editor = getenv("EDITOR")
#     system(f'"{editor}" -w "{path}"')
#     return f'edit "{editor}" "{path}"'


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
        js = pub_root / f'pub.json'
        if not js.exists():
            data = dict(pub_name=pub_name, pub_dir=pub_dir, tag_line='AI tools for Authors')
            json = render_to_string('pub_script/pub.json', data)
            js.write_text(json)

    if not args:
        return 'usage: project pub-dir'
    make_json(args[0])
    return f'project (pub_dir={args[0]})'



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


def pub_script_command(command, args, edit=True):
    if command == 'project':
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
    else:
        output = "Invalid command: {}".format(command) + usage
    return output

