"""Reaction errors; i.e. those that occur during a reaction."""

from __future__ import print_function, division, unicode_literals, \
    absolute_import
from future.builtins import *  # noqa
from future.builtins.disabled import *  # noqa


class FailedReactionError(Exception):
    """Indicates that a reaction failed to occur."""

    pass
