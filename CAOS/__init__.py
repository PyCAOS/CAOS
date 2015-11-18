"""CAOS module."""


from __future__ import print_function, division, unicode_literals, \
    absolute_import

import argparse

from .chem_logging import get_logger


__version__ = "0.2.1"
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
