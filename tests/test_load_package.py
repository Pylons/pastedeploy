import importlib.metadata
import sys
from pprint import pprint


def test_load_package():
    print('Path:')
    pprint(sys.path)
    importlib.metadata.distribution('FakeApp')
