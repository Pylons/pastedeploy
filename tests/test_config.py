import os
from paste.deploy import loadapp, loadfilter, appconfig
from fixture import *
import fakeapp.configapps as fc

ini_file = 'config:sample_configs/test_config.ini'
here = os.path.dirname(__file__)
config_path = os.path.join(here, 'sample_configs')

def test_config_egg():
    app = loadapp('egg:FakeApp#configed')
    assert isinstance(app, fc.SimpleApp)
    
def test_config1():
    app = loadapp(ini_file, relative_to=here, name='test1')
    assert app.local_conf == {
        'setting1': 'foo', 'setting2': 'bar'}
    assert app.global_conf == {
        'def1': 'a', 'def2': 'b',
        'here': config_path}

def test_config2():
    app = loadapp(ini_file, relative_to=here, name='test2')
    assert app.local_conf == {
        'local conf': 'something'}
    assert app.global_conf == {
        'def1': 'test2',
        'def2': 'b',
        'another': 'TEST',
        'here': config_path}
    # Run this to make sure the global-conf-modified test2
    # didn't mess up the general global conf
    test_config1()

def test_config3():
    app = loadapp(ini_file, relative_to=here, name='test3')
    assert isinstance(app, fc.SimpleApp)
    assert app.local_conf == {
        'local conf': 'something',
        'another': 'something more\nacross several\nlines'}
    assert app.global_conf == {
        'def1': 'test3',
        'def2': 'b',
        'another': 'TEST',
        'here': config_path}
    test_config2()
    
def test_foreign_config():
    app = loadapp(ini_file, relative_to=here, name='test_foreign_config')
    assert isinstance(app, fc.SimpleApp)
    assert app.local_conf == {
        'another': 'FOO',
        'bob': 'your uncle'}
    assert app.global_conf == {
        'def1': 'a',
        'def2': 'from include',
        'def3': 'c',
        'glob': 'override',
        'here': config_path}
    
def test_config_get():
    app = loadapp(ini_file, relative_to=here, name='test_get')
    assert isinstance(app, fc.SimpleApp)
    assert app.local_conf == {
        'def1': 'a',
        'foo': 'TEST'}
    assert app.global_conf == {
        'def1': 'a',
        'def2': 'TEST',
        'here': config_path}

def test_appconfig():
    conf = appconfig(ini_file, relative_to=here, name='test_get')
    assert conf == {
        'def1': 'a',
        'def2': 'TEST',
        'here': config_path,
        'foo': 'TEST'}
    assert conf.local_conf == {
        'def1': 'a',
        'foo': 'TEST'}
    assert conf.global_conf == {
        'def1': 'a',
        'def2': 'TEST',
        'here': config_path}
