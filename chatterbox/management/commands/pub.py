from django.core.management.base import BaseCommand

from chatterbox.pub_script import pub_script_command


'''
Writer Script

Examples:
- project SoftwareEngineering
- chapter SoftwareEngineering 08
- create  SoftwareEngineering 08 from 03.md Outline.md
- publish SoftwareEngineering 08
- edit SoftwareEngineering 08

'''

class Command(BaseCommand):
    help = 'Execute a script that is passed as a list of words.'

    def add_arguments(self, parser):
        parser.add_argument('command_args', nargs='+', type=str)

    def handle(self, *args, **options):
        command_args = options['command_args']
        command = command_args[0]
        args = command_args[1:]
        output = pub_script_command(command, args)
        self.stdout.write(output)