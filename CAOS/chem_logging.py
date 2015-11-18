"""Singleton logging for the language.

When verbose mode is enabled, logged messages are written to stdout or
stderr, depending on the type of message.  Otherwise messages are
suppressed.

Attributes
----------
LEVEL_ENUM : Enum
    Logging levels - available levels are DEBUG, INFO, WARN, and ERROR.
"""

from __future__ import print_function, division, unicode_literals, \
    absolute_import

from .compatibility import StringIO

import sys

from enum import Enum


LEVEL_ENUM = Enum("LEVEL_ENUM", "DEBUG INFO WARN ERROR")

fake_out = StringIO()
fake_err = StringIO()

logger = None


def get_logger(verbose, level=LEVEL_ENUM.INFO):
    """Get a singleton logger for the given level and verbosity.

    Parameters
    ----------
    verbose : bool
        Whether or not verbose mode is enabled.
    level : Optional[LEVEL_ENUM]
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

    def __init__(self, out_stream, err_stream, level=LEVEL_ENUM.INFO):
        """Create a logger object.

        Parameters
        ----------
        out_stream : file-like
            Standard output stream for non-errors.
        err_stream : file-like
            Standard error stream for error messages.
        level : Optional[LEVEL_ENUM]
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

        if self.level is LEVEL_ENUM.DEBUG:
            self.log(message, self.out)

    def info(self, message):
        """Write an informative message to the output stream.

        Parameters
        ----------
        message : str
            The message to be written
        """

        if self.level <= LEVEL_ENUM:
            self.log(message, self.out)

    def log(self, message):
        """"""
        pass

    def warn(self, message):
        pass

    def error(self, message):
        pass


class DefaultLogger(Logger): 
    pass


class VerboseLogger(Logger): 
    pass
