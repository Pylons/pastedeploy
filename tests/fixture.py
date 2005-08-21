import os
from paste.deploy import load

def conf_fn(filename):
    return os.path.join(os.path.dirname(__file__), 'sample_configs', filename)

def loadtest(base_filename, *args **kw):
    return load(conf_fn(base_filename), *args, **kw)
