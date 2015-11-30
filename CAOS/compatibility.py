"""Compatibility file to match functionality between py2 and 3."""

from __future__ import print_function, division, unicode_literals, \
    absolute_import
from future.builtins import *
from future.builtins.disabled import *


try:
    from io import StringIO
except ImportError:
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO
