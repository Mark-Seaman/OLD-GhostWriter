from pathlib import Path
from random import choice
from shutil import copyfile
from publish.days import is_old

from publish.shell import banner

from .document import document_body, document_html, document_title
from .files import read_csv_file, read_file, read_json
from .import_export import create_pub, pub_json_path, save_pub_data
from .models import Content, Pub
from .text import line_count, text_join, word_count
from .toc import create_pub_index


def all_blogs():
    return all_pubs('blog')


def all_books():
    return all_pubs('book')


def all_courses():
    return all_pubs('course')


def all_privates():
    return all_pubs('private')


def all_pubs(pub_type=None):
    if pub_type:
        return list(Pub.objects.filter(pub_type=pub_type))
    else:
        return list(Pub.objects.all())


def bouncer_redirect(bouncer_id):
    if bouncer_id:
        bounce_table = read_csv_file('Documents/Shrinking-World-Pubs/_bouncer.csv')
        for x in bounce_table:
            if x[1:] and int(x[0]) == bouncer_id:
                # print(f"Bounce to {x[1]}")
                return x[1]


def build_pubs(verbose=False, delete=False):

    def build_pub_index(pub):
        if pub.auto_index:
            # if verbose:
            #     print(f"CREATE Index - {pub.name}")
            create_pub_index(pub, get_pub_contents(pub)) 

    def delete_pubs():
        if delete:
            if verbose:
                print("Delete pubs\n")
            Pub.objects.all().delete()
            assert len(Pub.objects.all()) == 0
    
    def verify_all_pubs():
        if is_old("config/publish.json"):
            if verbose:
                print("Save pubs JSON\n")
            save_pub_data()
        return verify_pubs(verbose)

    delete_pubs()
    if verbose:
        print("Build pubs:\n")
    for pub in list_publications():
        if verbose:
            print('CREATE -', pub)
        p = create_pub(pub[0], pub[1])
        build_pub_index(p)

    return verify_all_pubs()
    

def doc_view_context(**kwargs):
    path = kwargs.get('path', 'Documents/shrinking-world.com/blog/Index.md')
    json = kwargs.get('json', 'Documents/shrinking-world.com/blog.json')
    kwargs = read_json(json)
    markdown = document_body(read_file(path))
    kwargs['title'] = document_title(path)
    kwargs['html'] = document_html(markdown)
    return kwargs


def get_host(request):
    host = request.get_host()
    # if not host or host.startswith("127.0.0.1") or host.startswith("localhost"):
    #     host = "seamanslog.com"
    return host


def get_pub(name):
    return Pub.objects.get(name=name)


def get_pub_contents(pub):
    def doc_objects(pub, folder):
        return (
            Content.objects.filter(blog=pub, doctype="chapter", folder=folder)
            .order_by("order")
            .values()
        )

    def docs_in_folder(pub, folder):
        return [d for d in doc_objects(pub, folder)]

    def folder_objects(pub):
        return (
            Content.objects.filter(blog=pub, doctype="folder")
            .order_by("order")
            .values()
        )

    folders = []
    for folder in folder_objects(pub):
        docs = docs_in_folder(pub, folder.get("order"))
        folder.update(dict(documents=docs))
        folders.append(folder)
    return folders


def get_pub_info(pub_name=None):
    if pub_name:
        pubs = [get_pub(pub_name)]
    else:
        pubs = all_pubs()
    text = ''
    for pub in pubs:
        text += f'{banner(pub.name)}\n\n{pub}\n\n'
        text += f'Title: {pub.title}\n\n'
        text += f'Tag Line: {pub.subtitle}\n\n'
        text += f'Document Path: {pub.doc_path}\n\n'
        text += f'Details: \n{show_pub_details(pub)}\n\n'
        text += f'Summary: \n{show_pub_content(pub)}\n\n'  
        text += f'Words: \n{show_pub_words(pub)}\n\n' 
    return text


def list_publications():
    return read_csv_file('Documents/publications.csv')


def list_content(pub):
    return list(Content.objects.filter(blog=pub))


def pub_redirect(host, pub, doc):
    if host == "shrinking-world.com" and not pub:
        return f"/publish/book"
    if host == "seamanslog.com" and not pub:
        return f"/sampler/today"
    if host == "seamansguide.com" and not pub:
        return f"/publish/book"
    if host == "seamanfamily.org" and not pub:
        return f"/family/Index.md"
    if host == "spiritual-things.org" and not pub:
        return f"/spiritual/today"
    if host == "markseaman.org" and not pub:
        return f"/marks/ContactMe"
    if host == "markseaman.info" and not pub:
        return f"/private"
    if ("localhost" in host or "127.0.0.1" in host) and not pub:
        return f"/private"
    if not doc or not pub:
        return f"/private"
    return f"/{pub}/{doc}"


def random_doc(directory):
    return choice([p for p in Path(directory).iterdir()])


def random_doc_page(path):
    x = choice([str(f.name)
               for f in Path(path).iterdir() if str(f).endswith(".md")])
    return x.replace(".md", "")


