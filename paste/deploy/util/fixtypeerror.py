# (c) 2005 Ian Bicking and contributors; written for Paste (http://pythonpaste.org)
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php
"""
Fixes the vague error message that you get when calling a function
with the wrong arguments.
"""
import inspect
import sys

def fix_type_error(exc_info, callable, varargs, kwargs):
    """
    Given an exception, this will test if the exception was due to a
    signature error, and annotate the error with better information if
    so.
    
    Usage::

      try:
          val = callable(*args, **kw)
      except TypeError:
          exc_info = fix_type_error(None, callable, args, kw)
          raise exc_info[0], exc_info[1], exc_info[2]
    """
    if exc_info is None:
        exc_info = sys.exc_info()
    if (exc_info[0] != TypeError
        or str(exc_info[1]).find('arguments') == -1
        or getattr(exc_info[1], '_type_error_fixed', False)):
        return exc_info
    exc_info[1]._type_error_fixed = True
    import inspect
    argspec = inspect.formatargspec(*inspect.getargspec(callable))
    args = ', '.join(map(_short_repr, varargs))
    if kwargs and args:
        args += ', '
    if kwargs:
        kwargs = kwargs.items()
        kwargs.sort()
        args += ', '.join(['%s=...' % n for n, v in kwargs])
    gotspec = '(%s)' % args
    msg = '%s; got %s, wanted %s' % (exc_info[1], gotspec, argspec)
    exc_info[1].args = (msg,)
    return exc_info

def _short_repr(v):
    v = repr(v)
    if len(v) > 12:
        v = v[:8]+'...'+v[-4:]
    return v

def fix_call(callable, *args, **kw):
    """
    Call ``callable(*args, **kw)`` fixing any type errors that come
    out.
    """
    try:
        val = callable(*args, **kw)
    except TypeError:
        exc_info = fix_type_error(None, callable, args, kw)
        raise exc_info[0], exc_info[1], exc_info[2]
    return val
