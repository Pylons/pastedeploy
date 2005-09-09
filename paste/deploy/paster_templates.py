from paste.script.templates import Template

class PasteDeploy(Template):

    _template_dir = 'paster_templates/paste_deploy'
    summary = "A web application deployed through paste.deploy"
    
    egg_plugins = ['PasteDeploy']
    
