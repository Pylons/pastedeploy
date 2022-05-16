from pprint import pprint
import sys

import pkg_resources


def test_load_package():
    print('Path:')
    pprint(sys.path)
    print(pkg_resources.require('FakeApp'))
