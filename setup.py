from setuptools import setup, find_packages

version = '0.9.7'

setup(
    name="PasteDeploy",
    version=version,
    description="Load, configure, and compose WSGI applications and servers",
    long_description="""\
This tool provides code to load WSGI applications and servers from
URIs; these URIs can refer to Python Eggs for INI-style configuration
files.  `Paste Script <http://pythonpaste.org/script>`_ provides
commands to serve applications based on this configuration file.

The latest version is available in a `Subversion repository
<http://svn.pythonpaste.org/Paste/Deploy/trunk#egg=PasteDeploy-dev>`_.

For the latest changes see the `news file
<http://pythonpaste.org/deploy/news.html>`_.
""",
    classifiers=["Development Status :: 4 - Beta",
                 "Intended Audience :: Developers",
                 "License :: OSI Approved :: Python Software Foundation License",
                 "Programming Language :: Python",
                 "Topic :: Internet :: WWW/HTTP",
                 "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
                 "Topic :: Software Development :: Libraries :: Python Modules",
                 ],
    keywords='web wsgi application server',
    author="Ian Bicking",
    author_email="ianb@colorstudy.com",
    url="http://pythonpaste.org/deploy/",
    license='MIT',
    namespace_packages=['paste'],
    packages=find_packages(exclude='tests'),
    package_data={
      'paste.deploy': ['paster_templates/paste_deploy/docs/*_tmpl',
                       'paster_templates/paste_deploy/docs/*.txt'],
      },
    zip_safe=False,
    extras_require={
      'Config': [],
      'Paste': ['Paste'],
      },
    entry_points="""
    [paste.filter_app_factory]
    config = paste.deploy.config:make_config_filter [Config]
    prefix = paste.deploy.config:PrefixMiddleware

    [paste.paster_create_template]
    paste_deploy=paste.deploy.paster_templates:PasteDeploy
    """,
    )
