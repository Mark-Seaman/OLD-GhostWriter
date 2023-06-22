from django.core.management.base import BaseCommand
from course.teach import teaching_prep

from publish.write import write_blog, write_masto, write_review, write_tech, write_words


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("command", nargs="*", type=str)

    def show_usage(self):
        self.stdout.write("usage: teach [outline|greenhouse]")

    def handle(self, *args, **options):
        x = options.get("command")
        text = teaching_prep(x)
        if text:
            self.stdout.write(text)
