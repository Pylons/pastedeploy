from setuptools import setup, find_packages

setup(
    name="FakeApp",
    version="1.0",
    packages=find_packages(),
    entry_points={
      'paste.app_factory1': """
      basic_app=fakeapp.apps:make_basic_app
      other=fakeapp.apps:make_basic_app2
      """,
      'paste.composit_factory1': """
      remote_addr=fakeapp.apps:make_remote_addr
      """,
      },
    )
