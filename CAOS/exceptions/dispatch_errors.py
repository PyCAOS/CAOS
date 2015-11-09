"""Errors that occur while dispatching the mechanism or type."""


class DispatchException(Exception):
    """Generic error raised when some problem occurs during dispatch."""

    def __init__(self, message, *args, **kwargs):
        """Create the error."""

        super(DispatchException, self).__init__(message, *args, **kwargs)


class ExistingReactionError(DispatchException):
    """A mechanism with this name has already been registered."""

    pass


class InvalidReactionError(DispatchException):
    """The reaction being registered is invalid in some way."""

    pass
