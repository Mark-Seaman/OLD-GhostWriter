from csv import reader

from probe.tests_django import DjangoTest
from publish.publication import all_pubs, get_pub_info, list_publications


class PubDocTest(DjangoTest):
    fixtures = ["config/publish.json"]

    def test_all_docs(self):
        self.assertFiles('Documents', 2051, 2100)

    def test_doc_directories(self):
        data = '''Documents,2051,2080
Documents/seamansguide.com,114,114
Documents/seamanslog.com,380,390
Documents/markseaman.info,65
Documents/shrinking-world.com,490,500
Documents/shrinking-world.io,59
Documents/shrinking-world.org,3
Documents/spiritual-things.org,431
Documents/SHRINKING-WORLD-PUBS,480,510
'''
        for x in list(reader(data.splitlines())):
            # print(x)
            if x[2:]:
                self.assertFiles(x[0], int(x[1]), int(x[2]))
            else:
                self.assertFiles(x[0], int(x[1]), int(x[1]))

    def test_pub_list(self):
        self.assertRange(len(list_publications()), 18, 21)