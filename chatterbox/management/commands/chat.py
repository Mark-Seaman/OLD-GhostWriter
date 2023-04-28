from django.core.management.base import BaseCommand

from chatterbox.chatter import chat


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("command", nargs="*", type=str)

    def show_usage(self):
        self.stdout.write("usage: chat input output")

    def handle(self, *args, **options):
        x = options.get("command")
        text = chat(x[0], x[1])
        if text:
            self.stdout.write(text)
