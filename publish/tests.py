from os import getenv
from pathlib import Path

from chatterbox.tests_django import DjangoTest

from .models import Document
from .pub import chapter_list, doc_html, doc_list, doc_text, doc_title, pub_path, list_pubs, pub_view_data, read_pub_doc


def list_files(pub, glob):
    files = [f.name for f in pub_path(pub).glob(glob)]
    return files


def ghost_writer_files(glob):
    return len(list_files('GhostWriter', glob))


def ghost_writer_chapters():
    chapters = pub_view_data(pub='GhostWriter')['chapters']
    return len(chapters)


class PubTest(DjangoTest):

    def test_pub_path(self):
        x = Path('/Users/seaman/Hammer/Documents/Shrinking-World-Pubs')
        y = pub_path()
        self.assertEqual(y, x)

        x = Path('/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/GhostWriter/AI')
        y = pub_path('GhostWriter')
        self.assertEqual(y, x)

        x = Path(
            '/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/GhostWriter/AI/Chapter1')
        y = pub_path('GhostWriter', 'Chapter1')
        self.assertEqual(y, x)

        x = Path(
            '/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/GhostWriter/AI/Chapter1/Chapter1.md')
        y = pub_path('GhostWriter', 'Chapter1', 'Chapter1.md')
        self.assertEqual(y, x)

    def test_num_pubs(self):
        x = 1
        pubs = list_pubs()
        self.assertEqual(len(pubs), x)

        pubs = pub_view_data()['pubs']
        self.assertEqual(len(pubs), x)

    def test_doc_files(self):
        self.assertEqual(ghost_writer_files('*/*.md'), 25)

    def test_ai_files(self):
        self.assertEqual(ghost_writer_files('*/*.ai'), 19)

    def test_txt_files(self):
        self.assertEqual(ghost_writer_files('*/*.txt'), 14)

    def test_chapters(self):
        chapters = pub_view_data(pub='GhostWriter')['chapters']
        self.assertEqual(len(chapters), 7)

    def test_doc_list(self):
        y = doc_list('GhostWriter', 'Chapter1')
        self.assertEqual(len(y), 6)

    def test_load_doc(self):
        x = '# Chapter 1 - Introduction'
        y = read_pub_doc('GhostWriter', 'Chapter1', 'Chapter1.md')[:26]
        self.assertEqual(y, x)

        x = pub_view_data(pub='GhostWriter', chapter='Chapter1',
                          doc='Chapter1.md')['text'][:26]
        self.assertEqual(y, x)

    def test_doc_title(self):
        x = 'Chapter 1 - Introduction'
        y = doc_title('GhostWriter', 'Chapter1', 'Chapter1.md')
        self.assertEqual(y, x)

    def test_doc_text(self):
        x = '    1.1. Purpose of '
        y = doc_text('GhostWriter', 'Chapter1', 'Chapter1.md')[:20]
        self.assertEqual(y, x)

    def test_doc_html(self):
        html = doc_html('GhostWriter', 'Chapter1', 'Chapter1.md')
        self.assertNumLines(html, 128, 130)
        html = pub_view_data(
            pub='GhostWriter', chapter='Chapter1', doc='Chapter1.md')['html']
        self.assertNumLines(html, 128, 130)


class DocumentModelTest(DjangoTest):
    def setUp(self):
        self.document = Document.objects.create(
            pub='Publication',
            chapter='Chapter 1'
        )

    def test_document_str_representation(self):
        self.assertEqual(str(self.document), 'Publication - Chapter 1')
