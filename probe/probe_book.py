from pathlib import Path

from publish.publication import all_books

from .probe import check_files


book1 = Path("Documents") / "Shrinking-World-Pubs"
book2 = Path("Documents") / "seamansguide.com"


def test_book_journey():
    return check_files(book1 / "journey", 30, 70)


def test_book_poem():
    return check_files(book1 / "poem", 70, 100)


def test_book_leverage():
    return check_files(book2 / "leverage", 39, 46)


def test_book_webapps():
    return check_files(book2 / "webapps", 130, 140)


def test_book_quest():
    return check_files(book1 / "quest", 60, 70)
