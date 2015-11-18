from __future__ import print_function, division, unicode_literals, \
    absolute_import

try:
    range = xrange
except NameError:
    range = range

try:
    str = unicode
except NameError:
    str = str

try:
    from io import StringIO
except ImportError:
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO
