"""Mechanisms for the CAOS system."""

from __future__ import print_function, division, unicode_literals, \
    absolute_import

from importlib import import_module

from . import requirements


__mechanism_names__ = ('acid_base',)

__mechanisms__ = {}


for mechanism_name in __mechanism_names__:
    mechanism_module = import_module(
        ".{0}".format(mechanism_name), package="CAOS.mechanisms"
    )
    function_requirements = [
        getattr(requirements, requirement_name)
        for requirement_name in mechanism_module.__requirements__
    ]
    mechanism_function = getattr(
        mechanism_module, "{0}_reaction".format(mechanism_name)    )
    print(type(mechanism_function))
    __mechanisms__[mechanism_name] = {
        'function': mechanism_function,
        'requirements': function_requirements
    }
