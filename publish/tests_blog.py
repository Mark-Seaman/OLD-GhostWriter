from .tests_pub_views import DjangoTest


class RemoteBlogPagesTest(DjangoTest):
    def test_blog_seamanslog(self):
        self.assertPageLines("https://seamanslog.com", 100, 120)

    def test_blog_spirit(self):
        self.assertPageLines("https://spiritual-things.org", 100, 121)

    def test_blog_mark_seaman(self):
        self.assertPageLines("https://markseaman.org", 120, 170)


class BlogFilesTest(DjangoTest):
    def test_seamanslog(self):
        self.assertFiles("Documents/seamanslog.com", 380, 400)

    def test_spiritlog(self):
        self.assertFiles("Documents/spiritual-things.org/daily", 370, 380)

 