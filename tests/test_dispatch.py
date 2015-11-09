from CAOS.dispatch import register_reaction_mechanism
from CAOS.util import raises
from CAOS.exceptions.dispatch_errors import InvalidReactionError, \
    ExistingReactionError


def test_register_simple_reaction():
    @register_reaction_mechanism('reaction 1', {})
    def reaction1(reactants, conditions):
        return 42

    assert 'reaction 1' in register_reaction_mechanism.mechanism_namespace


def test_register_simple_reaction_with_requirements():
    def magic(reactants, conditions):
        return reactants and conditions

    @register_reaction_mechanism('reaction 2', {'magic': magic})
    def reaction2(reactants, conditions):
        return 36

    assert 'reaction 2' in register_reaction_mechanism.mechanism_namespace


def test_register_simple_reaction_with_invalid_requirements():
    voodoo = 17
    function = register_reaction_mechanism
    args = ['reaction 3', {'voodoo': voodoo}]

    assert raises(InvalidReactionError, function, args)
    assert 'reaction 3' not in register_reaction_mechanism.mechanism_namespace


def test_register_existing_reaction():
    function = register_reaction_mechanism
    args = ['reaction 2', {}]

    assert raises(ExistingReactionError, function, args)


def test_not_modified_by_decorator():
    def myfunction(*args):
        return 42

    decorated = register_reaction_mechanism('reaction 4', {})(myfunction)
    assert myfunction is decorated
    assert myfunction() == decorated()
