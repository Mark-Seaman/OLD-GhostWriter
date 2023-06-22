from os import system

from django.core.management.base import BaseCommand

from probe.probe import accept_results, reset_tests, run_tests, test_results
from probe.quick_test import quick_test


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('command', nargs='*', type=str)

    def handle(self, *args, **options):
        command = options.get('command')[0]
        self.level = options.get('command')[1:]
        if command == 'run':
            print('TEST RUN')
            self.run_tests_level()

        if command == 'like':
            print('TEST LIKE')
            accept_results()

        if command == 'reset':
            print('TEST RESET')
            reset_tests()

        if command == 'results':
            print('TEST results')
            test_results()

        if command == 'quick':
            print("QUICK TEST")
            print(quick_test())

    def run_tests_level(self):
        level = int(self.level[0] if self.level else '0')
        if level >= 1:
            print('Django Tests')
            system('python manage.py test')
        if level >= 2 or level == 0:
            print('Probe Tests')
            run_tests()
            test_results()
