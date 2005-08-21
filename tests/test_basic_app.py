from paste.deploy import loadwsgi
from fixture import *
import fakeapp.apps

def test_main():
    app = loadtest('basic_app.ini')
    assert app is fakeapp.apps.basic_app

def test_other():
    app = loadtest('basic_app.ini', name='other')
    assert app is fakeapp.apps.basic_app2
    
