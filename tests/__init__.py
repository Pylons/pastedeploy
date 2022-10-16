import os
import shutil
import sys

here = os.path.dirname(__file__)
base = os.path.dirname(here)
sys.path.insert(0, base)

test_dir = os.path.dirname(__file__)
egg_info_dir = os.path.join(test_dir, 'fake_packages', 'FakeApp.egg', 'EGG-INFO')
info_dir = os.path.join(test_dir, 'fake_packages', 'FakeApp.egg', 'FakeApp.egg-info')
if not os.path.exists(egg_info_dir):
    try:
        os.symlink(info_dir, egg_info_dir)
    except Exception:
        shutil.copytree(info_dir, egg_info_dir)

sys.path.append(os.path.dirname(egg_info_dir))

from paste.deploy.util import importlib_metadata  # noqa E402

# Make absolutely sure we're testing *this* package, not
# some other installed package
importlib_metadata.distribution('PasteDeploy')

# ensure FakeApp is available for use by tests
importlib_metadata.distribution('FakeApp')
