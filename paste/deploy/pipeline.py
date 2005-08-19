from paste import wsgi_deploy

def make_pipeline(context):
    pipeline = filter(
        None, context.app_config.get('pipeline', '').split())
    if not pipeline:
        raise IndexError(
            "You must give a pipeline setting")
    filters = pipeline[:-1]
    filters.reverse()
    app_name = pipeline[-1]
    deploy = context.deployment_config
    app = deploy.make_app(app_name)
    for filter_name in filters:
        wsgi_filter = deploy.make_filter(filter_name)
        app = wsgi_filter(app)
    return app

