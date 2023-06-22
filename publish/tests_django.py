from pathlib import Path
from django.test import TestCase
from requests import get

from publish.files import read_file
from publish.text import line_count, text_lines

NO_INTERNET = False

class DjangoTest(TestCase):

    def assertFiles(self, directory, min, max):
        num_files = len([f for f in Path(directory).rglob("*.md")])
        error = f"files in {directory}: {num_files} is not in range (min {min} and max {max})"
        # self.assertGreaterEqual(num_files, min, error)
        # self.assertLessEqual(num_files, max, error)
        self.assertRange(num_files,  min, max, error)

    def assertPage(self, page):
        if page.startswith('/'):
            response = self.client.get(page)
            text = response.content.decode('utf-8')
        else:
            if NO_INTERNET:
                print('\nNO_INTERNET\n')
                return
            else:
                response = get(page)
                text = response.text
        self.assertEqual(response.status_code, 200)
        return text


    def assertPageRedirect(self, page, url):
        if page.startswith('/'):
            response = self.client.get(page)
        else:
            if NO_INTERNET:
                print('\nNO_INTERNET\n')
                return
            else:
                response = get(page)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, url)


    def assertPageLines(self, page, min, max):
        self.assertNumLines(self.assertPage(page), min, max)

    def assertPageText(self, page, pattern=None):
        text = self.assertPage(page)
        if pattern:
            self.assertIn(pattern, text)
        return text

    def assertNumLines(self, text, min, max=1000, label='Lines of Text'):
        lines = line_count(text)
        self.assertRange(lines, min, max, label)

    def assertFileLines(self, path, min, max):
        self.assertNumLines(read_file(path), min, max)

    def assertRange(self, num, min, max=1000, label="Value"):
        error = f"{label} {num} is not in range (min {min} and max {max})"
        self.assertGreaterEqual(num, min, error)
        self.assertLessEqual(num, max, error)


    # def test_django_test(self):
        # self.assertTrue(True)
