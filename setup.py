import os

from setuptools import setup, find_packages

here = os.path.dirname(__file__)
readme_path = os.path.join(here, "README.rst")
readme = open(readme_path).read()

docs_extras = [
    'Sphinx >= 1.7.5',  # Read The Docs minimum version
    'pylons-sphinx-themes',
]

setup(
    name='PasteDeploy',
    version='1.5.2',
    description='Load, configure, and compose WSGI applications and servers',
    long_description=readme,
    classifiers=[
        'Development Status :: 6 - Mature',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Framework :: Paste',
    ],
    keywords='web wsgi application server',
    author='Ian Bicking',
    author_email='ianb@colorstudy.com',
    maintainer='Alex Gronholm',
    maintainer_email='alex.gronholm@nextday.fi',
    url="https://pylonsproject.org/",
    project_urls={
        "Documentation": "https://docs.pylonsproject.org/projects/pastedeploy/en/latest/",
        "Changelog": "https://docs.pylonsproject.org/projects/pastedeploy/en/latest/news.html",
        "Issue Tracker": "https://github.com/Pylons/pastedeploy/issues",
    },
    license='MIT',
    namespace_packages=['paste'],
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    extras_require={
        'Config': [],
        'Paste': ['Paste'],
        'docs': docs_extras,
    },
    entry_points="""
    [paste.filter_app_factory]
    config = paste.deploy.config:make_config_filter [Config]
    prefix = paste.deploy.config:make_prefix_middleware

    [paste.paster_create_template]
    paste_deploy=paste.deploy.paster_templates:PasteDeploy
    """
)
