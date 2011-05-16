import os
import sys

here = os.path.dirname(__file__)
base = os.path.dirname(here)
sys.path.insert(0, base)

# We can only import this after we adjust the paths
import pkg_resources

# Make absolutely sure we're testing *this* package, not
# some other installed package
pkg_resources.require('PasteDeploy')

