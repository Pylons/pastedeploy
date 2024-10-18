from setuptools import find_packages, setup

setup(
    name="FakeJsonLoader",
    version="1.0",
    packages=find_packages(),
    entry_points={
        "paste.config_factory": [
            "config+json = fakejsonloader:load_json",
        ],
    },
)
