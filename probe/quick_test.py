
from publish.publication import (build_pubs, show_pubs)

from .models import Probe, TestResult


def quick_test():
    # print("No quick test defined")
    pubs()
    tests()
    return 'OK'


def pubs():
    # Do complete rebuild
    build_pubs(False, True)
    print(show_pubs())


def tests():
    print(f'{len(Probe.objects.all())} Tests available'  )
    print(f'{len(TestResult.objects.all())} Test Results available'  )
