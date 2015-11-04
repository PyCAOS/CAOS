class DispatchException(Exception):

    def __init__(self, message, *args, **kwargs):
        super(DispatchException, self).__init__(message, *args, **kwargs)


class ExistingReactionError(DispatchException):
    pass


class InvalidReactionError(DispatchException):
    pass
