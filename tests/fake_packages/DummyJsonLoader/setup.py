from setuptools import find_packages, setup

setup(
    name="JsonLoader",
    version="1.0",
    packages=find_packages(),
    entry_points={
        "paste.config_factory": [
            "config+json = jsonloader:JsonPasteDeployLoader",
        ],
    },
)
