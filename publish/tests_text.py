from pathlib import Path
from .tests_django import DjangoTest
from .files import concatonate, read_file, recursive_files, write_file
from .text import line_count, word_count


class TextFileTest(DjangoTest):
    
    def test_word_count(self):
        self.assertEqual(word_count("Hello world"), 2)
        self.assertEqual(word_count("  "), 1)
        self.assertEqual(word_count("  Hello   world  "), 2)
        self.assertEqual(word_count("Hello world"), 2)
        self.assertEqual(word_count("Hello \n\n world \n"), 2)

    def test_read_file(self):
        text = read_file('ReadMe.md')
        self.assertNumLines(text, 160)
        self.assertRange(word_count(text), 400, 600)

    def test_write_file(self):
        f = Path('Test.md')
        write_file(f, read_file('ReadMe.md'))
        text = read_file(f)
        self.assertNumLines(text, 160)
        f.unlink()

    def test_file_list(self):
        files = len(list(Path('publish').glob('**/*.py')))
        self.assertRange(files, 49, 51, f'files in publish python code file tree')

    def test_concatonate(self):
        text = concatonate('publish/**/*.py')
        self.assertNumLines(text, 3500, 5000, f'lines in Python files for probe file tree')

    