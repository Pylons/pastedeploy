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
    wrapped = ConfigMiddleware(app_with_exception, {'test': 1})

    environ = {
        'REQUEST_METHOD': 'GET',
        'PATH_INFO': '/',
        'SERVER_NAME': 'localhost',
        'SERVER_PORT': '80',
        'wsgi.input': b'',
        'wsgi.errors': None,
        'wsgi.url_scheme': 'http',
        'HTTP_HOST': 'localhost',
    }
    responses = []

    def start_response(status, headers):
        responses.append(status)

    app_iter = wrapped(environ, start_response)
    with pytest.raises(Bug):
        list(app_iter)
