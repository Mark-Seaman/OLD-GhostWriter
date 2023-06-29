from pathlib import Path

from probe.probe import check_files
from publish.text import char_fix_files

docs = Path("Documents")


def test_documents_images():
    return check_files(Path("static") / "images", 550, 570)


def test_documents_fix_chars():
    return char_fix_files("Documents")

