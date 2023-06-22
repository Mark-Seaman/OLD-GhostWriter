from pathlib import Path

from publish.files import create_directory

from .pub_dev import (doc_html, doc_list, doc_text, doc_title, pub_list,
                      pub_path, pub_view_data, read_pub_doc)
from .tests_django import DjangoTest
from .writer_script import pub_path, pub_script


class GhostTest(DjangoTest):

    def test_runs(self):
        self.assertEqual(3, 3)

    def test_create_directory(self):
        x = '/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/GhostWriter/AI/test/test/delete-me'
        create_directory(x)
        self.assertTrue(Path(x).exists())

    def test_pub_files(self):
        directory = pub_path('GhostWriter')
        self.assertEqual(str(
            directory), '/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/GhostWriter/AI')
        self.assertFiles(directory, 14, 40)

    def test_project(self):
        pub_script(['project', 'GhostWriter'])
        js = (pub_path('GhostWriter').parent)/'pub.json'
        self.assertFileLines(js, 20, 20)

    def test_chapter(self):
        pub_script(['chapter', 'GhostWriter', 'GhostWriter'])
        self.assertFileLines(
            pub_path('GhostWriter', 'GhostWriter', 'B-Ideas.txt'), 7, 24)
        self.assertFileLines(
            pub_path('GhostWriter', 'GhostWriter', 'B-Ideas.ai'), 12, 24)

    def test_doc(self):
        pub_script(
            ['doc', 'GhostWriter', 'GhostWriter', 'B-Ideas.md'], False)

    # def test_outline(self):
    #     text = pub_script_command(
    #         'outline', ['GhostWriter', 'Micropublishing', 'C-Outline.md'])
    #     self.assertNumLines(text, 6, 6)
    #     # print(text)

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
        self.assertEqual(
            str(pub_path('GhostWriter', 'Chapter1', 'Chapter1.md')), x)

    def test_num_pubs(self):
        pubs1 = len(pub_list())
        pubs2 = len(pub_view_data()['pubs'])
        self.assertEqual(pubs1, pubs2)
        self.assertRange(pubs2, 15, 16)

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
        text = self.assertPageText( 'http://shrinking-world.com', 210, 250, 'html')

    def test_pub_list_view(self):
        text = self.assertPageText('/writer/', 180, 200, 'html')

    def test_pub_view(self):
        text = self.assertPageText('/writer/GhostWriter', 240, 260, 'html')

    def test_chapter_view(self):
        text = self.assertPageText(
            '/writer/GhostWriter/WritersGuide', 240, 310, 'html')

    def test_doc_view(self):
        text = self.assertPageText(
            '/writer/GhostWriter/WritersGuide/Chapter1.md', 290, 310, 'html')

    def test_ai_view(self):

        # Skip the Call to Open AI API
        # response = self.client.get('/GhostWriter/Pub/Haiku.md/ai')
        # self.assertEqual(response.status_code, 302)

        self.assertPageText('/writer/GhostWriter/Pub/Haiku.md', 140, 300, 'Haiku')


# class DocumentModelTest(DjangoTest):
#     def setUp(self):
#         self.document = Document.objects.create(
#             pub='Publication',
#             chapter='Chapter 1'
#         )

#     def test_document_str_representation(self):
#         self.assertEqual(str(self.document), 'Publication - Chapter 1')
