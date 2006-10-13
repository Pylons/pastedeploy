class AppFactoryDescription(object):
    description = """
    This gives a factory/function that can create WSGI apps
    """

class CompositeFactoryDescription(object):
    description = """
    This gives a factory/function that can create WSGI apps, and has
    access to the application creator so that it can in turn fetch
    apps based on name.
    """

class FilterAppFactoryDescription(object):
    description = """
    This gives a factory/function that wraps a WSGI application to
    create another WSGI application (typically applying middleware)
    """

class FilterFactoryDescription(object):
    description = """
    This gives a factory/function that return a function that can wrap
    a WSGI application and returns another WSGI application.
    paste.filter_app_factory is the same thing with less layers.
    """

class ServerFactoryDescription(object):
    description = """
    This gives a factory/function that creates a server, that can be
    called with a WSGI application to run indefinitely.
    paste.server_runner is the same thing with less layers.
    """

class ServerRunnerDescription(object):
    description = """
    This gives a factory/function that, given a WSGI application and
    configuration, will serve the application indefinitely.
    """
