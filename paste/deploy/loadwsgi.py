import os
from ConfigParser import RawConfigParser
from paste import server
from paste.util import import_string
import pkg_resources

class ConfigError(Exception):

    def __init__(self, deployment_config, *args):
        self.deployment_config = deployment_config
        Exception.__init__(self, *args)

def make_paste_app(context, app_ops):
    """
    Create a WSGI application using Paste conventions.  app_ops
    are options that are fixed for this application (i.e., don't
    haveto be configured; things like 'framework' that Paste
    treats specially).
    """
    ops = app_ops.copy()
    ops.update(context.app_config)
    return server.make_app(ops)

############################################################
## Deployment utility functions
############################################################


class DeploymentConfig(object):

    def __init__(self, filename):
        self.filename = filename
        parser = RawConfigParser()
        parser.read([filename])
        self.data = {}
        # @@: DEFAULT?
        for section in parser.sections():
            self.data[section] = {}
            for key in parser.options(section):
                self.data[section][key] = parser.get(section, key)

    def make_app(self, name='main'):
        """
        Create a WSGI application with the given name.  The factories
        are functions that are called like
        ``factory(config_context)`` and
        return a WSGI application.
        """
        factory, context = self.make_factory(
            'application', 'wsgi.app_factory01', name)
        return factory(context)

    def make_filter(self, name):
        """
        Create a WSGI filter with the given name.  No default/'main'
        name applies here.
        
        The factory is called like ``factory(config_context)`` and
        returns a function that is called like ``filter(app)`` and
        returns a WSGI application.
        """
        factory, context = self.make_factory(
            'filter', 'wsgi.filter_factory01', name)
        return factory(context)

    def make_server(self, name='main'):
        """
        Creates a WSGI server.  The server is a factory that is called
        like ``factory(options...)``, where all the settings in the
        section are turned into keyword arguments (except 'use' and
        'factory' which are special).  The server is called with a
        single application to serve that application indefinitely.
        """
        factory, context = self.make_factory(
            'server', 'wsgi.server_factory00', name)
        ops = context.app_config.copy()
        for key in 'factory', 'use', 'require':
            if key in ops:
                del ops[key]
        return factory(**ops)

    def make_deployment(self):
        """
        From a configuration, return both the server and main app, so
        you can do::

          conf = DeploymentConfig(...)
          server, app = conf.make_deployment()
          server(app)
        """
        server = self.make_server()
        app = self.make_app()
        return server, app

    def make_factory(self, type, entry_point_type, name):
        if name.startswith('file:'):
            filename, app_name = self.split_filename(name[5:])
            filename = self.normalize_filename(filename)
            deploy = self.__class__(filename)
            return deploy.make_factory(type, entry_point_type, app_name)
        section = self.find_match(type, name, self.data.keys())
        factory = self.make_factory_from_section(
            type, entry_point_type, section)
        context = self.make_context_from_section(section)
        return factory, context

    def make_factory_from_section(self, type, entry_point_type, section):
        conf = self.data[section]
        if 'require' in conf:
            for spec in conf['require'].split():
                pkg_resources.require(spec)
        if 'config' in conf:
            filename = conf['config']
            filename, app_name = self.split_filename(filename)
            filename = self.normalize_filename(filename)
            deploy = self.__class__(filename)
            return deploy.make_factory(
                type, entry_point_type, app_name)
        if 'factory' in conf:
            return import_string.eval_import(conf['factory'])
        if 'use' in conf:
            spec, name = conf['use'].split()
            return pkg_resources.load_entry_point(
                spec, entry_point_type, name)
        raise ConfigError(
            self, "No way to create a factory from section [%s] "
            "(no factory or use key)" % section)

    def split_filename(self, filename):
        """
        Given a filename with an optional :appname part, return
        the ``(filename, app_name)``
        """
        # Make sure we don't catch Windows drives:
        if filename.find(':') > 1:
            new_f, app_name = filename[2:].split(':')
            return filename[:2] + new_f, app_name
        else:
            return filename, 'main'

    def normalize_filename(self, filename):
        return os.path.join(os.path.dirname(self.filename), filename)

    def find_match(self, type, name, possible):
        type = type.lower()
        for section in possible:
            section = section.strip()
            if section.lower() == type and (not name or name == 'main'):
                return section
            if not section.lower().startswith(type + ':'):
                continue
            section_name = section[len(type)+1:].strip()
            if section_name == name:
                return section
        raise ConfigError(
            self, "No section like [%s: %s] found" % (type, name))

    def make_context_from_section(self, section):
        conf = self.data[section]
        return ConfigContext(self, conf)

class ConfigContext(object):

    def __init__(self, deployment_config, app_config):
        self.deployment_config = deployment_config
        self.app_config = app_config

if __name__ == '__main__':
    import sys
    conf = DeploymentConfig(sys.argv[1])
    server, app = conf.make_deployment()
    server(app)
    
