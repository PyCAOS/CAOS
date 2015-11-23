"""Singleton logging for the language.

When verbose mode is enabled, logged messages are written to stdout or
stderr, depending on the type of message.  Otherwise non-error messages
are suppressed.

Attributes
----------
LoggingLevelEnum : Enum
    Logging levels - available levels are DEBUG, INFO, WARN, and ERROR.
"""

from __future__ import print_function, division, unicode_literals, \
    absolute_import

from .compatibility import StringIO

import sys

try:
    from enum import IntEnum
except ImportError:
    raise ImportError(
        "You need to install the enum34 package for Python versions < 3.4"
    )


class LoggingLevelEnum(IntEnum):
    DEBUG = 1
    INFO = 2

fake_out = StringIO()
fake_err = StringIO()

logger = None


def get_logger(verbose, level=LoggingLevelEnum.INFO):
    """Get a singleton logger for the given level and verbosity.

    Parameters
    ----------
    verbose : bool
        Whether or not verbose mode is enabled.
    level : Optional[LoggingLevelEnum]
        The logging  level to be used.  Defaults to INFO.

    Returns
    -------
    logger : Logger
        The logger object, set the the appropriate logging level.
    """

    global logger

    if logger is None:
        if verbose:
            logger = VerboseLogger(sys.stdout, sys.stderr, level)
        else:
            logger = DefaultLogger(fake_out, fake_err, level)

    logger.level = level

    return logger


class Logger(object):
    """Base logging class."""

    def __init__(self, out_stream, err_stream, level=LoggingLevelEnum.INFO):
        """Create a logger object.

        Parameters
        ----------
        out_stream : file-like
            Standard output stream for non-errors.
        err_stream : file-like
            Standard error stream for error messages.
        level : Optional[LoggingLevelEnum]
            The logging level to be used.
        """

        self.out = out_stream
        self.err = err_stream
        self.level = level

    def debug(self, message):
        """Write a debugging message to the output stream.

        Parameters
        ----------
        message : str
            The message to be written.
        """

        if self.level == LoggingLevelEnum.DEBUG:
            self.log(message, self.out)

    def info(self, message):
        """Write an informative message to the output stream.

        Parameters
        ----------
        message : str
            The message to be written
        """

        if self.level <= LoggingLevelEnum.INFO:
            self.log(message, self.out)

    def log(self, message, stream=None):
        """Log a message to a given stream.

        Parameters
        ----------
        message : str
            The message to log.
        stream : Optiona[file-like]
            The stream to write to.
        """

        if not stream:
            stream = self.out

        stream.write(message)

    def warn(self, message):
        """Write a warning to the error stream.

        Parameters
        ----------
        message : str
            The warning message.
        """

        self.log(message, self.err)

    def error(self, message):
        """Write an error message to the error stream.

        Parameters
        ----------
        message : str
            The error message.
        """

        self.log(message, self.err)


class DefaultLogger(Logger):
    """Default logger for non-verbose mode."""

    def __init__(self, out=fake_out, err=sys.stderr,
                 level=LoggingLevelEnum.INFO):
        """Creates a default logger.

        Parameters
        ----------
        out, err : Optional[file-like]
            Streams to write to. Defaults to a dummy output stream, and
            `sys.stderr`, respectively.
        level : Optional[LoggingLevelEnum]
            Logging level to use.
        """

        super(DefaultLogger, self).__init__(out, err, level)


class VerboseLogger(Logger):
    """Verbose mode logger."""

    def __init__(self, out=sys.stdout, err=sys.stderr,
                 level=LoggingLevelEnum.DEBUG):
        """Creates a verbose logger.

        Parameters
        ----------
        out, err : Optional[file-like]
            Streams to write to. Defaults to `sys.stdout` and
            `sys.stderr`, respectively.
        level : Optional[LoggingLevelEnum]
            Logging level to use.
        """

        super(VerboseLogger, self).__init__(out, err, level)
