Custom Paste File Format
========================

paste original file format is `.ini` and implement only the ini
file format.

But developpers can register a ``paste.app_factory`` entrypoint to define
new file format.

Here is an example on how to register a ``.json`` configuration file format.

.. literalinclude:: ../../tests/fake_packages/DummyJsonLoader/setup.py

Now, some code needs to be written in order to load the config from the
this file format. The class ``AbstractLoader`` has to be implemented
for the type registered in the registered ``paste.app_factory`` entrypoint.

.. autoclass:: paste.deploy.loadwsgi.AbstractLoader


To follow our json example, we can load the app from a json file:

.. literalinclude:: ../../tests/fake_packages/DummyJsonLoader/jsonloader/__init__.py

Now, the paste config can be spefide using the `config+json:` prefix while
specifying the paste prefix.


Here is an example of using ``paste.deploy`` with uwsgi using the registered json
file format.

::

   $ uwsgi --paste config+json:/path/to/config.ini ...
