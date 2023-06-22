from pathlib import Path
from re import findall, sub

from publish.files import read_json
from publish.shell import banner
from publish.text import text_join


def check_images(path, image_path):
    images = []
    for i in find_images(path):
        image = i.replace("img", image_path)
        if Path(image).exists():
            images.append(f"FOUND: {image}")
        else:
            images.append(f"MISSING: {image}")
    return images


def fix_images(text, image_path):
    html_pattern = '<img .*src=["\']img/(.*?)["\'].*? alt="(.*?)".*?>'
    replace_pattern = rf"![\2]({image_path}/\1)"
    text = sub(html_pattern, replace_pattern, text)
    md_pattern = r"\[(.*)\]\(img/(.*)\)"
    replace_pattern = rf"[\1]({image_path}/\2)"
    text = sub(md_pattern, replace_pattern, text)
    return text


def find_images(text):
    def md_images(text):
        return findall(r"\!\[.*\]\((.*)\)", text)

    def html_images(text):
        return findall("<img .*src=[\"'](.*?)[\"'].*?>", text)

    return md_images(text) + html_images(text)


def show_images_found(images):
    s = [f"\n{i[0]}\n    " + "\n    ".join(i[1]) for i in images if i[1:] and i[1]]
    return text_join(s)


def verify_blog_images():
    output = ""

    doc_path = Path(f"Documents/seamanslog.com")
    image_path = f"static/images/seamanslog.com"
    images = verify_images(doc_path, image_path)
    show_images_found(images)
    title = banner("Images in SEAMANSLOG")
    output += f"\n\n{title}\n\n"
    output += show_images_found(images)

    doc_path = Path(f"Documents/spiritual-things.org/daily")
    image_path = f"static/images/spiritual-things.org"
    images = verify_images(doc_path, image_path)
    title = banner("Images in SPIRITUAL")
    output += f"\n\n{title}\n\n"
    output += show_images_found(images)

    return output


# def verify_course_images():
#     output = ""
#     for course in ["bacs200", "bacs350", "cs350"]:
#         doc_path = Path(f"Documents/shrinking-world.com/{course}")
#         settings = read_json(doc_path / "course.json")
#         image_path = settings["images"]
#         images = verify_images(doc_path, image_path)
#         title = banner(settings["site_title"])
#         output += f"\n{title}"
#         output += show_images_found(images)
#     return output


# def verify_textbook_images():
#     output = ""
#     for text in ["chapter", "skill", "demo", "project"]:
#         doc_path = Path(f"Documents/shrinking-world.com/bacs350/{text}")
#         image_path = "Documents/seamansguide.com/webapps/img"
#         images = verify_images(doc_path, image_path)
#         output += show_images_found(images)
#     return output


# def verify_book_images():
#     output = ""
#     for book in ["journey", "quest", "poem", "leverage"]:
#         pub = get_pub()
#         doc_path = Path(f"Documents/seamansguide.com/{book}")
#         settings = read_json(f"static/js/{book}.json")
#         image_path = settings["image_path"][1:]
#         images = verify_images(doc_path, image_path)
#         title = banner(settings["site_title"])
#         output += f"\n{title}"
#         output += show_images_found(images)
#     return output


def verify_images(doc_path, image_path):
    images = []
    for doc in doc_path.glob("**/*.md"):
        text = doc.read_text()
        # text = fix_images(text, image_path)
        text = check_images(text, image_path)
        images.append((doc, text))
    return images


# def verify_all_images():
#     print(verify_book_images())
#     print(verify_blog_images())
#     print(verify_course_images())


def doc_text(doc_path, image_path):
    text = doc_path.read_text()
    print(check_images(text, image_path))
    print(fix_images(text, image_path))
