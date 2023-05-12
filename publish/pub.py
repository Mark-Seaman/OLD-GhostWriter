from os import getenv
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
    return [pub_link(pub.name) for pub in path.iterdir() if pub.is_dir()]


def doc_list(pub, chapter):
    path = pub_path(pub, chapter)
    return [doc_link(pub, chapter, doc.name) for doc in path.iterdir() if doc.is_file()]


def chapter_list(pub):
    path = pub_path(pub)
    return [pub_link(pub, chapter.name) for chapter in path.iterdir() if chapter.is_dir()]
# pub_link(pub)

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


def pub_view_data(**kwargs):
    pub = kwargs.get('pub')
    chapter = kwargs.get('chapter')
    doc = kwargs.get('doc')

    if doc and chapter and pub:
        kwargs['text'] = read_pub_doc(pub, chapter, doc)
        kwargs['html'] = doc_html(pub, chapter, doc)
    if chapter and pub:
        kwargs['docs'] = doc_list(pub, chapter)
    if pub:
        kwargs['chapters'] = chapter_list(pub)
    kwargs['pubs'] = list_pubs()
    return kwargs


def read_pub_doc(pub, chapter, doc):
    path = pub_path(pub, chapter, doc)
    if not path.exists():
        return f"FILE NOT FOUND: {path}"
    return path.read_text()


