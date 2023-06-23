from os import system
from pathlib import Path
from shutil import copyfile

from .document import get_document
from .files import read_csv_file, read_json
from .models import Content, Pub
from .toc import content_file, write_content_csv


def create_pub(pub_name, pub_path):

    def update_record(name, doc_path):
        json = pub_json_path(name, doc_path)
        s = read_json(json)
        b = Pub.objects.get_or_create(name=name)[0]
        b.doc_path = doc_path
        b.title = s["site_title"]
        b.subtitle = s["site_subtitle"]
        b.domain = s.get("domain")
        b.url = s["url"]
        b.description = s["description"]
        b.css = s["css"]
        b.image_path = s["image_path"]
        b.cover_image = s.get("cover_image")
        b.pub_type = s.get("pub_type", "blog")
        b.menu = s.get("menu")
        b.logo = s.get("logo")
        b.auto_remove = s.get("auto_remove", False)
        b.auto_index = s.get("auto_index", False)  # simple_index
        b.simple_index = s.get("simple_index", False)
        b.auto_contents = s.get("auto_contents", False)
        b.index_folders = s.get("index_folders", False)
        b.index_months = s.get("index_months", False)
        b.save()
        return b

    def import_pub(pub):
        content = content_file(pub)
        if pub.auto_contents:
            write_content_csv(pub)
        import_content(pub, content)
        delete_extra_objects(pub)

    def set_content(pub, doctype, path, folder, order):
        path = Path(pub.doc_path) / path
        x = Content.objects.get_or_create(
            blog=pub, doctype=doctype, order=order, path=path
        )[0]
        doc = get_document(path)
        x.folder = folder
        x.title = doc["title"]
        x.words = doc["words"]
        x.retain_object = True
        x.save()

    def import_content(pub, index):
        content = read_csv_file(index)
        for row in content:
            if row[2:]:
                set_content(pub, "chapter", row[0], row[1], row[2])
            elif row:
                set_content(pub, "folder", row[0], 0, row[1])
        contents = len(Content.objects.filter(blog=pub))
        # print(f'Contents objects: {pub.name} {contents}')
        assert contents>0

    def delete_extra_objects(pub):
        Content.objects.filter(blog=pub, retain_object=False).delete()
        for c in Content.objects.filter(blog=pub):
            c.retain_object = False
            c.save()

    pub = update_record(pub_name, pub_path)
    import_pub(pub)
    copy_static_files(pub)
    return pub


def copy_static_files(pub):
    source = Path(pub.doc_path)/'../Images'
    dest = Path(pub.image_path[1:])
    if source.exists():
        dest.mkdir(exist_ok=True, parents=True)
        for f in source.iterdir():
            # print(f"COPY FILES {pub.name} {f} {dest/f.name}")
            copyfile(f, dest/f.name)


def pub_json_path(name, doc_path):
    path = Path(doc_path)
    path.mkdir(exist_ok=True, parents=True)
    json1 = Path(f'static/js/{name}.json')
    json2 = path/'pub.json'
    json3 = path.parent/'pub.json'
    if json2.exists():
        if path.name == 'Pub':
            json2.rename(json3)
            return json3
        return json2
    if json3.exists():
        return json3
    if json1.exists():
        print("COPY FILE", json1, json2)
        copyfile(json1, json2)
        return json1
    return json2
    
    
def load_data():
    Pub.objects.all().delete()
    system("python manage.py loaddata config/publish.json")
    Content.objects.filter(words=0).delete()
    pubs = len(Pub.objects.all())
    print(f"Loaded {pubs} Pubs")
    content = len(Content.objects.all())
    print(f"Loaded {content} Content Posts")


def rename_file(f1, f2):
    if not Path(f1).exists():
        print("No PATH", f1)
    else:
        assert Path(f1).exists()
        Path(f1).rename(Path(f2))
        print(f"rename {f1} {f2}")
    assert Path(f2).exists()


def refresh_pub_from_git():
    system('cd Documents/Shrinking-World-Pubs && git pull')


def save_pub_data():
    command = '''
        {
            python manage.py dumpdata --indent 4 publish > config/publish.json &&
            git add config/publish.json &&
            git commit -m "Save pub JSON" &&
            git push
        } 2>/dev/null  > /dev/null 
    '''
    system(command)
