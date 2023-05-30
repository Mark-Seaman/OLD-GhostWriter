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
        self.assertEqual(pub_path(), x)

        x = Path('/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/GhostWriter/AI')
        self.assertEqual(pub_path('GhostWriter'), x)

        x = '/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/GhostWriter/AI/Chapter1'
        self.assertEqual(str(pub_path('GhostWriter', 'Chapter1')), x)

        x = '/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/GhostWriter/AI/Chapter1/Chapter1.md'
        self.assertEqual(str(pub_path('GhostWriter', 'Chapter1', 'Chapter1.md')), x)

    def test_num_pubs(self):
        x = 1
        pubs = list_pubs()
        self.assertEqual(len(pubs), x)

        pubs = pub_view_data()['pubs']
        self.assertEqual(len(pubs), x)

    def test_doc_files(self):
        self.assertRange(ghost_writer_files('*/*.md'), 28, 36)

    def test_ai_files(self):
        self.assertRange(ghost_writer_files('*/*.ai'), 20, 39)

    def test_txt_files(self):
        self.assertRange(ghost_writer_files('*/*.txt'), 15, 18)

    def test_chapters(self):
        chapters = pub_view_data(pub='GhostWriter')['chapters']
        self.assertRange(len(chapters), 7, 9)

    def test_doc_list(self):
        y = doc_list('GhostWriter', 'WritersGuide')
        self.assertEqual(len(y), 6)

    def test_load_doc(self):
        x = '# Chapter 1 - Introduction'
        y = read_pub_doc('GhostWriter', 'WritersGuide', 'Chapter1.md')[:26]
        self.assertEqual(y, x)

        x = pub_view_data(pub='GhostWriter', chapter='WritersGuide',
                          doc='Chapter1.md')['text'][:26]
        self.assertEqual(y, x)

    def test_doc_title(self):
        x = 'Chapter 1 - Introduction'
        y = doc_title('GhostWriter', 'WritersGuide', 'Chapter1.md')
        self.assertEqual(y, x)

    def test_doc_text(self):
        x = '    1.1. Purpose of '
        y = doc_text('GhostWriter', 'WritersGuide', 'Chapter1.md')[:20]
        self.assertEqual(y, x)

    def test_doc_html(self):
        html = doc_html('GhostWriter', 'WritersGuide', 'Chapter1.md')
        self.assertNumLines(html, 128, 130)
        html = pub_view_data(
            pub='GhostWriter', chapter='WritersGuide', doc='Chapter1.md')['html']
        self.assertNumLines(html, 128, 130)


class DocumentViewTest(DjangoTest):
    def test_web_page(self):
        text = self.assertPageText('http://shrinking-world.com', 176, 176, 'html')

    def test_pub_list_view(self):
        text = self.assertPageText('/', 69, 69, 'html')

    def test_pub_view(self):
        text = self.assertPageText('/GhostWriter', 118, 130, 'html')

    def test_chapter_view(self):
        text = self.assertPageText('/GhostWriter/WritersGuide', 150, 170, 'html')

    def test_doc_view(self):
        text = self.assertPageText('/GhostWriter/WritersGuide/Chapter1.md', 360, 380, 'html')

    def test_ai_view(self):

        # Skip the Call to Open AI API
        # response = self.client.get('/GhostWriter/Pub/Haiku.md/ai')
        # self.assertEqual(response.status_code, 302)

        self.assertPageText('/GhostWriter/Pub/Haiku.md', 200, 300, 'Haiku')

    
# class DocumentModelTest(DjangoTest):
#     def setUp(self):
#         self.document = Document.objects.create(
#             pub='Publication',
#             chapter='Chapter 1'
#         )

#     def test_document_str_representation(self):
#         self.assertEqual(str(self.document), 'Publication - Chapter 1')
