from CAOS.structures.molecule import Molecule
from CAOS.dispatch import react


def test_simple_acid_base_reaction():
    acid = Molecule(
        {'a1': 'H', 'a2': 'H', 'a3': 'H', 'a4': 'O'},
        {'b1': {'nodes': ('a1', 'a4'), 'order': 1},
         'b2': {'nodes': ('a2', 'a4'), 'order': 1},
         'b3': {'nodes': ('a3', 'a4'), 'order': 1}
        },
        **{'id': 'Hydronium'}
    )

    base = Molecule(
        {'a1': 'H', 'a2': 'O'},
        {'b1': {'nodes': ('a1', 'a2'), 'order': 1}},
        **{'id': 'Hydroxide'}
    )

    conditions = {
        'pkas': {'Hydronium': -1.74, 'Hydroxide': 16},
        'pka_points': {'Hydronium': 'a1', 'Hydroxide': 'a2'}
    }

    products = react([acid, base], conditions)

    conjugate_acid = Molecule(
        {'a1': 'H', 'a2': 'H', 'a3': 'O'},
        {'b1': {'nodes': ('a1', 'a3'), 'order': 1},
         'b2': {'nodes': ('a2', 'a3'), 'order': 1}
        }
    )

    conjugate_base = Molecule(
        {'a1': 'H', 'a2': 'H', 'a3': 'O'},
        {'b1': {'nodes': ('a1', 'a3'), 'order': 1},
         'b2': {'nodes': ('a2', 'a3'), 'order': 1}
        }
    )

    assert products[0] == conjugate_acid
    assert products[1] == conjugate_base

    # Determining the salt isn't implemented
    assert products[2] is None
