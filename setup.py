from setuptools import setup, find_packages

version = '0.4'

setup(
    name="PasteDeploy",
    version=version,
    description="Load, configure, and compose WSGI applications and servers",
    long_description="""\
This tool provides code to load WSGI applications and servers from
URIs; these URIs can refer to Python Eggs for INI-style configuration
files.  

See also the `Subversion repository <http://svn.pythonpaste.org/Paste/Deploy/trunk#egg=Paste-Deploy-%sdev>`_
""" % version,
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
    namespace_packages=['paste'],
    packages=find_packages(exclude='tests'),
    package_data={
      'paste.deploy': ['paster_templates/paste_deploy/docs/*_tmpl',
                       'paster_templates/paste_deploy/docs/*.txt'],
      },
    zip_safe=False,
    extras_require={
      'Config': ['Paste'],
      'Paste': ['Paste'],
      },
    entry_points="""
    [distutils.commands]
    tag = paste.deploy.tag:tag

    [paste.filter_app_factory]
    config = paste.deploy.config:make_config_filter [Config]

    [paste.paster_create_template]
    paste_deploy=paste.deploy.paster_templates:PasteDeploy
    """,
    )
