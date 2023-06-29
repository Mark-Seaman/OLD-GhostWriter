import subprocess
from pathlib import Path
from sys import version_info

from django.test import TestCase

from probe.models import Probe


class TestDataTest(TestCase):

    def setUp(self):
        self.test1 = dict(name='Files list', expected='Initial output 1', source='test.test_system.test_system_source')
        self.test2 = dict(name='Python code', expected='Initial output 2', source='test.test_system.test_python_source')

    def test_add_test(self):
        self.assertEqual(len(Probe.objects.all()), 0)
        Probe.create(**self.test1)
        x = Probe.objects.get(pk=1)
        self.assertEqual(x.source, self.test1['source'])
        self.assertEqual(len(Probe.objects.all()), 1)

    def test_test_edit(self):
        Probe.create(**self.test1)
        b = Probe.objects.get(pk=1)
        b.expected = self.test2['expected']
        b.source = self.test2['source']
        b.save()
        self.assertEqual(b.expected, self.test2['expected'])

    def test_test_delete(self):
        Probe.objects.create(**self.test1)
        b = Probe.objects.get(pk=1)
        b.delete()
        self.assertEqual(len(Probe.objects.all()), 0)

    
class PythonEnvironmentTest(TestCase):
    def test_python_environment(self):
        requirements = '''aiohttp==3.8.4
aiosignal==1.3.1
asgiref==3.5.2
async-timeout==4.0.2
attrs==23.1.0
autopep8==2.0.1
beautifulsoup4==4.11.1
black==22.10.0
certifi==2022.6.15
charset-normalizer==2.0.12
click==8.1.3
dj-database-url==0.5.0
Django==4.0.5
django-crispy-forms==1.14.0
frozenlist==1.3.3
gunicorn==20.1.0
idna==3.3
importlib-metadata==6.0.0
Markdown==3.3.7
multidict==6.0.4
mypy-extensions==0.4.3
numpy==1.24.3
openai==0.27.5
pandas==2.0.1
pathspec==0.9.0
Pillow==9.5.0
platformdirs==2.5.2
psycopg2-binary==2.9.6
pycodestyle==2.10.0
python-dateutil==2.8.2
python-dotenv==1.0.0
pytz==2022.1
requests==2.28.0
six==1.16.0
soupsieve==2.3.2.post1
sqlparse==0.4.2
tabulate==0.9.0
toml==0.10.2
tomli==2.0.1
toot==0.31.0
tqdm==4.65.0
typing_extensions==4.6.3
tzdata==2023.3
urllib3==1.26.9
urwid==2.1.2
wcwidth==0.2.5
whitenoise==6.2.0
yarl==1.9.2
zipp==3.12.0
'''
        self.assertEqual(Path('requirements.txt').read_text(),requirements)

    def test_python_packages(self):
        expected_packages = [
            'Django',
            'requests',
            'numpy',
        ]
        process = subprocess.Popen(['pip', 'freeze'], stdout=subprocess.PIPE)
        output, _ = process.communicate()
        installed_packages = output.decode('utf-8')
        # installed_packages = output.decode('utf-8').strip().split('\n')
        for package in expected_packages:
            self.assertIn(package, installed_packages)

    def test_python_version(self):
        v = version_info[:2]
        self.assertTrue(v == (3, 11) or v == (3, 10))
