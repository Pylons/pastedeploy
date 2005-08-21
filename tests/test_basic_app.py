from paste.deploy import loadapp, loadfilter
from fixture import *
require('FakeApp')
import fakeapp.apps

here = os.path.dirname(__file__)

def test_main():
    app = loadapp('config:sample_configs/basic_app.ini',
                  relative_to=here)
    assert app is fakeapp.apps.basic_app
    app = loadapp('config:sample_configs/basic_app.ini#main',
                  relative_to=here)
    assert app is fakeapp.apps.basic_app
    app = loadapp('config:sample_configs/basic_app.ini',
                  relative_to=here, name='main')
    assert app is fakeapp.apps.basic_app
    app = loadapp('config:sample_configs/basic_app.ini#ignored',
                  relative_to=here, name='main')
    assert app is fakeapp.apps.basic_app

def test_other():
    app = loadapp('config:sample_configs/basic_app.ini#other',
                  relative_to=here)
    assert app is fakeapp.apps.basic_app2
    
