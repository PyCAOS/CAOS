"""Singleton logging for the language.

When verbose mode is enabled, logged messages are written to stdout or
stderr, depending on the type of message.  Otherwise they are ignored.
"""


class DummyLogger(object):
    """Fake logger I'm going to use for now.

    Will return something valid in all cases.
    """

    def __getattr__(self, name, default=None):
        """Return a function that can take anything as a parameter."""

        def _(*a, **kw):
            pass
        return _

    def __setattr__(self, name, value):
        """"Set" a value."""

        pass

logger = DummyLogger()
