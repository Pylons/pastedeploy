def simple_app(response, environ, start_response):
    start_response('200 OK', [('Content-type', 'text/html')])
    return [response]

def basic_app(environ, start_response):
    return simple_app('basic app', environ, start_response)

def make_basic_app(global_conf, **conf):
    return basic_app

def basic_app2(environ, start_response):
    return simple_app('basic app2', environ, start_response)
    
def make_basic_app2(global_conf, **conf):
    return basic_app2
