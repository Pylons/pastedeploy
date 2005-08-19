from paste import wsgi_deploy
from paste import urlmap

def make_urlmap(context):
    mapper = urlmap.URLMap()
    for key, value in context.app_config.items():
        if (key.startswith('/') or key.startswith('http://')
            or key.startswith('https://')):
            app = context.deployment_config.make_app(value)
            mapper[key] = app
    return mapper

