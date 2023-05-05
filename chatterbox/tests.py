from pathlib import Path
from django.test import TestCase
from requests import get
from chatterbox.files import recursive_files
from chatterbox.pub_script import pub_path, pub_script_command

from chatterbox.text import text_lines


class DjangoTest(TestCase):

    def assertFiles(self, directory, min, max):
        num_files = len([f for f in Path(directory).rglob("*.md")])
        error = f"files in {directory}: {num_files} is not in range (min {min} and max {max})"
        self.assertGreaterEqual(num_files, min, error)
        self.assertLessEqual(num_files, max, error)

    def assertLines(self, page, min, max):
        response = get(page)
        self.assertEqual(response.status_code, 200)
        lines = len(text_lines(response.text))
        self.assertRange(lines, min, max, label=f"Lines in {page}")

    def assertText(self, page, text):
        response = get(page)
        self.assertEqual(response.status_code, 200)
        self.assertIn(text, response.text)

    def assertRange(self, num, min, max, label="Value"):
        error = f"{label} {num} is not in range (min {min} and max {max})"
        self.assertGreaterEqual(num, min, error)
        self.assertLessEqual(num, max, error)


class GhostTest(DjangoTest):

    def test_runs(self):
        self.assertEqual(3, 3)

    def test_pub_files(self):
        directory = pub_path('GhostWriter')
        self.assertEqual(str(directory), '/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/GhostWriter')
        self.assertFiles(directory, 20, 21)

    def test_project(self):
        pub_script_command('project', ['GhostWriter','ghost'])
        pub = pub_path('GhostWriter')/'Pub'
        self.assertTrue(pub.exists())
        js = pub_path('GhostWriter')/'Pub/ghost.js'
        self.assertTrue(js.exists())
        ai = pub_path('GhostWriter')/'AI'
        self.assertTrue(ai.exists())
