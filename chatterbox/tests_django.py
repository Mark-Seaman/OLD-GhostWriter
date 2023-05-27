from pathlib import Path
from django.test import TestCase
from requests import get

from publish.files import read_file
from publish.text import text_lines


class DjangoTest(TestCase):

    def assertFiles(self, directory, min, max):
        num_files = len([f for f in Path(directory).rglob("*.md")])
        error = f"files in {directory}: {num_files} is not in range (min {min} and max {max})"
        self.assertGreaterEqual(num_files, min, error)
        self.assertLessEqual(num_files, max, error)

    def assertLines(self, page, min, max):
        response = get(page)
        self.assertEqual(response.status_code, 200)
        self.assertNumLines(self, response.text, min, max)

    def assertText(self, page, text):
        response = get(page)
        self.assertEqual(response.status_code, 200)
        self.assertIn(text, response.text)

    def assertNumLines(self, text, min, max):
        lines = len(text_lines(text))
        self.assertRange(lines, min, max, label=f"Lines in {text}")

    def assertFileLines(self, path, min, max):
        self.assertNumLines(read_file(path), min, max)

    def assertRange(self, num, min, max, label="Value"):
        error = f"{label} {num} is not in range (min {min} and max {max})"
        self.assertGreaterEqual(num, min, error)
        self.assertLessEqual(num, max, error)

    # def test_django_test(self):
    #     self.assertTrue(True)
