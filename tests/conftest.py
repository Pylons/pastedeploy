import os
import sys

here = os.path.dirname(__file__)
base = os.path.dirname(here)
fake_packages = os.path.join(here, 'fake_packages')
sys.path.append(fake_packages)

# We can only import this after we adjust the paths
import pkg_resources

# Make absolutely sure we're testing *this* package, not
# some other installed package
sys.path.insert(0, base)
#pkg_resources.require('Paste-Deploy')

# This is where applications we test go; these applications
# are only used for testing, they aren't "real".
sys.path.append(os.path.join(here, 'fake_packages'))

