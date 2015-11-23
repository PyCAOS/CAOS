"""Compatibility file to match functionality between py2 and 3."""

from __future__ import print_function, division, unicode_literals, \
    absolute_import

import itertools
import sys

try:
    range = xrange
except NameError:
    range = range

try:
    str = unicode
except NameError:
    str = str

try:
    long
except NameError:
    long = int

try:
    from io import StringIO
except ImportError:
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO

if sys.version[0] == 2:
    map = itertools.imap
    zip = itertools.izip

del sys
del itertools
