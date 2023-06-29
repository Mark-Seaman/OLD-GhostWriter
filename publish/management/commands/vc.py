from traceback import format_exc

from django.core.management.base import BaseCommand

from publish.vc import vc_command

# ------------------------------
# Command Interpreter


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("script", nargs="+", type=str)

    def handle(self, *args, **options):
        try:
            vc_command(options["script"])
        except:
            self.stdout.write("** tst Exception (%s) **" %
                              " ".join(options["script"]))
            self.stdout.write(format_exc())
