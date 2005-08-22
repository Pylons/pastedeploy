############################################################
## Apps
############################################################

def simple_app(response, environ, start_response):
    start_response('200 OK', [('Content-type', 'text/html')])
    return ['This is ', response]

def basic_app(environ, start_response):
    return simple_app('basic app', environ, start_response)

def make_basic_app(global_conf, **conf):
    return basic_app

def basic_app2(environ, start_response):
    return simple_app('basic app2', environ, start_response)
    
def make_basic_app2(global_conf, **conf):
    return basic_app2

############################################################
## Composits
############################################################

def make_remote_addr(loader, global_conf, **conf):
    apps = {}
    addrs = {}
    for name, value in conf.items():
        if name.startswith('app.'):
            apps[name[4:]] = loader.get_app(value, global_conf)
        elif name.startswith('addr.'):
            addrs[name[5:]] = value
    dispatcher = RemoteAddrDispatch()
    for name in apps:
        dispatcher.map[addrs[name]] = apps[name]
    return dispatcher

class RemoteAddrDispatch(object):
    def __init__(self, map=None):
        self.map = map or {}

    def __call__(self, environ, start_response):
        addr = environ['REMOTE_ADDR']
        app = self.map.get(addr) or self.map['0.0.0.0']
        return app(environ, start_response)

############################################################
## Filters
############################################################

def make_cap_filter(global_conf, method_to_call='upper'):
    def filter(app):
        return CapFilter(app, method_to_call)
    return filter

class CapFilter(object):

    def __init__(self, app, method_to_call):
        self.app = app
        self.method_to_call = method_to_call

    def __call__(self, environ, start_response):
        app_iter = self.app(environ, start_response)
        for item in app_iter:
            yield getattr(item, self.method_to_call)()
        if hasattr(app_iter, 'close'):
            app_iter.close()