def save_pub_info():
    path = Path(f'probe/pubs')
    if path.exists():
        for pub in all_pubs():
            text = get_pub_info(pub.name)
            f = path/ '{pub.name}'
            f.write_text(text)


def select_blog_doc(host, blog, doc):
    def load_object(pub):
        return Pub.objects.filter(pk=pub.pk).values()[0]

    def load_document(pub):
        # Find doc path - Use the markdown file extension
        path = pub.doc_path
        path = Path(path) / doc.replace("-", "/")
        if not Path(path).exists() and Path(f"{path}.md").exists():
            path = Path(f"{path}.md")

        # Load the correct document
        if path.exists():
            markdown = document_body(read_file(path), pub.image_path)
            title = document_title(path)
            html = document_html(markdown)
        else:
            title = "Missing Document"
            html = f"<h1>Document file not found<h1><h2> {path}</h2>"

        return dict(
            title=title, html=html, site_title=pub.title, site_subtitle=pub.subtitle
        )

    pub = get_pub(blog)
    kwargs = load_object(pub)
    kwargs.update(load_document(pub))
    menu = kwargs.get("menu")
    if menu:
        kwargs["menu"] = read_json(menu)["menu"]

    return kwargs


def show_pub_content(pub):
    text = f"PUB CONTENT - {pub.title}\n\n"
    folders = get_pub_contents(pub)
    for f in folders:
        text += f"\nFOLDER {f.get('path')}\n"
        for d in f.get("documents"):
            text += f"     {d.get('path')}\n"
    return text


def show_pub_details(pub):
    content = pub.content_set.all()
    output = f'Pub Contents - {pub.name} - {pub.title}'
    total_words = 0
    for f in content.filter(folder=0):
        folder_words = word_count(read_file(f.path))
        output += f'\n{f.title} - {f.path} - {folder_words} words\n'
        for d in content.filter(folder=f.order):
            words = word_count(read_file(d.path))
            folder_words += words
            output += f'    {d.title} - {d.path} - {words} words\n'
        output += f'    Words in {f.title}: {folder_words} words\n'
        total_words += folder_words
    output = f'\nTotal Words in {pub.title}: {total_words} words, {int(total_words/250)} pages\n'
    pub.words = total_words
    pub.save()
    return output


def show_pub_json(pub=None):
    if pub:
        pubs =[get_pub(pub)]
    else:
        pubs = all_pubs()
    return text_join([read_file(pub_json_path(pub.name, pub.doc_path)) for  pub in pubs])
        
    # text = "PUB JSON\n\n"
    # for js in Path("static/js").iterdir():
    #     text += f"\n\n---\n\n{js}\n\n---\n\n"
    #     text += js.read_text()
    # return text


def show_pub_words(pub=None):
    text = "PUB WORDS\n\n"
    pubs = [pub] if pub else all_pubs()
    for pub in pubs:
        path = word_count_file(pub)
        text += f"\n\n---\n\n{path}\n\n---\n\n"
        text += path.read_text()
    return text


def show_pubs():
    output = "PUBLICATIONS:\n\n"
    for t in ['book', 'blog', 'private']:
        text = ''
        words = 0
        for p in all_pubs(t):
            text += f'    {p.name:15} -  {p.title:35} - {p.words:5} words\n'
            words += p.words
            get_pub(p.name)
        output += f'\nPubs - {t} - {words} words - {int(words/250)} pages\n{text}\n'
    return output    


def verify_pubs(verbose):
    pubs = list_publications()
    for p in pubs:
        if p:
            pub = Pub.objects.filter(doc_path=p[1], name=p[0])
            if pub:
                pub = pub[0]
            else:
                print("NO OBJECT", p)
                assert False
        # if not Path(pub.doc_path).exists():
        #     print(f'   {pub.name} -- {pub.doc_path} -- NOT FOUND')
        assert Path(pub.doc_path).exists()
        json = pub_json_path(pub.name, pub.doc_path)
        # if json.exists():
        #     print(f'   JSON {json} NOT FOUND')
        assert json.exists()

    pubs = list(Pub.objects.all())
    info = line_count(get_pub_info())
    contents = len(Content.objects.all())
    # min_lines, max_lines = 57, 57
    # if min_lines < info and info < max_lines: 
    #     text = f'Rebuild Pubs:  {text_join([str(p) for p in  pubs])}\n'
    #     text += f'\nPub Info: {info}\n'
    #     text += f'\nPub Contents: {contents}\n'
    #     if verbose:
    #         print(text)
    #     else:
    #         return text
    # else:
    #     print(f'** Pub Info: {info} Lines **')
    #     assert info>min_lines
    #     assert info<max_lines


def word_count_file(pub):
    path = Path("Documents") / "words"
    if not path.exists():
        path.mkdir(exist_ok=True, parents=True)
    path = path / pub.name
    if not path.exists():
        path.write_text('')
    return path
