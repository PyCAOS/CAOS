from CAOS.util import raises


def test_raises_false():
    function = int
    args = [3]
    exception_type = ValueError
    assert not raises(exception_type, function, args)


def test_raises_true():
    function = int
    args = ["hello"]
    exception_type = ValueError
    assert raises(exception_type, function, args)


def test_raises_error():
    function = int
    args = ["hello"]
    exception_type = UnboundLocalError
    assert raises(ValueError, raises, (exception_type, function, args))
