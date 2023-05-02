# Ghost Writer Application

a dream tool for authors

## What is Ghost Writer?

An application for creating publications using an AI agent.

A set of scripts perform file operations on a pub collection.

AI prompts are used to read and write files and to invoke a GPT Chat agent.

The writer's main goal is to design prompts to force GPT to write the desired content.

This is a process I call "**Metawriting**".


## Chatterbox

At the heart of the Ghost Writer application is an AI agent.

The Python function takes an input script and sends it to the GPT engine.

The output is collected and returned.

    def ghost_prompt(in_file, out_file)

GhostWriter/config/.env

    OPENAI_API_KEY={secret api for openai}


## Pub Script

A Django management command interpreter is used to define a domain specific language (DSL)
to work with publications.

Pubscript Commands Examples:

- project SoftwareEngineering
- chapter SoftwareEngineering 08
- create  SoftwareEngineering 08 from 03.md Outline.md
- publish SoftwareEngineering 08
- edit SoftwareEngineering 08


### project Command
Create a new project in the Pub directory

    example:
        project SoftwareEngineering

    usage:
        python manage.py project pub_name

    actions:
        - create directory in Shrinking-World-Pubs
        - create directory Shrinking-World-Pubs/pub_name/Pub and AI
        - copy scripts into AI directory
        - create chapters for Cover, Table of Contents, Introduction


### chapter Command
Create a new chapter folder in the selected Pub.  This folder will hold all of the
revisions of the chapter content during development.

    example:
        chapter SoftwareEngineering Intro

    usage:
        python manage.py chapter pub_name chapter_name

    actions:
        - create a directory in AI for chapter drafts
        - apply "Initial.md" script to chapter create "01.md"
        - edit the "_content.csv" file to include the chapter


### create Command
Create a new draft for the chapter using a GPT prompt file and some existing content.
The new draft is saved in the development folder as a numbered version.

    example:
        create SoftwareEngineering Intro from 03.md Outline.md

    usage:
        python manage.py create pub_name chapter_name from content script

    actions:
        - read the script and create a file that can be sent to GPT API
        - include content from the additional content file to pass to GPT API
        - execute the request to get a response
        - store the response in a the file as the latest draft (eg. 01.md, 02.md, ...)


### publish Command
Update the specified chapter content by selecting the latest version of the
drafts in the chapter's development folder.  Copy the file into the "Pub" directory
to make it the official version of the chapter.

    example:
        publish SoftwareEngineering Intro

    usage:
        python manage.py publish pub_name chapter_name 

    actions:
        - copy the latest version of the chapter draft into the "Pub" directory
        - rebuild the Pub/Index.md file to match the new contents from "_content.csv" 


### edit Command
Run a text editor and visit the chapter content so that it can be edited.

    example:
        edit SoftwareEngineering Intro

    usage:
        python manage.py edit pub_name chapter_name

    actions:
        GhostWriter/config/.env
            - EDITOR={editor}
            - SHRINKING_WORLD_PUBS={pubs_path}
        Run the system script
            $EDITOR $SHRINKING_WORLD_PUBS/$PUB/$CHAPTER

### files Command
Create a list of files in the selected pub project.

    example:
        files SoftwareEngineering

    usage:
        python manage.py files pub_name

    actions:
        GhostWriter/config/.env
            - SHRINKING_WORLD_PUBS={pubs_path}
        Recursive list all all files



## Prompt Library

The prompts for ChatGPT are organized around different domains.

* Django code
* Linux automation
* Software Engineering
* Innovation
* Web design
* Write
* Teach
* Learn
* Spirituality
* Publish
* Stories
* Poems
