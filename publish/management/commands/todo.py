from django.core.management.base import BaseCommand
from traceback import format_exc

from task.todo import edit_todo_list


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            edit_todo_list()
        except:
            self.stdout.write(format_exc())


