from pathlib import Path
from django.test import TestCase
from requests import get

from publish.pub import pub_path

from .ai import do_gpt_task
from .pub_script import pub_script_command
from .tests_django import DjangoTest


class GhostTest(DjangoTest):

    def test_runs(self):
        self.assertEqual(3, 3)

    def test_pub_files(self):
        directory = pub_path('GhostWriter')
        self.assertEqual(str(directory), '/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/GhostWriter/AI')
        self.assertFiles(directory, 14, 40)

    def test_project(self):
        pub_script_command('project', ['GhostWriter','ghost'])
        pub = pub_path('GhostWriter')/'Pub'
        self.assertTrue(pub.exists())
        js = pub_path('GhostWriter')/'Pub/ghost.js'
        self.assertTrue(js.exists())
        ai = pub_path('GhostWriter')/'AI'
        self.assertTrue(ai.exists())

    # def test_outliner(self):
    #     directory = pub_path('GhostWriter')
    #     doc = directory/'Chapter2/Chapter2.md'
    #     text = markdown_to_outline(doc.read_text())
    #     self.assertNumLines(text, 21, 22)
    #     text = extract_outline(text, '2.3')
    #     self.assertNumLines(text, 6, 6)
    #     # print(text)

    # def test_chatter(self):
        output = 'GhostWriter/AI/Pub/Outline.md'  
        context = 'GhostWriter/AI/Pub/Persona.md'  
        content = 'GhostWriter/AI/Pub/TOC.md'  
        task = 'GhostWriter/AI/Pub/Outline.ai' 
        task = None   # Disable the AI API call
        answer = "Prompt: output=GhostWriter/AI/Pub/Outline.md task=None prompt=None content,context=['GhostWriter/AI/Pub/Persona.md', 'GhostWriter/AI/Pub/TOC.md']"
        self.assertEqual(do_gpt_task([output, task, context, content]), answer)

