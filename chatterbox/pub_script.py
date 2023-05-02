from django.core.management.base import BaseCommand
from django.utils.text import slugify
from os import getenv, system


'''
Writer Script

Examples:
- project SoftwareEngineering
- chapter SoftwareEngineering 08
- create  SoftwareEngineering 08 from 03.md Outline.md
- publish SoftwareEngineering 08
- edit SoftwareEngineering 08

'''

def project_function(args):
    # Function to handle "project" command
    # ...
    if not args:
        return 'usage: project pub-name'
    pub_name = args[0]
    return f'''\nproject {pub_name}
        - create directory in Shrinking-World-Pubs
        - create directory Shrinking-World-Pubs/ {pub_name}/Pub and AI
        - copy scripts into AI directory
        - create chapters for Cover, Table of Contents, Introduction
        '''


def chapter_function(args):
    # Function to handle "chapter" command
    # ...
    if not args[1:]:
        return 'usage: chapter pub-name chapter-name'
    pub_name, chapter = args
    return f'''\nchapter {pub_name} {chapter}
        - create a directory in AI for chapter drafts
        - apply "Initial.md" script to chapter create "01.md"
        - edit the "_content.csv" file to include the chapter
        '''


def create_function(args):
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
    
def publish_function(args):
    # Function to handle "edit" command
    # ...
    if not args[1:]:
        return 'usage: publish pub-name chapter-name'
    pub_name, chapter = args
    return f'''\npublish {pub_name} {chapter}
        - copy the latest version of the chapter draft into the "Pub" directory
        - rebuild the Pub/Index.md file to match the new contents from "_content.csv" 
        '''
    

def edit_function(args):
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
    

def pub_script_command(command, args):
    if command == 'project':
        output = project_function(args)
    elif command == 'chapter':
        output = chapter_function(args)
    elif command == 'create':
        output = create_function(args)
    elif command == 'publish':
        output = publish_function(args)
    elif command == 'edit':
        output = edit_function(args)
    else:
        output = "Invalid command: {}".format(command)
    return output
