import os
import urllib
from ConfigParser import RawConfigParser
import pkg_resources

############################################################
## Object types
############################################################

class _ObjectType(object):

    def __init__(self, name, egg_protocols, config_prefixes):
        self.name = name
        self.egg_protocols = map(_aslist, _aslist(egg_protocols))
        self.config_prefixes = map(_aslist, _aslist(config_prefixes))

    def __repr__(self):
        return '<%s protocols=%r prefixes=%r>' % (
            self.name, self.egg_protocols, self.config_prefixees)

def _aslist(obj):
    if obj is None:
        return []
    elif isinstance(obj, (list, tuple)):
        return obj
    else:
        return [obj]

def _flatten(lst):
    if not isinstance(lst, (list, tuple)):
        return [lst]
    result = []
    for item in lst:
        result.extend(_flatten(item))
    return result

APP = _ObjectType(
    'application',
    ['paste.app_factory1', 'paste.composit_factory1'],    
    [['app', 'application'], 'composit'])

def APP_invoke(context):
    if context.protocol == 'paste.composit_factory1':
        return context.object(context.loader, context.global_conf,
                              **context.local_conf)
    elif context.protocol == 'paste.app_factory1':
        return context.object(context.global_conf, **context.local_conf)
    else:
        assert 0, "Protocol %r unknown" % context.protocol

APP.invoke = APP_invoke

FILTER = _ObjectType(
    'filter',
    ['paste.filter_factory1'],
    ['filter'])

def FILTER_invoke(context):
    assert context.protocol == 'paste.filter_factory1'
    return context.object(context.global_conf, **context.local_conf)

FILTER.invoke = FILTER_invoke

SERVER = _ObjectType(
    'server',
    ['paste.server_factory1'],
    ['server'])

def SERVER_invoke(context):
    assert context.protocol == 'paste.server_factory1'
    return context.object(context.global_conf, **context.local_conf)

SERVER.invoke = SERVER_invoke

def import_string(s):
    return pkg_resources.EntryPoint.parse("x="+s).load(False)

############################################################
## Locators
############################################################

def find_egg_entry_point(object_type, egg_spec, name=None):
    """
    Returns the (entry_point, protocol) for the with the given
    ``name`` and specification ``egg_spec``.
    """
    if name is None:
        name = 'main'
    possible = []
    for protocol_options in object_type.egg_protocols:
        for protocol in protocol_options:
            entry = pkg_resources.get_entry_info(
                egg_spec,
                protocol,
                name)
            if entry is not None:
                possible.append((entry.load(), protocol))
                break
    if not possible:
        # Better exception
        print pkg_resources.get_entry_map(egg_spec)
        raise LookupError(
            "Entry point %r not found in egg %r (protocols: %s)"
            % (name, egg_spec,
               ', '.join(_flatten(object_type.egg_protocols))))
    if len(possible) > 1:
        raise LookupError(
            "Ambiguous entry points for %r in egg %r (protocols: %s)"
            % (name, egg_spec, ', '.join(_flatten(protocol_list))))
    return possible[0]

def find_config_section(object_type, config_sections,
                        name=None):
    """
    Return the section name with the given name prefix (following the
    same pattern as ``protocol_desc`` in ``config``.  It must have the
    given name, or for ``'main'`` an empty name is allowed.  The
    prefix must be followed by a ``:``.

    Case is *not* ignored.
    """
    possible = []
    for name_options in object_type.config_prefixes:
        for name_prefix in name_options:
            found = _find_sections(config_sections, name_prefix, name)
            if found:
                possible.extend(found)
                break
    if not possible:
        raise LookupError(
            "No section %r (prefixed by %r) found in config"
            % (name, _flatten(name_prefix_list)))
    if len(possible) > 1:
        raise LookupError(
            "Ambiguous section names %r for section %r (prefixed by %r) "
            "found in config"
            % (possible, name, _flatten(name_prefix_list)))
    return possible[0]

def _find_sections(sections, name_prefix, name):
    found = []
    if name is None:
        if name_prefix in sections:
            found.append(name_prefix)
        name = 'main'
    for section in sections:
        if section.startswith(name_prefix+':'):
            if section[len(name_prefix)+1:].strip() == name:
                found.append(section)
    return found

############################################################
## Loaders
############################################################

def loadapp(uri, name=None, **kw):
    return loadobj(APP, uri, name=name, **kw)

def loadfilter(uri, name=None, **kw):
    return loadobj(FILTER, uri, name=name, **kw)

