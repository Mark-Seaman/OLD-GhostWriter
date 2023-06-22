from os import system
from pathlib import Path
from re import sub
from shutil import copyfile

from django.template.loader import render_to_string
from django.utils.timezone import localdate

from .ai import ghost_prompt
from .cover import write_cover
from .files import read_file, write_file
from .management.commands.edit import edit_file
from .models import Content
from .publication import get_pub, show_pub_words
from .seamanslog import create_toot_file, random_article
from .slides import create_slides, markdown, plant, write_workshop
from .text import text_lines


def write_blog(args=[]):
    # print(f"write blog {args}")
    if not args:
        return '''usage: write [options]

            options:
                blogcast - write a blogcast article
                cover - design a cover for a book, blog, or video
                green - show the Greenhouse for Ideas
                io - edit the Shrinking World I/O website
                plant topic - create Markdown for the selected idea
                markdown doc - conver the Markdown to HTML
                masto - select an article, review it, and create a posting
                new - create a new publication
                render source dest script template - create a post file
                slides - create a slide show from an outline
                seamanslog - edit the blog post for today
                spiritual - edit the blog post for today
                today - daily video blog
                words - summary of word count

        '''
    elif args[0] == 'ai':
        write_ai(args[1:])
    elif args[0] == 'blogcast':
        # write blogcast Documents/markseaman.org/today/03/Success
        # write blogcast Documents/spiritual-things.org/transformation/LifeWithGod.ol
        write_blogcast(args[1:])
    elif args[0] == 'cover':
        write_cover(args[1:])
    elif args[0] == 'genetics':
        edit_genetics()
    elif args[0] == 'green':
        greenhouse()
    elif args[0] == 'io':
        ghost_write(args[1:])
        edit_io(args[1:])
    elif args[0] == 'markdown':
        markdown(args[1:])
    elif args[0] == 'masto':
        write_masto()
    elif args[0] == 'new':
        edit_file(new_pub(args[1:]))
    elif args[0] == 'plant':
        edit_file(plant(args[1:]))
    elif args[0] == 'render':
        return write_render(args[1:])
    elif args[0] == 'slides':
        # write slides Documents/shrinking-world.com/greenhouse/Content
        # write slides Documents/shrinking-world.org/L1-message
        return create_slides(args[1:])
    elif args[0] == 'seamanslog':
        today = localdate().strftime("%m/%d") + ".md"
        args[0] = f"Documents/seamanslog.com/sampler/{today}"
        edit_file(args)
    elif args[0] == 'spiritual':
        today = localdate().strftime("%m/%d") + ".md"
        args[0] = f"Documents/spiritual-things.org/daily/{today}"
        edit_file(args)
    elif args[0] == 'tech':
        write_tech(args[1:])
    elif args[0] == 'today':
        write_today()
    elif args[0] == 'words':
        write_words(args[1:])
    elif args[0] == 'workshop':
        write_workshop(args[1:])
    else:
        write_pub(args)

def edit_genetics():
    x = Path.home()/'Github/Shrinking-World-Pubs/Genetics/Book'
    y = Path('Documents/Shrinking-World-Pubs/Genetics')
    for p in x.iterdir():
        print(f'GENETICS {p} {y}')
        copyfile(p, y/p.name)
    edit_file(x.parent)


def edit_io(args):
    print('The Shrinking World I/O')
    path = 'Documents/shrinking-world.io'
    if args:
        path = ghost_write(args)
    system('open https://shrinking-world.io/ghost/#/site')
    edit_file(path)


def ghost_write(args):
    def write_weekly(file):
        text = 'RAW TEXT'
        data = dict(file=file)
        text = render_to_string('pub/ghost_weekly.md', data)
        path.write_text(text)

    def write_article(path, args):
        p = (args[1:] and args[1] == 'p')
        n = (args[1:] and args[1] == 'n')
        print(f'Ghost write ({p}, {n})')
        file = path
        text = 'MARKDOWN TEXT'
        link_url = f'https://shrinking-world.com/{file}'
        options = dict(file=file, text=text, template='pub/ghost.md',
                       paragraph=p, numbered_list=n,
                       page_title='I/O TITLE',
                       page_url=file,
                       link_title='LINK PAGE TITLE',
                       link_url=link_url)
        write_post(path,  options)

    path = Path('Documents/shrinking-world.io/ghost.org')
    if args:
        path = path/(args[0]+'.md')
        if 'weekly' in args[0]:
            write_weekly(args[0])
        else:
            write_article(path, args)
    else:
        edit_file(path)
    return path


def greenhouse():
    edit_file(['Documents/shrinking-world.com/greenhouse',
               'Documents/shrinking-world.com/greenhouse/Content.ol',
               'Documents/shrinking-world.com/greenhouse'])


