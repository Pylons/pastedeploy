# (c) 2005 Ian Bicking and contributors; written for Paste (http://pythonpaste.org)
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php
from loadwsgi import *
try:
    from config import CONFIG
except ImportError:
    # @@: Or should we require Paste?  Or should we put threadlocal
    # into this package too?
    pass

