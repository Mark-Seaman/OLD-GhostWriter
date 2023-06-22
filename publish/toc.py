from calendar import month_name
from django.template.loader import render_to_string
from pathlib import Path

from publish.files import fix_chars


def create_pub_index(pub, content_tree):
    def url(pub_name, path):
        path = Path(path)
        return f"/{pub_name}/{path.parent.name}-{path.name}"

    def link(text, url):
        return f"[{text}]({url})"

    def folder_index_text(folder, documents):
        path = folder.get("path")
        docs = []
        name = Path(path).parent.name
        if pub.index_months:
            title = f"Month of {month_name[int(name)]}"
        else:
            folder.get('title')
        # print(title)
        for doc in documents:
            if not doc["path"].endswith("Index.md"):
                docs.append(link(doc["title"], url(pub.name, doc["path"])))
        data = dict(title=title, docs=docs)
        return fix_chars(render_to_string("pub/pub_index.md", data))

    def top_index_text(content_tree):
        path = Path(pub.doc_path) / "Index.md"
        docs = [
            link(f["title"], url(pub.name, f["path"]))
            for f in content_tree
            if f["path"] != str(path)
        ]
        data = dict(title="Table of Contents", docs=docs)
        # print("TOP FOLDER", data["title"])
        text = render_to_string("pub/pub_index.md", data)
        path.write_text(fix_chars(text))

    def folder_index(folder):
        text = folder_index_text(folder, folder.get("documents"))
        path = Path(folder.get("path"))
        path.write_text(fix_chars(text))

    def folders(content_tree):
        return content_tree[1:]

    def top_folder(content_tree):
        return content_tree[0]

    if pub.index_folders or pub.index_months:
        for f in folders(content_tree):
            folder_index(f)
        if pub.auto_index:
            top_index_text(content_tree)
    elif pub.auto_index:
        write_toc_index(pub, content_tree)

    # for f in content_tree:
    #     if f.get("doctype") == "folder":
    #         path = f.get("path")
    #         name = Path(path).parent.name
    #         if not pub.doc_path.endswith(name):
    #             folder_index(f)
    #         else:
    #             top_index_text(content_tree)


def content_file(pub):
    return Path(pub.doc_path) / "_content.csv"


def pub_contents(pub):
    return f"\n\n{pub.title}\n\n{read_content_csv(pub)}"


def read_content_csv(pub):
    path = content_file(pub)
    if not path.exists():
        write_content_csv(pub)
    return path.read_text()


def show_word_count(label, word_count, post_count=None):
    if word_count > 1000:
        words = f"{int(word_count / 1000)}k"
    else:
        words = word_count
    pages = int(word_count / 250)
    if post_count:
        return f"{label} {post_count} Posts, {words} Words, {pages} Pages\n"
    elif word_count != 0:
        return f"{label} {words} Words, {pages} Pages\n"
    else:
        return f"{label}\n"


def table_of_contents(pub, content_tree, word_count=False):
    def link(folder, pub, title, url, words):
        url = url.replace(pub.doc_path, "")[1:]
        url = url.replace("/", "-")
        # words = int(words) if words else 0
        if folder and not pub.simple_index:
            label = f"\n## [{title}](/{pub.name}/{url})"
        else:
            label = f"* [{title}](/{pub.name}/{url})"
        return show_word_count(f"{label:80}", int(words))

    text = f"# {pub.title}\n\n"
    for f in content_tree:
        url = Path(f.get("path")).name
        title = f.get("title")
        w = f["words"] if word_count else '0'
        text += link(True, pub, title, f.get("path"), w) + "\n"
        for d in f.get("documents"):
            url = Path(d.get("path")).name
            title = d.get("title")
            w = d["words"] if word_count else '0'
            text += link(False, pub, title, d.get("path"), w)
    return text


def write_toc_index(pub, content_tree):
    toc = Path(pub.doc_path) / "Index.md"
    toc.write_text(fix_chars(table_of_contents(pub, content_tree)))


def write_content_csv(pub):
    def is_markdown(path):
        x = str(path)
        return path.is_file() and x.endswith(".md") and not x.endswith("Index.md")

    content = "Index.md,0\n"
    folder = Path(pub.doc_path)
    for i, d in enumerate(sorted(folder.iterdir())):
        if d.is_file():
            if is_markdown(d):
                content += f"{d.name},{i+1}\n"
        elif d.is_dir():
            content += f"{d.name}/Index.md,{i+1}\n"
            for j, f in enumerate(sorted(d.iterdir())):
                if is_markdown(f):
                    content += f"{d.name}/{f.name},{i+1},{j+1}\n"
    Path(content_file(pub)).write_text(content)
