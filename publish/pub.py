from os import getenv
from markdown import markdown

from chatterbox.pub_script import pub_path

from .document import title
from .text import text_join, text_lines


def read_pub_doc(doc_path):
    path = pub_path(doc_path)
    if not path.exists():
        return f"FILE NOT FOUND: {path}"
    return path.read_text()


def doc_html(doc_path):
    return markdown(read_pub_doc(doc_path))

def doc_title(doc_path):
    return title(read_pub_doc(doc_path))


def doc_text(doc_path):
    lines = text_lines(read_pub_doc(doc_path))[2:]
    return text_join(lines)


def list_pubs():
    path = pub_path()
    return [pub_link(pub.name) for pub in path.iterdir() if pub.is_dir()]


def doc_list(pub):
    path = pub_path(pub)
    return [doc_link(pub, doc.name) for doc in path.iterdir() if doc.is_file()]


def pub_link(pub):
    url = f'/{pub}'
    title = pub
    return f'<a href="{url}">{title}</a>'


def doc_link(pub, doc=None):
    if doc:
        url = f'/{pub}/{doc}'
        title = doc_title(f'{pub}/{doc}')
    else:
        url = f'/{pub}'
        title = doc_title(f'{pub}')
    return f'<a href="{url}">{title}</a>'
