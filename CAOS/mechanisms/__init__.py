"""Mechanisms for the CAOS system."""

from __future__ import print_function, division, unicode_literals, \
    absolute_import

from importlib import import_module

from ..dispatch import register_reaction_mechanism
from CAOS import requirements

__mechanisms__ = ('acid_base',)


for mechanism in __mechanisms__:
    mechanism_module = import_module(
        ".{}".format(mechanism), package="CAOS.mechanisms"
    )

    function_requirements = [
        getattr(requirements, requirement_name)
        for requirement_name in mechanism_module.__requirements__
    ]
    registrator = register_reaction_mechanism(function_requirements)
    mechanism_function = getattr(
        mechanism_module, "{}_reaction".format(mechanism)
    )
    registrator(mechanism_function)
