"""Reaction errors; i.e. those that occur during a reaction."""


class FailedReactionError(Exception):
    """Indicates that a reaction failed to occur."""

    def __init__(self, message, *args, **kwargs):
        """Create a new error."""

        super(FailedReactionError, self).__init__(message, *args, **kwargs)
