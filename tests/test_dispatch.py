from __future__ import print_function, division, unicode_literals, \
    absolute_import
from future.builtins import *  # noqa
from future.builtins.disabled import *  # noqa

from CAOS.dispatch import register_reaction_mechanism, reaction_is_registered, \
    ReactionDispatcher, react
from CAOS.util import raises
from CAOS.exceptions.dispatch_errors import InvalidReactionError, \
    ExistingReactionError


def teardown_module():
    for key in map('reaction{0}'.format, [1, 2, 4]):
        del ReactionDispatcher._test_namespace[key]


def vacuous(*_, **__):
    return True


def test_register_simple_reaction():
    @register_reaction_mechanism([vacuous], True)
    def reaction1(reactants, conditions):
        return 42

    assert reaction_is_registered('reaction1', True)
    assert reaction_is_registered(reaction1, True)


def test_register_simple_reaction_with_requirements():
    def magic(reactants, conditions):
        return reactants and conditions

    @register_reaction_mechanism([magic], True)
    def reaction2(reactants, conditions):
        return 36

    assert reaction_is_registered('reaction2', True)
    assert reaction_is_registered(reaction2, True)


def test_register_simple_reaction_with_invalid_requirements():
    voodoo = 17
    function = register_reaction_mechanism([voodoo], True)

    def reaction3(reactants, conditions):
        return 11

    args = [reaction3]

    assert raises(InvalidReactionError, function, args)
    assert not reaction_is_registered('reaction3', True)
    assert not reaction_is_registered(reaction3, True)


def test_register_existing_reaction():
    function = register_reaction_mechanism([vacuous], True)

    def reaction2(*args):
        pass

    args = [reaction2]

    assert raises(ExistingReactionError, function, args)


def test_mechanism_not_modified_by_decorator():
    def reaction4(*args):
        return 42

    decorated = register_reaction_mechanism([vacuous], True)(reaction4)
    assert reaction4 is decorated
    assert reaction4() == decorated()

    assert reaction_is_registered('reaction4', True)
    assert reaction_is_registered(reaction4, True)


def test_no_requirements_error():
    registrator = register_reaction_mechanism([], True)
    assert raises(InvalidReactionError, registrator, ((lambda x, y: None),))


def test_not_callable_has_name():
    class _(object):
        __name__ = 'dumb'

    registrator = register_reaction_mechanism([_()], True)

    assert raises(InvalidReactionError, registrator, ((lambda x, y: None),))
