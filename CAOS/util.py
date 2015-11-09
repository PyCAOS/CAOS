"""Utility functions that aren't core functionality."""


def raises(exception_types, function, args=None, kwargs=None):
    """Return whether or not the given function raises the error.

    Parameters
    ==========
    exception_types: tuple, Exception
        Tuple of the types of the exceptions (or a single type of
        exception) that should be caught.
    function: callable
        The function to be called
    args: collection, optional
        List of positional arguments to be used
    kwargs: mapping, optional
        Dictionary of keyword arguments to be used

    Examples
    ========
    It should return `False` when given a valid value

    >>> raises(ValueError, int, ["3"])
    False

    It should return `True` when given an invalid value that results in
    the expected error

    >>> raises(ValueError, int, ["hello"])
    True

    It should raise an error if it gets an unexpected error

    >>> raises(UnboundLocalError, int, ["hello"])
    Traceback (most recent call last):
        ...
    ValueError: invalid literal for int() with base 10: 'hello'
    """

    args = args if args is not None else []
    kwargs = kwargs if kwargs is not None else {}
    try:
        function(*args, **kwargs)
    except exception_types:
        return True
    else:
        return False
