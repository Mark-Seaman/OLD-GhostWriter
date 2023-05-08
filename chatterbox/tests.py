from pathlib import Path
from django.test import TestCase
from requests import get
from chatterbox.ai import do_gpt_task
from chatterbox.files import recursive_files
from chatterbox.pub_script import extract_outline, markdown_to_outline, pub_path, pub_script_command

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
        self.assertNumLines(self, response.text, min, max)

    def assertText(self, page, text):
        response = get(page)
        self.assertEqual(response.status_code, 200)
        self.assertIn(text, response.text)

    def assertNumLines(self, text, min, max):
        lines = len(text_lines(text))
        self.assertRange(lines, min, max, label=f"Lines in {text}")

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
        self.assertFiles(directory, 20, 40)

    def test_project(self):
        pub_script_command('project', ['GhostWriter','ghost'])
        pub = pub_path('GhostWriter')/'Pub'
        self.assertTrue(pub.exists())
        js = pub_path('GhostWriter')/'Pub/ghost.js'
        self.assertTrue(js.exists())
        ai = pub_path('GhostWriter')/'AI'
        self.assertTrue(ai.exists())

    def test_outliner(self):
        directory = pub_path('GhostWriter')
        doc = directory/'Pub/Chapter2.md'
        text = markdown_to_outline(doc.read_text())
        self.assertNumLines(text, 21, 22)
        text = extract_outline(text, '2.3')
        self.assertNumLines(text, 6, 6)
        # print(text)

    def test_chatter(self):
        output = 'GhostWriter/AI/Pub/Outline.md'  
        context = 'GhostWriter/AI/Pub/Persona.md'  
        content = 'GhostWriter/AI/Pub/TOC.md'  
        task = 'GhostWriter/AI/Pub/Outline.ai' 
        task = None   # Disable the AI API call
        print(do_gpt_task([output, task, context, content]))

