from datetime import datetime

from probe.tests_django import DjangoTest
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
# Build Pubs


class PubInputOutputTest(DjangoTest):
    def test_build_blogs(self):
        build_pubs()
        self.assertRange(len(Pub.objects.all()), 18, 20)
        num = len(Content.objects.all())
        self.assertRange(num, 1200, 1300, "Blog Contents")


# -----------------------
# Pub Fixture

class FixtureTest(DjangoTest):
    fixtures = ["config/publish.json"]

    def test_with_data(self):
        num = len(Content.objects.all())
        self.assertRange(num, 1200, 1300, "Content objects")

    def test_pub_list(self):
        self.assertRange(len(all_pubs()), 19, 21, 'Num Pubs')

    def test_book_list(self):
        self.assertRange(len(all_books()), 5, 5, 'Num Books')

    def test_blog_list(self):
        self.assertRange(len(all_blogs()), 5, 7, 'Num Blogs')
   
    def test_private_list(self):
        self.assertRange(len(all_privates()), 8, 9, 'Num Private Pubs')

    def test_pub_info(self):
        save_pub_info()
        text = concatonate('probe/pubs/*')
        self.assertNumLines(text, 3900, 4000)

    def test_rebuld_pubs(self):
        build_pubs(False, True)
        self.assertRange(len(Pub.objects.all()), 18, 21)
        self.assertRange(len(Content.objects.all()), 1200, 1300, "Content Nodes")

    def test_data_file(self):
        self.assertFalse(is_old("config/publish.json"), 'config/publish.json is old')

