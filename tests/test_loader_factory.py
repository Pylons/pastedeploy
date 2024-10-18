import sys
from pathlib import Path

import pytest
from paste.deploy import loadapp

import fakeapp.apps


here = Path(__file__).parent


@pytest.fixture(scope="module", autouse=True)
def fake_package_path():
    fake_packages_path = here / "fake_packages" / "DummyJsonLoader"
    sys.path.insert(0, str(fake_packages_path))
    yield
    sys.path.pop(0)


def test_load_json():
    app = loadapp("config+json:sample_configs/basic_app.json", relative_to=str(here))
    assert app is fakeapp.apps.basic_app


def test_lookup_error():
    with pytest.raises(LookupError) as ctx:
        loadapp("config+xml:sample_configs/basic_app.xml", relative_to=str(here))
    assert (
        str(ctx.value) == "URI scheme not known: 'config+xml' (from config, egg, call)"
    )
