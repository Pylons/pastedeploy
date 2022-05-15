class SimpleApp:
    def __init__(self, global_conf, local_conf, name):
        self.global_conf = global_conf
        self.local_conf = local_conf
        self.name = name

    def __call__(self, environ, start_response):
        start_response('200 OK', [('Content-type', 'text/html')])
        return ['I am: ', name]
        
    def make_app(cls, global_conf, **conf):
        return cls(global_conf, conf, 'basic')
    make_app = classmethod(make_app)

