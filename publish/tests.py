from os import getenv
from pathlib import Path
from chatterbox.pub_script import pub_path
from chatterbox.tests_django import DjangoTest
from publish.pub import doc_html, doc_list, doc_text, doc_title, list_pubs, read_pub_doc

class PubTest(DjangoTest):

    def test_pub_root(self):
        x = Path('/Users/seaman/Hammer/Documents/Shrinking-World-Pubs')
        y = pub_path()
        self.assertEqual(y, x)

    def test_num_pubs(self):
        self.assertEqual(len(list_pubs()), 11)

    def test_doc_path(self):
        
        x = Path('/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/GhostWriter/Chapter1.md')
        y = pub_path('GhostWriter/Chapter1.md')
        self.assertEqual(y, x)
        
    def test_load_doc(self):
        x = '# Chapter 1 - Introduction'
        y = read_pub_doc('GhostWriter/Chapter1.md')[:26]
        self.assertEqual(y, x)

    def test_doc_title(self):
        x = 'Chapter 1 - Introduction'
        y = doc_title('GhostWriter/Chapter1.md')
        self.assertEqual(y, x)

    def test_doc_text(self):
        x = '    1.1. Purpose of '
        y = doc_text('GhostWriter/Chapter1.md')[:20]
        self.assertEqual(y, x)

    def test_doc_list(self):
        x = 3
        y = doc_list('GhostWriter')
        self.assertEqual(len(y), x)

    def test_doc_html(self):
        text = doc_html('GhostWriter/Chapter1.md')
        self.assertNumLines(text, 128, 130)
