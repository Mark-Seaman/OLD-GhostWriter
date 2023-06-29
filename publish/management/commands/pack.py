from django.core.management.base import BaseCommand
from os import environ, system
from os.path import exists, isdir, isfile
from pathlib import Path


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('command', nargs='*', type=str)

    def handle(self, *args, **options):

        command, pack = options.get('command')

        if command == 'open':
            print(f'PACK OPEN {pack}')
            home = Path(environ['HOME'])
            base = home / 'Archive'
            archive = base / f'.{pack}.opc'
            if not exists(archive) or not isfile(archive):
                print('File does not exist')
            else:
                system(f'mv {archive} {base}/package.zip && cd {base} && unzip package.zip && rm package.zip')
            if not exists(base / pack) or not isdir(base / pack):
                print('File not unpacked')
            if exists(base / 'package.zip'):
                print('File not deleted')

        if command == 'close':
            print(f'PACK CLOSE {pack}')
            home = Path(environ['HOME'])
            base = home / 'Archive'
            archive = base / f'.{pack}.opc'
            if not exists(base / pack) or not isdir(base / pack):
                print('Directory does not exist')
            system(f'cd {base} && zip -r package.zip {pack} && rm -fr {pack} && mv package.zip {archive}')
            if not exists(archive):
                print('File not packed')
            if exists(base / 'package.zip'):
                print('File not deleted')
