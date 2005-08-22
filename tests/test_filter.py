from paste.deploy import loadapp, loadfilter
from fixture import *
import fakeapp.apps

here = os.path.dirname(__file__)

def test_filter_app():
    app = loadapp('config:sample_configs/test_filter.ini#filt',
                  relative_to=here)
    assert isinstance(app, fakeapp.apps.CapFilter)
    assert app.app is fakeapp.apps.basic_app
    assert app.method_to_call == 'lower'

def test_pipeline():
    app = loadapp('config:sample_configs/test_filter.ini#piped',
                  relative_to=here)
    assert isinstance(app, fakeapp.apps.CapFilter)
    assert app.app is fakeapp.apps.basic_app
    assert app.method_to_call == 'upper'
