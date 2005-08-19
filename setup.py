from setuptools import setup, find_packages

setup(
    name="Paste-Deploy",
    version="0.1",
    namespace_packages=['paste'],
    packages=find_packages(exclude='tests'),
    )
