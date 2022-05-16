def test_asbool_truthy():
    from paste.deploy.converters import asbool

    assert asbool('true')
    assert asbool('yes')
    assert asbool('on')
    assert asbool('y')
    assert asbool('t')
    assert asbool('1')


def test_asbool_falsy():
    from paste.deploy.converters import asbool

    assert not asbool('false')
    assert not asbool('no')
    assert not asbool('off')
    assert not asbool('n')
    assert not asbool('f')
    assert not asbool('0')
