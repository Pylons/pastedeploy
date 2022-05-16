import os
import sys

here = os.path.dirname(__file__)
base = os.path.dirname(here)
sys.path.insert(0, base)

import pkg_resources  # noqa E402

# Make absolutely sure we're testing *this* package, not
# some other installed package
pkg_resources.require('PasteDeploy')
