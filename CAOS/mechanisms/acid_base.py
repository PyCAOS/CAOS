"""The acid base mechanism implementation."""

from copy import deepcopy


__requirements__ = ('pka',)


def _get_ideal_hydrogen(acid):
    pass


def _get_hydrogen_acceptor(base):
    pass


def _move_hydrogen(base):
    pass


def acid_base_reaction(reactants, conditions):
    """Perform an acid base reaction on the reactants.

    Parameters
    ----------
    reactants: list[Molecule]
        The reactants in the reaction.
    conditions: dict
        The conditions under which the reaction should occur.

    Returns
    -------
    products: list[Molecule]
        The products of the reaction.
    """

    # Figure out the acid and the base
    acid = reactants[0]
    base = reactants[1]

    for reactant in reactants:
        if reactant.pka < acid.pka:
            acid = reactant
        elif reactant.pka > base.pka:
            base = reactant

    # Figure out what is going to move and where
    donating_hydrogen_id = _get_ideal_hydrogen(acid)
    hydrogen_acceptor_id = _get_hydrogen_acceptor(base)

    # Make the conjugate acids, bases, and salt
    conjugate_acid = deepcopy(base)
    conjugate_base = deepcopy(acid)
    salt = None

    _move_hydrogen(
        conjugate_base, donating_hydrogen_id,
        conjugate_acid, hydrogen_acceptor_id
    )

    return [conjugate_acid, conjugate_base, salt]
