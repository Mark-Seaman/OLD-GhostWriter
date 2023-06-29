from csv import reader

from probe.tests_django import DjangoTest
from publish.publication import list_publications


class PubDocTest(DjangoTest):
    fixtures = ["config/publish.json"]

    def test_all_docs(self):
        self.assertFiles('Documents', 500, 2080)

    def test_doc_directories(self):
        data = '''Documents/SHRINKING-WORLD-PUBS,480,520'''
        for x in list(reader(data.splitlines())):
            # print(x)
            if x[2:]:
                self.assertFiles(x[0], int(x[1]), int(x[2]))
            else:
                self.assertFiles(x[0], int(x[1]), int(x[1]))

    def test_pub_list(self):
        self.assertRange(len(list_publications()), 4,20)