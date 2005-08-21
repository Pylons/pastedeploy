from setuptools import setup, find_packages

setup(
    name="Paste-Deploy",
    version="0.1",
    description="Load, configure, and compose WSGI applications and servers",
    long_description="""\
This tool provides code to load WSGI applications and servers from
URIs; these URIs can refer to Python Eggs for INI-style configuration
files.
""",
    classifiers=["Development Status :: 3 - Alpha",
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
    url="http://pythonpaste.org",
    namespace_packages=['paste'],
    extras_require={'composit': ['Paste']},
    packages=find_packages(exclude='tests'),
    zip_safe=True,
    )
