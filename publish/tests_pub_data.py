from datetime import datetime

from .tests_django import DjangoTest
from os.path import getmtime

from publish.days import is_old
from publish.files import concatonate

from .models import Content, Pub
from .publication import (all_blogs, all_books, all_privates, all_pubs,
                          build_pubs, get_pub_info, build_pubs, save_pub_info)


# -----------------------
# Pub Data Model

class PubDataTest(DjangoTest):

    # Pub Data Model
    def setup(self):
        blog1 = Pub.objects.create()

    def test_blog_add(self):
        blog1 = Pub.objects.create(
            name="Write", title="Authoring Tips", url="write")
        blog2 = Pub.objects.create(name="Tech", title="Pro Pub", url="tech")
        self.assertEqual(len(Pub.objects.all()), 2)

    def test_blog_detail(self):

        Pub.objects.create(name="Write", title="Authoring Tips", url="write")
        Pub.objects.create(name="Tech", title="Pro Pub", url="tech")
        blog1 = Pub.objects.get(name="Write")
        blog2 = Pub.objects.get(title="Pro Pub", url="tech")
        self.assertEqual(blog1.title, "Authoring Tips")
        self.assertEqual(blog1.url, "write")
        self.assertEqual(blog2.url, "tech")

    def test_blog_edit(self):

        Pub.objects.create(name="Write", title="Authoring Tips", url="write")
        Pub.objects.create(name="Tech", title="Pro Pub", url="tech")
        blog1 = Pub.objects.get(name="Write")
        blog2 = Pub.objects.get(title="Pro Pub", url="tech")
        blog1.title = "New Tips"
        blog1.url = "newurl"
        self.assertEqual(blog1.title, "New Tips")
        self.assertEqual(blog1.url, "newurl")
        self.assertEqual(blog2.url, "tech")


# -----------------------
# Pub Fixture

class FixtureTest(DjangoTest):
    fixtures = ["config/publish.json"]

    def test_with_data(self):
        num = len(Content.objects.all())
        self.assertRange(num, 213, 1300, "Content objects")

    def test_pub_list(self):
        self.assertRange(len(all_pubs()), 4, 21, 'Num Pubs')

    def test_book_list(self):
        self.assertRange(len(all_books()), 3, 5, 'Num Books')

    def test_blog_list(self):
        self.assertRange(len(all_blogs()), 0, 7, 'Num Blogs')
   
    def test_private_list(self):
        self.assertRange(len(all_privates()), 1, 9, 'Num Private Pubs')

    def test_pub_info(self):
        save_pub_info()
        text = concatonate('publish/*.py')
        self.assertNumLines(text, 3600, 4000)

    def test_rebuld_pubs(self):
        build_pubs(False, True)
        self.assertRange(len(Pub.objects.all()), 1, 5)
        self.assertRange(len(Content.objects.all()), 10, 300, "Content Nodes")

    def test_data_file(self):
        self.assertFalse(is_old("config/publish.json"), 'config/publish.json is old')

