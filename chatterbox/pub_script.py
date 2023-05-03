from pathlib import Path
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from os import getenv, system

from .text import text_join
from .files import recursive_files


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


def files_script(args):
    if not args:
        return 'usage: files pub-name'
    pub_root = Path(f'{getenv("SHRINKING_WORLD_PUBS")}/{args[0]}')
    print(pub_root)
    files = pub_root.rglob('*')
    files = [str(f).replace(str(pub_root)+'/', '    ') for f in files if f.is_file()]
    return f'Files:\n\n{text_join(files)}'


def project_script(args):
    def make_project_dirs(pub_root):
        ai_path = pub_root/'AI'
        pubication_path = pub_root/'Pub'
        image_path = pub_root/'Images'
        ai_path.mkdir(parents=True, exist_ok=True)
        pubication_path.mkdir(parents=True, exist_ok=True)
        image_path.mkdir(parents=True, exist_ok=True)
        return ai_path, pubication_path, image_path

    if not args:
        return 'usage: project pub-name'
    pub_root = pub_path(args[0])
    ai_path, pubication_path, image_path = make_project_dirs(pub_root)
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


def pub_path(pub):
    return Path(f'{getenv("SHRINKING_WORLD_PUBS")}/{pub}')


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
    else:
        output = "Invalid command: {}".format(command)
    return output
