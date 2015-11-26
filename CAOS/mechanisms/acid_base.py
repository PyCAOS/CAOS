"""The acid base mechanism implementation."""

from __future__ import print_function, division, unicode_literals, \
    absolute_import

from copy import deepcopy


__requirements__ = ('pka',)


def _get_ideal_hydrogen(acid):
    # Todo: Actually compute this here instead of relying on an instance
    # variable
    return acid.pka_point


def _get_hydrogen_acceptor(base):
    # Todo: Actually compute this here instead of relying on an instance
    # variable
    return base.pka_point


def _move_hydrogen(conj_base, donate_id, conj_acid, accept_id):
    conj_base.remove_node(donate_id)
    id_ = conj_acid._next_free_atom_id
    conj_acid._add_node(id_, 'H')
    conj_acid._add_edge(
        conj_acid._next_free_bond_id,
        {'nodes': (id_, accept_id), 'order': 1}
    )


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