def loadserver(uri, name=None, **kw):
    return loadobj(SERVER, uri, name=name, **kw)

_loaders = {}

def loadobj(object_type, uri, name=None, relative_to=None,
            global_conf=None):
    context = loadcontext(
        object_type, uri, name=name, relative_to=relative_to,
        global_conf=global_conf)
    return object_type.invoke(context)

def loadcontext(object_type, uri, name=None, relative_to=None,
                global_conf=None):
    if '#' in uri:
        if name is None:
            uri, name = uri.split('#', 1)
        else:
            # @@: Ignore fragment or error?
            uri = uri.split('#', 1)[0]
    scheme, path = uri.split(':', 1)
    scheme = scheme.lower()
    if scheme not in _loaders:
        raise LookupError(
            "URI scheme not known: %r (from %s)"
            % (scheme, ', '.join(_loaders.keys())))
    return _loaders[scheme](
        object_type,
        uri, path, name=name, relative_to=relative_to,
        global_conf=global_conf)

def _loadconfig(object_type, uri, path, name, relative_to,
                global_conf):
    # De-Windowsify the paths:
    path = path.replace('\\', '/')
    if not path.startswith('/'):
        if not relative_to:
            raise ValueError(
                "Cannot resolve relative uri %r; no context keyword "
                "argument given" % uri)
        relative_to = relative_to.replace('\\', '/')
        if relative_to.endswith('/'):
            path = relative_to + path
        else:
            path = relative_to + '/' + path
    if path.startswith('///'):
        path = path[2:]
    path = urllib.unquote(path)
    loader = ConfigLoader(path)
    return loader.get(object_type, name, global_conf)

_loaders['config'] = _loadconfig

def _loadegg(object_type, uri, spec, name, relative_to,
             global_conf):
    loader = EggLoader(spec)
    return loader.get(object_type, name, global_conf)

_loaders['egg'] = _loadegg

############################################################
## Loaders
############################################################

class _Loader(object):

    def getapp(self, name=None, global_conf=None):
        return self.get(APP, name=name, global_conf=global_conf)

    def getfilter(self, name=None, global_conf=None):
        return self.get(FILTER, name=name, global_conf=global_conf)

    def getserver(self, name=None, global_conf=None):
        return self.get(SERVER, name=name, global_conf=global_conf)

class ConfigLoader(_Loader):

    def __init__(self, filename):
        self.filename = filename
        self.parser = RawConfigParser()
        # Don't lower-case keys:
        self.parser.optionxform = str
        self.parser.read(filename)

    def get(self, object_type, name=None, global_conf=None):
        if global_conf is None:
            global_conf = {}
        else:
            global_conf = global_conf.copy()
        section = find_config_section(
            object_type, self.parser.sections(), name=name)
        global_conf.update(self.parser.defaults())
        local_conf = {}
        for option in self.parser.options(section):
            if option.startswith('set '):
                name = option[4:].strip()
                global_conf[name] = self.parser.get(section, option)
            else:
                local_conf[option] = self.parser.get(section, option)
        if 'use' in local_conf:
            use = local_conf.pop('use')
            context = loadcontext(
                object_type, use,
                relative_to=os.path.dirname(self.filename))
            context.global_conf.update(global_conf)
            context.local_conf.update(local_conf)
            # @@: Should loader be overwritten?
            context.loader = self
            return context
        possible = []
        for protocol_options in object_type.egg_protocols:
            for protocol in protocol_options:
                if protocol in local_conf:
                    possible.append((protocol, local_conf[protocol]))
                    break
        if len(possible) > 1:
            raise LookupError(
                "Multiple protocols given in section %r: %s"
                % (section, possible))
        if not possible:
            raise LookupError(
                "No loader given in section %r" % section)
        value = import_string(possible[0][1])
        context = LoaderContext(
            value, object_type, possible[0][0],
            global_conf, local_conf, self)
        return context

class EggLoader(_Loader):

    def __init__(self, spec):
        self.spec = spec

    def get(self, object_type, name=None, global_conf=None):
        entry_point, protocol = find_egg_entry_point(
            object_type, self.spec, name=name)
        return LoaderContext(
            entry_point,
            object_type,
            protocol,
            global_conf or {}, {},
            self)

class LoaderContext(object):

    def __init__(self, obj, object_type, protocol,
                 global_conf, local_conf, loader):
        self.object = obj
        self.object_type = object_type
        self.protocol = protocol
        self.global_conf = global_conf
        self.local_conf = local_conf
        self.loader = loader

    
