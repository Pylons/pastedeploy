from loadwsgi import loadapp, loadfilter, loadserver
try:
    from config import CONFIG
except ImportError:
    # @@: Or should we require Paste?  Or should we put threadlocal
    # into this package too?
    pass

