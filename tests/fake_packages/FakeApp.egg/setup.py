from setuptools import setup, find_packages

setup(
    name="FakeApp",
    version="1.0",
    packages=find_packages(),
    entry_points={
      'paste.app_factory': """
      basic_app=fakeapp.apps:make_basic_app
      other=fakeapp.apps:make_basic_app2
      configed=fakeapp.configapps:SimpleApp.make_app
      """,
      'paste.composit_factory': """
      remote_addr=fakeapp.apps:make_remote_addr
      """,
      'paste.filter_factory': """
      caps=fakeapp.apps:make_cap_filter
      """,
      'paste.filter_app_factory': """
      caps2=fakeapp.apps:CapFilter
      """,
      },
    )
