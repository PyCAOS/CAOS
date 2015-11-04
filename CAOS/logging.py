class DummyLogger(object):
    """Fake logger I'm going to use for now. Will return something valid
    in all cases.
    """

    def __getattr__(self, name, default=None):
        def _(*a, **kw):
            pass
        return _

logger = DummyLogger()
