from pathlib import Path
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from os import getenv, system
from re import match

from publish.text import text_join, text_lines
from publish.files import read_file, recursive_files


'''
Writer Script

Examples:
- project SoftwareEngineering
- chapter SoftwareEngineering 08
- create  SoftwareEngineering 08 from 03.md Outline.md
- publish SoftwareEngineering 08
- edit SoftwareEngineering 08

'''

def chapter_script(args):
    # Function to handle "chapter" command
    # ...
    if not args[1:]:
        return 'usage: chapter pub-name chapter-name'
    pub_name, chapter = args
    project_script(args)
    chapter_path = pub_path(pub_name)/'AI'/chapter
    chapter_path.mkdir(parents=True, exist_ok=True)
    edit_script([pub_name, 'AI'])
    return f'''\nchapter {pub_name} {chapter}
        - create a directory in AI for chapter drafts
        - apply "Initial.md" script to chapter create "01.md"
        - edit the "_content.csv" file to include the chapter
        '''


def create_script(args):
    # Function to handle "edit" command
    # ...
    if not args[3:]:
        return 'usage: create pub-name chapter-name from content-file script-file'
    pub_name, chapter, content, script = args
    return f'''\ncreate {pub_name} {chapter} from {content} {script}
        - read the script and create a file that can be sent to GPT API
        - include content from the additional content file to pass to GPT API
        - execute the request to get a response
        - store the response in a the file as the latest draft (eg. 01.md, 02.md, ...)
        '''
    

def edit_script(args):
    # Function to handle "edit" command
    # ...
    if not args[1:]:
        return 'usage: edit pub-name chapter-name'
    pub_name, chapter = args
    editor = getenv("EDITOR")
    pubs_path = getenv("SHRINKING_WORLD_PUBS")
    system(f'{editor} {pubs_path}/{pub_name}/{chapter}')
    return f'''\nedit {editor} {pubs_path}
        - EDITOR={editor}
        - SHRINKING_WORLD_PUBS={pubs_path}
        - PUB={pub_name}
        - CHAPTER={chapter}
        '''

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
    files = [str(f).replace(str(pub_root)+'/', '    ') for f in files if f.is_file()]
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
    def make_project_dirs(pub_root):
        ai_path = pub_root/'AI'
        pubication_path = pub_root/'Pub'
        image_path = pub_root/'Images'
        ai_path.mkdir(parents=True, exist_ok=True)
        pubication_path.mkdir(parents=True, exist_ok=True)
        image_path.mkdir(parents=True, exist_ok=True)
        return ai_path, pubication_path, image_path

    def make_js(pub_root, pub_name):
        js = pub_root / f'Pub/{pub_name}.js'
        if not js.exists():
            js.write_text(pub_js)

    if not args:
        return 'usage: project pub-dir pub-name'
    pub_root = pub_path(args[0])
    ai_path, pubication_path, image_path = make_project_dirs(pub_root)
    make_js(pub_path(args[0]), args[1])
    return f'''\nproject {args[0]}
        - create directory {ai_path}
        - create directory {pubication_path}
        - create directory {image_path}
        '''


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


def pub_path(doc=None):
    path = Path(f'{getenv("SHRINKING_WORLD_PUBS")}')
    if doc:
        return path/doc
    return path


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


def pub_script_command(command, args):
    if command == 'project':
        output = project_script(args)
    elif command == 'chapter':
        output = chapter_script(args)
    elif command == 'create':
        output = create_script(args)
    elif command == 'publish':
        output = publish_script(args)
    elif command == 'edit':
        output = edit_script(args)
    elif command == 'files':
        output = files_script(args)
    elif command == 'scriptor':
        output = scriptor_script(args)
    else:
        output = "Invalid command: {}".format(command)
    return output
