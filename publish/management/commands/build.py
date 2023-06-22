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
        usage = "usage:\n    Build Options: data, pubs"
        if x:
            if x[0] == "data":
                print("BUILD DATA")
                load_data()
                return
            elif x[0] == "pubs":
                print("BUILD PUBS")
                print(build_pubs())
                return
        print(usage)
