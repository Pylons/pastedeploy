Paste Deployment News
=====================

3.0 (2022-10-16)
----------------

* Drop support for Python 2, as well as 3.4, 3.5, and 3.6.

* Fix a broken compatibility shim that would cause the ConfigParser to fail
  on Python 3.12 when ``ConfigParser.readfp`` is removed.

* Drop setuptools dependency and start using ``importlib.metadata`` instead.

* Refactor repository into a src folder layout.

2.1.1 (2020-10-12)
------------------

* Added ``setuptools`` as an explicit dependency.
  This has always been required but now that more environments are becoming capable of operating without it being installed, we now need to ensure it's available.

2.1.0
-----

* pytest-runner removed, use tox to run tests.

2.0.0
-----

* Python 3 deprecation warning cleanups
* Moved code to `GitHub <https://github.com/Pylons/pastedeploy>`_ under the Pylons Project.
* Moved documentation under the Pylons Project, hosted by Read the Docs at https://docs.pylonsproject.org/projects/pastedeploy/en/latest/

1.5.2
-----

* Fixed Python 3 issue in paste.deploy.util.fix_type_error()

1.5.1
-----

* Fixed use of the wrong variable when determining the context protocol

* Fixed invalid import of paste.deploy.Config to paste.deploy.config.Config

* Fixed multi proxy IPs bug in X-Forwarded-For header in PrefixMiddleware

* Fixed TypeError when trying to raise LookupError on Python 3

* Fixed exception reraise on Python 3

Thanks to Alexandre Conrad, Atsushi Odagiri, Pior Bastida and Tres Seaver for their contributions.

1.5.0
-----

* Project is now maintained by Alex Grönholm <alex.gronholm@nextday.fi>

* Was printing extraneous data when calling setup.py

* Fixed missing paster template files (fixes "paster create -t paste.deploy")

* Excluded tests from release distributions

* Added support for the "call:" protocol for loading apps directly as
  functions (contributed by Jason Stitt)

* Added Python 3.x support

* Dropped Python 2.4 support

* Removed the ``paste.deploy.epdesc`` and ``paste.deploy.interfaces`` modules
  -- contact the maintainer if you actually needed them

1.3.4
-----

* Fix loadconfig path handling on Jython on Windows.

1.3.3
-----

* In :class:`paste.deploy.config.PrefixMiddleware` the headers
  ``X-Forwarded-Scheme`` and ``X-Forwarded-Proto`` are now translated
  to the key ``environ['wsgi.url_scheme']``.  Also ``X-Forwarded-For``
  is translated to ``environ['REMOTE_ADDR']``

* Also in PrefixMiddleware, if X-Forwarded-Host has multiple
  (comma-separated) values, use only the first value.

1.3.2
-----

* Added ``paste.deploy.converters.asint()``.
* fixed use sections overwriting the config's __file__ value with the
  use'd filename.
* ``paste.deploy.loadwsgi`` now supports variable expansion in the
  DEFAULT section of config files (unlike plain ConfigParser).

1.3.1
-----

* Fix ``appconfig`` config loading when using a config file with
  ``filter-with`` in it (previously you'd get TypeError: iteration
  over non-sequence)

1.3
---

* Added ``scheme`` option to ``PrefixMiddleware``, so you can force a
  scheme (E.g., when proxying an HTTPS connection over HTTP).

* Pop proper values into ``environ['paste.config']`` in
  ``ConfigMiddleware``.

1.1
---

* Any ``global_conf`` extra keys you pass to ``loadapp`` (or the other
  loaders) will show up as though they were in ``[DEFAULT]``, so they
  can be used in variable interpolation.  Note: this won't overwrite
  any existing values in ``[DEFAULT]``.

* Added ``force_port`` option to
  ``paste.deploy.config.PrefixMiddleware``.  Also the ``prefix``
  argument is stripped of any trailing ``/``, which can't be valid in
  that position.

1.0
---

* Added some documentation for the different kinds of entry points
  Paste Deploy uses.

* Added a feature to ``PrefixMiddleware`` that translates the
  ``X-Forwarded-Server`` header to ``Host``.

0.9.6
-----

* Added ``PrefixMiddleware`` which compensates for cases where the
  wsgi app is behind a proxy of some sort that isn't moving the prefix
  into the SCRIPT_NAME in advance.

* Changed _loadconfig() so that it works with Windows absolute paths.

* Make the error messages prettier when you call a function and fail
  to give an argument, like a required function argument.

0.5
---

* Made the ``paste_deploy`` template (used with ``paster create
  --template=paste_deploy``) more useful, with an example application
  and entry point.

0.4
---

* Allow filters to have ``filter-with`` values, just like
  applications.

* Renamed ``composit`` to ``composite`` (old names still work, but
  aren't documented).

* Added ``appconfig()`` to load along with ``loadapp()``, but return
  the configuration without invoking the application.

0.3
---

* Allow variable setting like::

    get local_var = global_var_name

  To bring in global variables to the local scope.

* Allow interpolation in files, like ``%(here)s``.  Anything in the
  ``[DEFAULTS]`` section will be available to substitute into a value,
  as will variables in the same section.  Also, the special value
  ``here`` will be the directory the configuration file is located in.

0.2
---

Released 26 August 2004

* Added a ``filter-with`` setting to applications.

* Removed the ``1`` from all the protocol names (e.g.,
  ``paste.app_factory1`` is not ``paste.app_factory``).

* Added ``filter-app:`` and ``pipeline:`` sections.

* Added ``paste.filter_app_factory1`` and ``paste.server_runner1`` protocols.

* Added ``paste.deploy.converters`` module for handling the
  string values that are common with this system.

0.1
---

Released 22 August 2004

Initial version released.  It's all new.
