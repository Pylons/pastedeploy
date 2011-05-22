from nose.tools import eq_

from paste.deploy import loadapp, appconfig
from tests.fixture import *
import fakeapp.configapps as fc


ini_file = 'config:sample_configs/test_config.ini'
here = os.path.dirname(__file__)
config_path = os.path.join(here, 'sample_configs')
config_filename = os.path.join(config_path, 'test_config.ini')


def test_config_egg():
    app = loadapp('egg:FakeApp#configed')
    assert isinstance(app, fc.SimpleApp)


def test_config1():
    app = loadapp(ini_file, relative_to=here, name='test1')
    eq_(app.local_conf, {
        'setting1': 'foo',
        'setting2': 'bar',
        'apppath': os.path.join(config_path, 'app')})
    eq_(app.global_conf, {
        'def1': 'a',
        'def2': 'b',
        'basepath': config_path,
        'here': config_path,
        '__file__': config_filename})


def test_config2():
    app = loadapp(ini_file, relative_to=here, name='test2')
    eq_(app.local_conf, {
        'local conf': 'something'})
    eq_(app.global_conf, {
        'def1': 'test2',
        'def2': 'b',
        'basepath': config_path,
        'another': 'TEST',
        'here': config_path,
        '__file__': config_filename})
    # Run this to make sure the global-conf-modified test2
    # didn't mess up the general global conf
    test_config1()


def test_config3():
    app = loadapp(ini_file, relative_to=here, name='test3')
    assert isinstance(app, fc.SimpleApp)
    eq_(app.local_conf, {
        'local conf': 'something',
        'another': 'something more\nacross several\nlines'})
    eq_(app.global_conf, {
        'def1': 'test3',
        'def2': 'b',
        'basepath': config_path,
        'another': 'TEST',
        'here': config_path,
        '__file__': config_filename})
    test_config2()


def test_foreign_config():
    app = loadapp(ini_file, relative_to=here, name='test_foreign_config')
    assert isinstance(app, fc.SimpleApp)
    eq_(app.local_conf, {
        'another': 'FOO',
        'bob': 'your uncle'})
    eq_(app.global_conf, {
        'def1': 'a',
        'def2': 'from include',
        'def3': 'c',
        'basepath': config_path,
        'glob': 'override',
        'here': config_path,
        '__file__': os.path.join(config_path, 'test_config.ini')})


def test_config_get():
    app = loadapp(ini_file, relative_to=here, name='test_get')
    assert isinstance(app, fc.SimpleApp)
    eq_(app.local_conf, {
        'def1': 'a',
        'foo': 'TEST'})
    eq_(app.global_conf, {
        'def1': 'a',
        'def2': 'TEST',
        'basepath': os.path.join(here, 'sample_configs'),
        'here': config_path,
        '__file__': config_filename})


def test_appconfig():
    conf = appconfig(ini_file, relative_to=here, name='test_get')
    eq_(conf, {
        'def1': 'a',
        'def2': 'TEST',
        'basepath': os.path.join(here, 'sample_configs'),
        'here': config_path,
        '__file__': config_filename,
        'foo': 'TEST'})
    eq_(conf.local_conf, {
        'def1': 'a',
        'foo': 'TEST'})
    eq_(conf.global_conf, {
        'def1': 'a',
        'def2': 'TEST',
        'basepath': os.path.join(here, 'sample_configs'),
        'here': config_path,
        '__file__': config_filename})


def test_appconfig_filter_with():
    conf = appconfig('config:test_filter_with.ini', relative_to=config_path)
    eq_(conf['example'], 'test')


def test_global_conf():
    conf = appconfig(ini_file, relative_to=here, name='test_global_conf',
                     global_conf={'def2': 'TEST DEF 2', 'inherit': 'bazbar'})
    eq_(conf, {
        'def1': 'a',
        # Note that this gets overwritten:
        'def2': 'b',
        'basepath': os.path.join(here, 'sample_configs'),
        'here': config_path,
        'inherit': 'bazbar',
        '__file__': config_filename,
        'test_interp': 'this:bazbar',
        })
    eq_(conf.local_conf, {
        'test_interp': 'this:bazbar'})


def test_interpolate_exception():
    try:
        appconfig('config:test_error.ini', relative_to=config_path)
    except Exception:
        e = sys.exc_info()[1]
        expected = "Error in file %s" % os.path.join(config_path, 'test_error.ini')
        eq_(str(e).split(',')[0], expected)
    else:
        assert False, 'Should have raised an exception'
