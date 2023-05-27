from os import getenv, system
from pathlib import Path
from markdown import markdown

from .document import title
from .text import text_join, text_lines


def doc_html(pub, chapter, doc):
    return markdown(read_pub_doc(pub, chapter, doc))


def doc_title(pub, chapter, doc):
    return title(read_pub_doc(pub, chapter, doc))


def doc_text(pub, chapter, doc):
    lines = text_lines(read_pub_doc(pub, chapter, doc))[2:]
    return text_join(lines)


def list_pubs():
    path = pub_path()
    return [pub_link(pub.parent.name) for pub in path.glob('*/pub.json') if pub.parent.is_dir()]


def doc_list(pub, chapter):
    path = pub_path(pub, chapter)
    return [doc_link(pub, chapter, doc.name) for doc in sorted(path.glob('*.md')) if doc.is_file()]


def chapter_list(pub):
    path = pub_path(pub)
    return [pub_link(pub, chapter.name) for chapter in path.iterdir() if chapter.is_dir()]


def pub_link(pub, chapter=None):
    if chapter:
        url = f'/{pub}/{chapter}'
        title = chapter
    else:
        url = f'/{pub}'
        title = pub

    return f'<a href="{url}">{title}</a>'


def doc_link(pub, chapter, doc):
    url = f'/{pub}/{chapter}/{doc}'
    title = doc_title(pub, chapter, doc)
    return f'<a href="{url}">{title}</a>'


def pub_path(pub=None, chapter=None, doc=None):
    path = Path(f'{getenv("SHRINKING_WORLD_PUBS")}')

    if doc and chapter and pub:
        path = path/pub/'AI'/chapter/doc
    elif chapter and pub:
        path = path/pub/'AI'/chapter
    elif pub:
        path = path/pub/'AI'
    else:
        path = path
    return path

def doc_ai(pub, chapter, doc):
    doc = doc.replace('.md', '.ai')
    path = pub_path(pub, chapter, doc)
    if path.exists():
        return markdown(path.read_text())
    
def doc_human(pub, chapter, doc):
    doc = doc.replace('.md', '.txt')
    path = pub_path(pub, chapter, doc)
    if path.exists():
        return markdown(path.read_text())


def pub_view_data(**kwargs):
    pub = kwargs.get('pub')
    chapter = kwargs.get('chapter')
    doc = kwargs.get('doc')

    if doc and chapter and pub:
        kwargs['text'] = read_pub_doc(pub, chapter, doc)
        kwargs['html'] = doc_html(pub, chapter, doc)
        kwargs['ai'] = doc_ai(pub, chapter, doc)
        kwargs['human'] = doc_human(pub, chapter, doc)
    if chapter and pub:
        kwargs['docs'] = doc_list(pub, chapter)
    if pub:
        kwargs['chapters'] = chapter_list(pub)
    kwargs['pubs'] = list_pubs()
    return kwargs


def pub_edit(**kwargs):
    pub = kwargs.get('pub')
    chapter = kwargs.get('chapter')
    doc = kwargs.get('doc')
    path = pub_path(pub, chapter, doc)
    path2 = str(path).replace('.md','.txt')
    path3 = str(path).replace('.md','.ai')
    editor = getenv("EDITOR")
    system(f'{editor} {path} {path2} {path3}')
    url = f'/{kwargs["pub"]}/{kwargs["chapter"]}/{kwargs["doc"]}'
    return url


def read_pub_doc(pub, chapter, doc):
    path = pub_path(pub, chapter, doc)
    if not path.exists():
        return f"FILE NOT FOUND: {path}"
    return path.read_text()