def new_pub(args):

    def make_dir(d):
        if not d.exists():
            d.mkdir()

    x = Path(f'Documents/Shrinking-World-Pubs/{args[0]}')
    make_dir(x)
    make_dir(x/'AI')
    make_dir(x/'Images')
    make_dir(x/'Pub')
    write_cover([x.name])
    return x

def render_document(**kwargs):

    def read_source(source):
        if source:
            path = Path(source)
            if path.exists():
                text = path.read_text()
            else:
                text = f'\n**** BAD FILE **** {path}\n'
        return text

    def apply_script(script, text):
        if script:
            if script == 'upcase':
                text = text.upper()
            elif script == 'review':
                text = random_article()['text']
            else:
                text += f'\n**** BAD SCRIPT **** {script}\n'
        return text

    def render_template(template, text):
        if template:
            if template == 'blog':
                text = render_to_string('pub/blog.md', dict(text=text))
            elif template == 'message':
                text = render_to_string(
                    'pub/message.md', dict(text=text[:500]))
            else:
                text += f'\n**** BAD TEMPLATE **** {template}\n'
        return text

    def write_dest(dest, text):
        if dest:
            path = Path(dest)
            path.write_text(text)

    source = kwargs.get('source')
    dest = kwargs.get('dest')
    script = kwargs.get('script')
    template = kwargs.get('template')
    text = read_source(source)
    text = apply_script(script, text)
    text = render_template(template, text)
    write_dest(dest, text)
    return text


def write_ai(args):
    if args:
        print('AI', args)
        pub = get_pub(args[0])
        path1 = f'{pub.doc_path}/../AI/{args[1]}'
        path2 = f'{pub.doc_path}/../AI/Response.md'
        ghost_prompt(path1, path2)
        # print(read_file(path))
        # path = Path(f'Documents/Shrinking-World-Pubs/i/{args[0]}.md')
        # p = (args[1:] and args[1] == 'p')
        # n = (args[1:] and args[1] == 'n')
        # data = dict(file=path, text='RAW TEXT', template='pub/ai.md',
        #             paragraph=p, numbered_list=n)
        # write_post(path,  data)
    else:
        # edit_file(f'Documents/shrinking-world.com/ai')
        system('open https://chat.openai.com/chat')


def write_blogcast(args=[]):
    print(f'write blogcast {args[0]+".ol"} {args[0]+".md"}')
    text = ''
    d = args[0]
    f = args[1]
    lines = text_lines(read_file(f'{d}/{f}.ol'))
    for line in lines:
        if not line:
            text += '\n'
        elif not line.startswith('    '):
            text += f'# {line}\n\n'
        elif not line.startswith('        '):
            text += f'\n## {line.strip()}\n\n'
        elif line:
            text += f'* {line.strip()}\n'
    f = f'{d}/{f}.md'
    write_file(f, text)
    print(text)


def write_masto(args=[]):
    print(f"write masto {args}")
    edit_file(create_toot_file())


def write_post(path, options):

    def write_post_file(path, options):
        if path.exists():
            text = fix_text(path.read_text(), options)
            path.write_text(text)
            print(path, '\n', text)
        else:
            text = render_to_string(options.get('template'), options)
        path.write_text(text)

    def fix_text(text, options):
        if options.get('paragraph'):
            text = text.replace('\n', '\n\n')
            text = text.replace('\n\n\n\n', '\n\n')
            text = text.replace('\n\n\n\n', '\n\n')
        if options.get('numbered_list'):
            text = sub(r'\n   ', '\n* ', text)
            text = sub(r'\n\d\. ', '\n* ', text)
        return text

    print(f'write_post {path} {options}')
    write_post_file(path, options)
    edit_file(path)


def write_pub(args):
    if args[0] == 'pub':
        pub = None
    else:
        pub = get_pub(args[0])
    print(f'WRITE {pub} {args}')
    if args[1:]:
        c = Content.objects.filter(blog=pub, path__endswith=args[1])
        if c:
            args = [c[0].path]
    else:
        article = random_article(pub)
        args[0] = article["doc"]
        print(f'SELECT {args}')
    if Path(args[0]).exists() and Path(args[0]).is_file():
        edit_file(args)


def write_render(args):
    # print(f"write render {args}")
    if not args[3:]:
        return 'usage: write render source dest script template'
    text = render_document(source=args[0], dest=args[1],
                           script=args[2], template=args[3])
    return text


def write_tech(args):
    if args:
        edit_file(f'Documents/shrinking-world.com/blog/{args[0]}')
    else:
        edit_file('Documents/shrinking-world.com/blog')


def write_today():
    edit_file('Documents/markseaman.org/today')


def write_words(args=[]):
    print(f"write words {args}")
    for pub in args:
        pub = get_pub(pub)
        print(show_pub_words(pub))
        # edit_file(f"Documents/markseaman.info/words/{args[0]}")
    edit_file(f"Documents/markseaman.info/words")
