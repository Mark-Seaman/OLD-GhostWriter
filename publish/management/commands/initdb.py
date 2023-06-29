from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from publish.book import create_all_books, import_books
from publish.book_tools import show_book_content
from course.content import show_course_content
from course.import_export import import_all_courses
from probe.probe import reset_tests, run_tests


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("IMPORT BOOKS")
        create_test_user()
        import_books()
        show_book_content()
        import_all_courses()
        show_course_content()


def create_test_user():
    args = dict(username="seaman", email="me@here.com", password="secret")
    user = get_user_model().objects.filter(username="seaman")
    if user:
        user = user[0]
    else:
        user = get_user_model().objects.create_user(**args)
    return user, args


def initialize_database():
    import_all_courses()
    import_books()
    # import_tasks()
    reset_tests()
    run_tests()
