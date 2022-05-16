import os

import fakeapp.apps

from paste.deploy import loadapp

here = os.path.dirname(__file__)


def test_filter_app():
    app = loadapp('config:sample_configs/test_filter.ini#filt', relative_to=here)
    assert isinstance(app, fakeapp.apps.CapFilter)
    assert app.app is fakeapp.apps.basic_app
    assert app.method_to_call == 'lower'


def test_pipeline():
    app = loadapp('config:sample_configs/test_filter.ini#piped', relative_to=here)
    assert isinstance(app, fakeapp.apps.CapFilter)
    assert app.app is fakeapp.apps.basic_app
    assert app.method_to_call == 'upper'


def test_filter_app2():
    app = loadapp('config:sample_configs/test_filter.ini#filt2', relative_to=here)
    assert isinstance(app, fakeapp.apps.CapFilter)
    assert app.app is fakeapp.apps.basic_app
    assert app.method_to_call == 'lower'


def test_pipeline2():
    app = loadapp('config:sample_configs/test_filter.ini#piped2', relative_to=here)
    assert isinstance(app, fakeapp.apps.CapFilter)
    assert app.app is fakeapp.apps.basic_app
    assert app.method_to_call == 'upper'


def test_filter_app_inverted():
    app = loadapp('config:sample_configs/test_filter.ini#inv', relative_to=here)
    assert isinstance(app, fakeapp.apps.CapFilter)
    assert app.app is fakeapp.apps.basic_app


def test_filter_with_filter_with():
    app = loadapp('config:sample_configs/test_filter_with.ini', relative_to=here)
    assert isinstance(app, fakeapp.apps.CapFilter)
    assert isinstance(app.app, fakeapp.apps.CapFilter)
    assert app.app.app is fakeapp.apps.basic_app


def test_bad_pipeline():
    try:
        loadapp('config:sample_configs/test_filter.ini#piped3', relative_to=here)
    except LookupError as err:
        assert 'has extra (disallowed) settings' in err.args[0]
    else:
        raise AssertionError('should have raised LookupError')
