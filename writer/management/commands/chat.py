from django.core.management.base import BaseCommand

from writer.ai import do_gpt_task


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("command", nargs="*", type=str)

    def show_usage(self):
        self.stdout.write("usage: output task content context")

    def handle(self, *args, **options):
        text = do_gpt_task(options.get("command"))
        if text:
            self.stdout.write(text)
