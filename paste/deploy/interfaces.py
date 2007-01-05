# (c) 2005 Ian Bicking and contributors; written for Paste (http://pythonpaste.org)
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php
############################################################
## Functions
############################################################

def loadapp(uri, name=None, relative_to=None, global_conf=None):
    """
    Provided by ``paste.deploy.loadapp``.
    
    Load the specified URI as a WSGI application (returning IWSGIApp).
    The ``name`` can be in the URI (typically as ``#name``).  If it is
    and ``name`` is given, the keyword argument overrides the URI.

    If the URI contains a relative filename, then ``relative_to`` is
    used (if ``relative_to`` is not provided, then it is an error).

    ``global_conf`` is used to load the configuration (additions
    override the values).  ``global_conf`` is copied before modifying.
    """

def loadfilter(uri, name=None, relative_to=None, global_conf=None):
    """
    Provided by ``paste.deploy.loadfilter``.

    Like ``loadapp()``, except returns in IFilter object.
    """

def loadserver(uri, name=None, relative_to=None, global_conf=None):
    """
    Provided by ``paste.deploy.loadserver``.

    Like ``loadapp()``, except returns in IServer object.
    """

############################################################
## Factories
############################################################

class IPasteAppFactory(object):

    """
    This is the spec for the ``paste.app_factory``
    protocol/entry_point.
    """

    def __call__(global_conf, **local_conf):
        """
        Returns a WSGI application (IWSGIAPP) given the global
        configuration and the local configuration passed in as keyword
        arguments.

        All keys are strings, but values in local_conf may not be
        valid Python identifiers (if you use ``**kw`` you can still
        capture these values).
        """

class IPasteCompositFactory(object):

    """
    This is the spec for the ``paste.composit_factory``
    protocol/entry_point.

    This also produces WSGI applications, like ``paste.app_factory``,
    but is given more access to the context in which it is loaded.
    """

    def __call__(loader, global_conf, **local_conf):
        """
        Like IPasteAppFactory this returns a WSGI application
        (IWSGIApp).  The ``loader`` value conforms to the ``ILoader``
        interface, and can be used to load (contextually) more
        applications.
        """

class IPasteFilterFactory(object):

    """
    This is the spec for the ``paste.filter_factory``
    protocol/entry_point.
    """

    def __call__(global_conf, **local_conf):
        """
        Returns a IFilter object.
        """

class IPasteFilterAppFactory(object):

    """
    This is the spec for the ``paste.filter_app_factory``
    protocol/entry_point.
    """
    
    def __call__(wsgi_app, global_conf, **local_conf):
        """
        Returns a WSGI application that wraps ``wsgi_app``.

        Note that paste.deploy creates a wrapper for these
        objects that implement the IFilter interface.
        """

class IPasteServerFactory(object):

    """
    This is the spec for the ``paste.server_factory``
    protocol/entry_point.
    """

    def __call__(global_conf, **local_conf):
        """
        Returns a IServer object.
        """

class IPasteServerRunner(object):

    """
    This is the spec for the ``paste.server_runner``
    protocol/entry_point.
    """

    def __call__(wsgi_app, global_conf, **local_conf):
        """
        Serves the given WSGI application.  May serve once, many
        times, forever; nothing about how the server works is
        specified here.

        Note that paste.deploy creates a wrapper for these
        objects that implement the IServer interface.
        """

class ILoader(object):

    """
    This is an object passed into ``IPasteCompositFactory``.  It is
    currently implemented in ``paste.deploy.loadwsgi`` by
    ``ConfigLoader`` and ``EggLoader``.
    """

    def get_app(name_or_uri, global_conf=None):
        """
        Return an IWSGIApp object.  If the loader supports named
        applications, then you can use a simple name; otherwise
        you must use a full URI.

        Any global configuration you pass in will be added; you should
        generally pass through the global configuration you received.
        """

    def get_filter(name_or_uri, global_conf=None):
        """
        Return an IFilter object, like ``get_app``.
        """
                   
    def get_server(name_or_uri, global_conf=None):
        """
        Return an IServer object, like ``get_app``.
        """

############################################################
## Objects
############################################################

class IWSGIApp(object):

    """
    This is an application that conforms to `PEP 333
    <http://www.python.org/peps/pep-0333.html>`_: Python Web Server
    Gateway Interface v1.0
    """

    def __call__(environ, start_response):
        """
        Calls ``start_response(status_code, header_list)`` and returns
        an iterator for the body of the response.
        """

class IFilter(object):

    """
    A filter is a simple case of middleware, where an object
    wraps a single WSGI application (IWSGIApp).
    """

    def __call__(wsgi_app):
        """
        Returns an IWSGIApp object, typically one that wraps the
        ``wsgi_app`` passed in.
        """

class IServer(object):

    """
    A simple server interface.
    """

    def __call__(wsgi_app):
        """
        Serves the given WSGI application.  May serve once, many
        times, forever; nothing about how the server works is
        specified here.
        """
