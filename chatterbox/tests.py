from pathlib import Path
from django.test import TestCase
from requests import get

from publish.pub import pub_path
from publish.text import text_lines

from .pub_script import extract_outline, markdown_to_outline, pub_script_command
from .tests_django import DjangoTest


class GhostTest(DjangoTest):

    def test_runs(self):
        self.assertEqual(3, 3)

    def test_pub_files(self):
        directory = pub_path('GhostWriter')
        self.assertEqual(str(
            directory), '/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/GhostWriter/AI')
        self.assertFiles(directory, 14, 40)

    def test_project(self):
        x = pub_script_command('project', ['GhostWriter', 'ghost'])
        self.assertEqual(
            x, '/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/GhostWriter/AI')
        pub = pub_path('GhostWriter', 'Pub')
        self.assertTrue(pub.exists())
        js = pub_path('GhostWriter')/'ghost.json'
        self.assertTrue(js.exists())
        ai = pub_path('GhostWriter')/'AI'
        self.assertTrue(ai.exists())

    def test_chapter(self):
        text = pub_script_command('chapter', ['GhostWriter', 'Chapter3'])
        self.assertFileLines(
            pub_path('GhostWriter', 'Chapter3', '1-Idea.txt'), 7, 24)
        self.assertFileLines(
            pub_path('GhostWriter', 'Chapter3', '1-Idea.ai'), 23, 24)

    def test_outline(self):
        text = pub_script_command(
            'outline', ['GhostWriter', 'Chapter2', 'Chapter2.md', '2.1'])
        y = '/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/GhostWriter/AI/Chapter2/Chapter2.md'
        self.assertNumLines(text, 6, 6)
        # print(text)

    # def test_chatter(self):
    #     output = 'GhostWriter/AI/Pub/Outline.md'
    #     context = 'GhostWriter/AI/Pub/Persona.md'
    #     content = 'GhostWriter/AI/Pub/TOC.md'
    #     task = 'GhostWriter/AI/Pub/Outline.ai'
    #     task = None   # Disable the AI API call
    #     answer = "Prompt: output=GhostWriter/AI/Pub/Outline.md task=None prompt=None content,context=['GhostWriter/AI/Pub/Persona.md', 'GhostWriter/AI/Pub/TOC.md']"
    #     self.assertEqual(do_gpt_task([output, task, context, content]), answer)

    # def test_chatgpt(self):
    #     x = transform_prompt('write a haiku about trees')
    #     y = ''
    #     # print(x)
    #     self.assertNumLines(x, 3, 3)

    # def test_outline_expander(self):
    #     print(pub_script_command(
    #         'expand', ['GhostWriter', 'Chapter2', 'Chapter2.md']))
