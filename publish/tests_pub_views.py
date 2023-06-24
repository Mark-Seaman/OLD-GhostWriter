from django.test import TestCase

from .tests_django import DjangoTest
from publish.publication import pub_redirect

from .models import Content, Pub

# -----------------------
# Local Blog Pub Pages

local_host = 'http://localhost:8002'


class BlogPageTest(DjangoTest):
    def test_home_page(self):
        page = f'{local_host}/journey'
        self.assertPageLines(page, 140, 200)

    def test_pub_redirect(self):
        redirects = (("shrinking-world.com", None, None, '/publish/book'),
                     ("seamansguide.com", "journey","Index.md", '/journey/Index.md'),
                     ("seamansguide.com", None, "journey", '/publish/book'),
                     ("seamansguide.com", "journey", None, '/journey'),
                     ("seamansguide.com", None, None, '/publish/book'),
                     ("seamanslog.com", None, None, '/sampler/today'),
                     ("seamanfamily.org", None, None, '/family/Index.md'),
                     ("seamanslog.com", None, None, '/sampler/today'),
                     ("spiritual-things.org", None, None, '/spiritual/today'),
                     ("markseaman.org", None, None, '/marks/ContactMe'),
                     ("markseaman.info", None, None, '/private'),
                     ("localhost:8000", None, None, '/publish/book'))
        for r in redirects:
            self.assertEqual(pub_redirect(r[0], r[1], r[2]), r[3], f'FAILED: {r}')


# -----------------------
# Local Book Pub Pages

class BookPageTest(DjangoTest):
    def test_book_list_page(self):
        page = f'{local_host}/publish/book'
        self.assertPage(page)
        # self.assertPageLines(page, 190, 244, page)

    def test_book_journey_page(self):
        page = f'{local_host}/journey'
        self.assertPageLines(page, 190, 200)
