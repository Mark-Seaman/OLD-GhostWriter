from os import environ

from django.core.management.base import BaseCommand
from os.path import exists, isdir, join
from traceback import format_exc

from publish.shell import shell


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("files", nargs="*", type=str)

    def handle(self, *args, **options):
        try:
            # print(options['files'])
            edit_file(options["files"])
        except:
            self.stdout.write("** edit Exception (%s) **" % " ".join(options["files"]))
            self.stdout.write(format_exc())


def file_args(args):
    directory = environ["p"]
    if exists(args[0]) and isdir(args[0]):
        # print(f'Directory:  {args[0]}')
        directory = args[0]
        args = args[1:]
    files = ""
    for f in args:
        d = join(directory, f)
        if exists(d):
            files += join(directory, f) + " "
        elif exists(f):
            files += f + " "
        else:
            files += join(directory, "", f) + " "
    # print(f"EDIT (dir={directory}, files={files})")
    return files


def edit_file(args):
    if isinstance(args, list):
        files = file_args(args)
    else:
        files = args
    exe_path = "subl"
    command = f"{exe_path} {files}"
    print(command)
    shell(command)
