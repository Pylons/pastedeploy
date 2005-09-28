import threading
# Loaded lazily
wsgilib = None
local = None

__all__ = ['DispatchingConfig', 'CONFIG', 'ConfigMiddleware']

def local_dict():
    global config_local, local
    try:
        return config_local.wsgi_dict
    except NameError:
        import pkg_resources
        pkg_resources.require('Paste>=0.1')
        from paste.util.threadinglocal import local
        config_local = local()
        config_local.wsgi_dict = result = {}
        return result
    except AttributeError:
        config_local.wsgi_dict = result = {}
        return result

class DispatchingConfig(object):

    """
    This is a configuration object that can be used globally,
    imported, have references held onto.  The configuration may differ
    by thread (or may not).

    Specific configurations are registered (and deregistered) either
    for the process or for threads.
    """

    # @@: What should happen when someone tries to add this
    # configuration to itself?  Probably the conf should become
    # resolved, and get rid of this delegation wrapper

    _constructor_lock = threading.Lock()

    def __init__(self):
        self._constructor_lock.acquire()
        try:
            self.dispatching_id = 0
            while 1:
                self._local_key = 'paste.processconfig_%i' % self.dispatching_id
                if not local_dict().has_key(self._local_key):
                    break
                self.dispatching_id += 1
        finally:
            self._constructor_lock.release()
        self._process_configs = []

    def push_thread_config(self, conf):
        """
        Make ``conf`` the active configuration for this thread.
        Thread-local configuration always overrides process-wide
        configuration.

        This should be used like::

            conf = make_conf()
            dispatching_config.push_thread_config(conf)
            try:
                ... do stuff ...
            finally:
                dispatching_config.pop_thread_config(conf)
        """
        local_dict().setdefault(self._local_key, []).append(conf)

    def pop_thread_config(self, conf=None):
        """
        Remove a thread-local configuration.  If ``conf`` is given,
        it is checked against the popped configuration and an error
        is emitted if they don't match.
        """
        self._pop_from(local_dict()[self._local_key], conf)

    def _pop_from(self, lst, conf):
        popped = lst.pop()
        if conf is not None and popped is not conf:
            raise AssertionError(
                "The config popped (%s) is not the same as the config "
                "expected (%s)"
                % (popped, conf))

    def push_process_config(self, conf):
        """
        Like push_thread_config, but applies the configuration to
        the entire process.
        """
        self._process_configs.append(conf)

    def pop_process_config(self, conf=None):
        self._pop_from(self._process_configs, conf)
            
    def __getattr__(self, attr):
        conf = self.current_conf()
        if not conf:
            raise AttributeError(
                "No configuration has been registered for this process "
                "or thread")
        return getattr(conf, attr)

    def current_conf(self):
        thread_configs = local_dict().get(self._local_key)
        if thread_configs:
            return thread_configs[-1]
        elif self._process_configs:
            return self._process_configs[-1]
        else:
            return None

    def __getitem__(self, key):
        # I thought __getattr__ would catch this, but apparently not
        conf = self.current_conf()
        if not conf:
            raise TypeError(
                "No configuration has been registered for this process "
                "or thread")
        return conf[key]

CONFIG = DispatchingConfig()

class ConfigMiddleware(object):

    """
    A WSGI middleware that adds a ``paste.config`` key to the request
    environment, as well as registering the configuration temporarily
    (for the length of the request) with ``paste.CONFIG``.
    """

    def __init__(self, application, config):
        """
        This delegates all requests to `application`, adding a *copy*
        of the configuration `config`.
        """
        self.application = application
        self.config = config

    def __call__(self, environ, start_response):
        global wsgilib
        if wsgilib is None:
            import pkg_resources
            pkg_resources.require('Paste')
            from paste import wsgilib
        conf = environ['paste.config'] = self.config.copy()
        app_iter = None
        CONFIG.push_thread_config(conf)
        try:
            app_iter = self.application(environ, start_response)
        finally:
            if app_iter is None:
                # An error occurred...
                CONFIG.pop_thread_config(conf)
        if type(app_iter) in (list, tuple):
            # Because it is a concrete iterator (not a generator) we
            # know the configuration for this thread is no longer
            # needed:
            CONFIG.pop_thread_config(conf)
            return app_iter
        else:
            def close_config():
                CONFIG.pop_thread_config(conf)
            new_app_iter = wsgilib.add_close(app_iter, close_config)
            return new_app_iter

def make_config_filter(app, global_conf, **local_conf):
    conf = global_conf.copy()
    conf.update(local_conf)
    return ConfigMiddleware(app, conf)

