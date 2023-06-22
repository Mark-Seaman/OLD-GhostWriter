from django.test import TestCase

from .tests_django import DjangoTest
from publish.publication import pub_redirect

from .models import Content, Pub

# -----------------------
# Local Blog Pub Pages


class BlogPageTest(DjangoTest):
    def test_home_page(self):
        page = "http://localhost:8000/"
        self.assertPageLines(page, 140, 150)

    def test_bouncer_page(self):
        page = "/11"
        url = "https://shrinking-world.com/marks/ContactMe"
        self.assertPageRedirect(page, url)
        page = "/81"
        url = "https://seamansguide.com/journey"
        self.assertPageRedirect(page, url)
        page = "http://localhost:8000/sampler"
        self.assertPageText(page, "Seaman&#x27;s Log")

    def test_pub_redirect(self):
        redirects = (("shrinking-world.com", None, None, '/publish/book'),
                     ("seamansguide.com", "journey","Index.md", '/journey/Index.md'),
                     ("seamansguide.com", None, "journey", '/publish/book'),
                     ("seamansguide.com", "journey", None, '/private'),
                     ("seamansguide.com", None, None, '/publish/book'),
                     ("seamanslog.com", None, None, '/sampler/today'),
                     ("seamanfamily.org", None, None, '/family/Index.md'),
                     ("seamanslog.com", None, None, '/sampler/today'),
                     ("spiritual-things.org", None, None, '/spiritual/today'),
                     ("markseaman.org", None, None, '/marks/ContactMe'),
                     ("markseaman.info", None, None, '/private'),
                     ("localhost:8000", None, None, '/private'),)
        for r in redirects:
            self.assertEqual(pub_redirect(r[0], r[1], r[2]), r[3], f'FAILED: {r}')
    
    def test_sampler_page(self):
        page = "http://localhost:8000/sampler"
        self.assertPageText(page, "Seaman&#x27;s Log")

    def test_index_page(self):
        page = "http://localhost:8000/sampler/Index"
        self.assertPageText(page, "Seaman&#x27;s Log")
        page = "http://localhost:8000/sampler/Index.md"
        self.assertPageText(page, "Seaman&#x27;s Log")

    def test_spirit_page(self):
        page = "http://localhost:8000/spiritual"
        self.assertPageText(page, "Meditations")

    def test_write_page(self):
        page = "http://localhost:8000/write"
        self.assertPageText(page, "Writer's Block")



# -----------------------
# Local Book Pub Pages

class BookPageTest(DjangoTest):
    def test_book_list_page(self):
        page = "http://localhost:8000/publish/book"
        self.assertPageLines(page, 200, 244)

    def test_book_journey_page(self):
        page = "http://localhost:8000/journey"
        self.assertPageLines(page, 190, 200)
