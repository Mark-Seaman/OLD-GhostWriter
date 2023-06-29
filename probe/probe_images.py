from pathlib import Path

from publish.document import doc_text
from publish.publication import get_pub


# def test_blog_images():
#     return verify_blog_images()


# def test_book_images():
#     return verify_book_images()


# def test_course_images():
#     return verify_course_images()


# def test_textbook_images():
#     return verify_textbook_images()


def test_image_pages():
    doc_path = Path(f"Documents/Shrinking-World-Pubs/journey/Pub")
    pub = get_pub('journey')
    # settings = read_json(pub_json_path(pub.name, pub.doc_path))
    # settings = read_json("static/js/journey.json")
    image_path = pub.image_path
    return doc_text(doc_path / "JFK.md", image_path) + doc_text(
        doc_path / "MushroomCloud.md", image_path
    )
