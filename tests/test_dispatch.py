from __future__ import print_function, division, unicode_literals, \
    absolute_import

from CAOS.dispatch import register_reaction_mechanism, reaction_is_registered, \
    ReactionDispatcher, react
from CAOS.util import raises
from CAOS.exceptions.dispatch_errors import InvalidReactionError, \
    ExistingReactionError


def teardown_module():
    for key in map('reaction{}'.format, [1, 2, 4]):
        del ReactionDispatcher._mechanism_namespace[key]


def test_register_simple_reaction():
    @register_reaction_mechanism([])
    def reaction1(reactants, conditions):
        return 42

    assert reaction_is_registered('reaction1')
    assert reaction_is_registered(reaction1)


def test_register_simple_reaction_with_requirements():
    def magic(reactants, conditions):
        return reactants and conditions

    @register_reaction_mechanism([magic])
    def reaction2(reactants, conditions):
        return 36

    assert reaction_is_registered('reaction2')
    assert reaction_is_registered(reaction2)


def test_register_simple_reaction_with_invalid_requirements():
    voodoo = 17
    function = register_reaction_mechanism([voodoo])

    def reaction3(reactants, conditions):
        return 11

    args = [reaction3]

    assert raises(InvalidReactionError, function, args)
    assert not reaction_is_registered('reaction3')
    assert not reaction_is_registered(reaction3)


def test_register_existing_reaction():
    function = register_reaction_mechanism([])

    def reaction2(*args):
        pass

    args = [reaction2]

    assert raises(ExistingReactionError, function, args)


def test_mechanism_not_modified_by_decorator():
    def reaction4(*args):
        return 42

    decorated = register_reaction_mechanism([])(reaction4)
    assert reaction4 is decorated
    assert reaction4() == decorated()

    assert reaction_is_registered('reaction4')
    assert reaction_is_registered(reaction4)
