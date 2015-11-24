"""CAOS module."""

from __future__ import print_function, division, unicode_literals, \
    absolute_import

import argparse

import six

from .logging import get_logger


__version__ = "0.4.0"
__author__ = "Dan Obermiller"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Predict an organic chemistry reaction using the CAOS tool"
                    ", powered by Python"
    )

    parser.add_argument(
        'source', type=str,
        help="The source file for the reaction."
    )
    parser.add_argument(
        '-v', '--verbose', dest='verbose', action='store_true', default=False,
        help="Set the program to run in verbose mode."
    )

    args = parser.parse_args()

    if 'verbose' not in globals():
        verbose = args.verbose
elif 'verbose' not in globals():
    verbose = False

logger = get_logger(verbose)

from .dispatch import register_reaction_mechanism
from . import mechanisms 

for mechanism_name, values in six.iteritems(mechanisms.__mechanisms__):
    registrar = register_reaction_mechanism(values['requirements'])
    registrar(values['function'])
