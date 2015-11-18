"""Errors that occur while dispatching the mechanism or type."""

from __future__ import print_function, division, unicode_literals, \
    absolute_import


class DispatchException(Exception):
    """Generic error raised when some problem occurs during dispatch."""

    pass


class ExistingReactionError(DispatchException):
    """A mechanism with this name has already been registered."""

    pass


class InvalidReactionError(DispatchException):
    """The reaction being registered is invalid in some way."""

    pass
