"""Calculate the pka of a molecule."""

from __future__ import print_function, division, unicode_literals, \
    absolute_import
from future.builtins import *  # noqa
from future.builtins.disabled import *  # noqa


def pka(reactants, conditions):
    """Compute the pka of every molecule in the reactants.

    The pka, as well as the id of the "pka_point" is stored in the
    molecule.  The "pka_point" is the id of the Hydrogen most likely to
    be donated, or the id of the atom most likely to accept a Hydrogen.
    The pka is based off of the pka_point of the atom.

    Parameters
    ----------
    reactants: list[Molecule]
        A list of reactant molecules.
    conditions: dict
        Dictionary of conditions.

    Notes
    -----
    Eventually this will be computed, however right now it just pulls
    specified information from the conditions dict.
    """

    if 'pkas' in conditions and 'pka_points' in conditions:
        for reactant in reactants:
            id_ = reactant.id
            reactant.pka = conditions['pkas'][id_]
            reactant.pka_point = conditions['pka_points'][id_]
        return True
    return False
