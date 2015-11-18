from __future__ import print_function, division, unicode_literals

from CAOS.dispatch import register_reaction_mechanism, reaction_is_registered, \
    ReactionDispatcher, react
from CAOS.util import raises
from CAOS.exceptions.dispatch_errors import InvalidReactionError, \
    ExistingReactionError


def teardown_module():
    for key in map('reaction {}'.format, [1, 2, 4]):
        del ReactionDispatcher._mechanism_namespace[key]


def test_register_simple_reaction():
    @register_reaction_mechanism('reaction 1', {})
    def reaction1(reactants, conditions):
        return 42

    assert reaction_is_registered('reaction 1')
    assert reaction_is_registered(reaction1)


def test_register_simple_reaction_with_requirements():
    def magic(reactants, conditions):
        return reactants and conditions

    @register_reaction_mechanism('reaction 2', {'magic': magic})
    def reaction2(reactants, conditions):
        return 36

    assert reaction_is_registered('reaction 2')
    assert reaction_is_registered(reaction2)


def test_register_simple_reaction_with_invalid_requirements():
    voodoo = 17
    function = register_reaction_mechanism
    args = ['reaction 3', {'voodoo': voodoo}]

    def reaction3(reactants, conditions):
        return 11

    assert raises(InvalidReactionError, function, args)
    assert not reaction_is_registered('reaction 3')
    assert not reaction_is_registered(reaction3)


def test_register_existing_reaction():
    function = register_reaction_mechanism
    args = ['reaction 2', {}]

    assert raises(ExistingReactionError, function, args)


def test_mechanism_not_modified_by_decorator():
    def myfunction(*args):
        return 42

    decorated = register_reaction_mechanism('reaction 4', {})(myfunction)
    assert myfunction is decorated
    assert myfunction() == decorated()

    assert reaction_is_registered('reaction 4')
    assert reaction_is_registered(myfunction)
