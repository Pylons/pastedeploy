import os
import sys
import shutil

test_dir = os.path.dirname(__file__)
egg_info_dir = os.path.join(test_dir, 'fake_packages', 'FakeApp.egg',
                            'EGG-INFO')
info_dir = os.path.join(test_dir, 'fake_packages', 'FakeApp.egg',
                        'FakeApp.egg-info')
if not os.path.exists(egg_info_dir):
    try:
        os.symlink(info_dir, egg_info_dir)
    except:
        shutil.copytree(info_dir, egg_info_dir)
        
sys.path.append(os.path.dirname(egg_info_dir))

from pkg_resources import *
working_set.add_entry(os.path.dirname(egg_info_dir))
require('FakeApp')

