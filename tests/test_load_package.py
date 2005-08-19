import sys, os
import pkg_resources
import site
from pprint import pprint

def test_load_package():
    print 'Path:'
    pprint(sys.path)
    print pkg_resources.require('FakeApp')
    
