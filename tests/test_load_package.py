from pprint import pprint
import sys


def test_load_package():
    from paste.deploy.util import importlib_metadata
    print('Path:')
    pprint(sys.path)
    importlib_metadata.distribution('FakeApp')
