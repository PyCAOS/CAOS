class FailedReactionError(Exception):

    def __init__(self, message, *args, **kwargs):
        super(FailedReactionError, self).__init__(message, *args, **kwargs)
