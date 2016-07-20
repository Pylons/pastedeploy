import pytest

from paste.deploy.config import ConfigMiddleware


class Bug(Exception):
    pass


def app_with_exception(environ, start_response):
    def cont():
        yield b"something"
        raise Bug
    start_response('200 OK', [('Content-type', 'text/html')])
    return cont()


def test_error():
    # This import is conditional due to Paste not yet working on py3k
    try:
        from paste.fixture import TestApp
    except ImportError:
        raise SkipTest

    wrapped = ConfigMiddleware(app_with_exception, {'test': 1})
    test_app = TestApp(wrapped)
    pytest.raises(Bug, test_app.get, '/')
