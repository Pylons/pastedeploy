from pprint import pprint
import pkg_resources
import sys


def test_load_package():
    print('Path:')
    pprint(sys.path)
    print(pkg_resources.require('FakeApp'))
