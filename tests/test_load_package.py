import importlib.metadata
from pprint import pprint
import sys


def test_load_package():
    print('Path:')
    pprint(sys.path)
    importlib.metadata.distribution('FakeApp')
