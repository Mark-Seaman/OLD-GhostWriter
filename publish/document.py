from markdown import markdown
from os.path import exists
from pathlib import Path
from re import findall, sub

from publish.files import read_file
from publish.text import char_fix, no_blank_lines, text_join, text_lines, word_count
from publish.image import fix_images


# def create_document(**kwargs):
#     doc = Document.objects.get_or_create(file=kwargs.get('file'))[0]
#     doc.body = kwargs.get('body')
#     doc.title = doc.body.split('\n')[0][2:]
#     doc.save()
#     write_document_file(doc)
#     return doc


def find_links(text):
    md_pattern = r"\[(.*?)\]\((.*?)\)"
    links = [(match[1], match[0]) for match in findall(md_pattern, text)]
    html_pattern = r"<a href=\"(.*?)\".*?\>(.*?)\</a\>"
    links += [(match[0], match[1]) for match in findall(html_pattern, text)]
    return links


def map_links(text):
    # markdown
    md_pattern = r"[^\!]\[(.*?)\]\((.*?)\)"
    replace_pattern = r' <a href="\2" target="_new">\1</a>'  # r'[\1](\2)'
    text = sub(md_pattern, replace_pattern, text)

    # html
    html_pattern = '<a href="(.*?)".*?>(.*?)</a>'
    replace_pattern = r'<a href="\1" target="_new">\2</a>'  # r' [\2](\1)'
    text = sub(html_pattern, replace_pattern, text)

    return text


def read_document_file(doc):
    text = open(f"Documents/{doc.file}.md").read()
    doc.markdown = text
    doc.html = text
    doc.save()


def doc_text(doc_path, image_path):
    text = doc_path.read_text()
    return fix_images(text, image_path)


def document_body(text, image_path=None):
    if image_path:
        text = fix_images(text, image_path)
        text = map_links(text)
    return text_join(text_lines(text))


def document_html(text):
    return char_fix(markdown(text, extensions=['tables']))


def document_title(path):
    if not exists(path):
        return f"Document not found, {path}"
    return text_lines(no_blank_lines(read_file(path)))[0][2:]


def get_document(path, image_path=None):
    if path.exists():
        md = document_body(read_file(path), image_path)
        words = word_count(md)
        html = document_html(md)
        title = document_title(path)
        return dict(title=title, path=path, markdown=md, html=html, words=words)
    md = Path(f"{path}.md")
    if md.exists():
        return get_document(md, image_path)
    else:
        title = "Document not found"
        html = f"<h1>Missing Document</h1><p>This document could not be found.  Sorry!</p><p>Document not found - {path}</p>"
        return dict(title=title, html=html, words=0)


def title(text):
    return text_lines(no_blank_lines(text))[0][2:]


def write_document_file(doc):
    open(f"Documents/{doc.file}.md", "w").write(doc.body + "\n")
