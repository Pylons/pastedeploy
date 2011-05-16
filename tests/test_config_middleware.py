from nose.tools import assert_raises
from paste.deploy.config import ConfigMiddleware
from paste.fixture import TestApp

class Bug(Exception): pass

def app_with_exception(environ, start_response):
    def cont():
        yield "something"
        raise Bug
    start_response('200 OK', [('Content-type', 'text/html')])
    return cont()

def test_error():
    wrapped = ConfigMiddleware(app_with_exception, {'test': 1})
    test_app = TestApp(wrapped)
    assert_raises(Bug, test_app.get, '/')

