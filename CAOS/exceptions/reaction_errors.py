"""Reaction errors; i.e. those that occur during a reaction."""


from __future__ import print_function, division, unicode_literals


class FailedReactionError(Exception):
    """Indicates that a reaction failed to occur."""

    pass
