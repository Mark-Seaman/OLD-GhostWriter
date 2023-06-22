from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from publish.import_export import load_data
from publish.publication import build_pubs
from publish.seamanslog import review_file


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("command", nargs="*", type=str)

    def handle(self, *args, **options):
        x = options.get("command")
        if not x:
            print(
                """Build Options: courses, data, webapps, images, logos, review tasks"""
            )
            return

        cmd = x[0]
        if cmd == "data":
            print("BUILD DATA")
            load_data()
        elif cmd == "pubs":
            print("BUILD PUBS")
            print(build_pubs())
        elif cmd == "review":
            review_file()
        elif cmd == "user":
            get_user_model().objects.get(username="seaman").delete()
            user_args = dict(
                username="seaman",
                email="mark.seaman@shrinking-world.com",
                password="MS1959-sws",
            )
            get_user_model().objects.create_user(**user_args)
        elif cmd == "webapps":
            print("BUILD WEB APPS BOOK")
            generate_textbook()
        else:
            print(
                """Build Options: books, courses, data, webapps, images, logos, tasks"""
            )
