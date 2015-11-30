"""Classes and functions associated with default molecule objects."""

from __future__ import print_function, division, unicode_literals, \
    absolute_import
from future.builtins import *  # noqa
from future.builtins.disabled import *  # noqa
import six

import json

import networkx as nx
from networkx.algorithms.isomorphism import is_isomorphic

from .. import logger


class Molecule(nx.Graph):
    """Representation of a molecule as a graph."""

    _ATOM_EXISTS = "ATOM {0} exists in the molecule as ID {1}"
    _BOND_EXISTS = "BOND {0} exists in the molecule as ID {1}"

    @classmethod
    def from_default(cls, other):
        """Build a molecule from the default molecule.

        Parameters
        ----------
        other : Molecule
            The default molecule that this should be built from.

        Returns
        -------
        other : Molecule
            The input molecule because this is already a default
            molecule.
        """

        return other

    def to_default(self):
        """Build a default molecule from this instance.

        Returns
        -------
        default : Molecule
            A default molecule that is roughly equivalent to this one.
        """

        return self

    def __init__(self, atoms, bonds, **kwargs):
        """Initialize a molecule.

        Parameters
        ==========
        atoms : dict
            Mapping from id within the molecule to an atom
        bonds : dict
            Mapping from id within the molecule to a bond

        Examples
        ========
        >>> atoms = {
        ...     'a1': 'H',
        ...     'a2': 'H',
        ...     'a3': 'O'
        ... }
        >>> bonds = {
        ...      'b1': {
        ...          'nodes': ('a1', 'a3'),
        ...          'order': 1
        ...       }, 'b2': {
        ...          'nodes': ('a2', 'a3'),
        ...          'order': 1
        ...       }
        ... }
        >>> molecule = Molecule(atoms, bonds)
        """

        super(Molecule, self).__init__()
        self.atoms = atoms
        self.bonds = bonds

        for name, value in six.iteritems(kwargs):
            if not hasattr(self, name):
                setattr(self, name, value)
            else:
                raise ValueError("Keyword argument {0} masks existing name.")

    _atoms = None

    @property
    def atoms(self):
        """The atoms in the molecule.

        Returns
        -------
        dict
            Dictionary of atoms.  The mapping is from string IDs to
            atomic identifiers.

        Raises
        ------
        KeyError
            If there is an attempt to add an atom with an existing key,
            instead of replacing that atom it raises an error.
        """

        if self._atoms is None:
            self._atoms = {}
        return self._atoms

    @atoms.setter
    def atoms(self, atom_dict):
        """Set the atoms in the molecule."""

        for id_, symbol in six.iteritems(atom_dict):
            self._add_node(id_, symbol)

    def _add_node(self, id_, atomic_symbol):
        """Add a node (atom) to the molecule.

        Parameters
        ----------
        id_ : str
            Id of this atom.
        atomic_symbol : str
            Symbol associated with this atom (i.e. 'H' for Hydrogen).

        Raises
        ------
        KeyError
            You can't add a node if there is already an atom with that
            id in the molecule.
        """

        if id_ in self.atoms:
            message = Molecule._ATOM_EXISTS.format(atomic_symbol, id_)
            logger.log(message)
            raise KeyError(message)
        else:
            self.add_node(id_, {'symbol': atomic_symbol})
            self.atoms[id_] = atomic_symbol

    _bonds = None

    @property
    def bonds(self):
        """The bonds within the molecule.

        Returns
        -------
        dict
            Dictionary of the bonds.  Mapping is from a string id to a
            dictionary of key-value pairs, including the nodes, the
            order, and any other pertient information.

        Raises
        ------
        KeyError
            If a bond with a given id already exists an error will be
            thrown.
        """

        if self._bonds is None:
            self._bonds = {}
        return self._bonds

    @bonds.setter
    def bonds(self, bond_dict):
        """Set the bonds in the molecule."""

        for id_, bond in six.iteritems(bond_dict):
            self._add_edge(id_, bond)

    def _add_edge(self, id_, bond):
        """Add an edge (bond) to the molecule.

        Parameters
        ----------
        id_ : str
            The id for the bond
        bond : dict
            Important values associated with the bond.

        Raises
        ------
        KeyError
            If a bond with an existing id is added, instead of replacing
            the existing one, an error is thrown.
        """

        bond['id'] = id_
        if id_ in self.bonds:
            message = Molecule._BOND_EXISTS.format(bond, id_)
            logger.log(message)
            raise KeyError(message)
        else:
            first, second = bond['nodes']
            self.add_edge(
                first, second,
                dict((key, value)
                     for (key, value) in six.iteritems(bond)
                     if key != 'nodes')
            )
            self.bonds[id_] = bond

    @property
    def _next_free_atom_id(self):
        return self._next_id('a')

    @property
    def _next_free_bond_id(self):
        return self._next_id('b')

    def _next_id(self, letter):
        invalid_nums = set()
        if letter == 'a':
            for atom_id in self.atoms:
                invalid_nums.add(int(atom_id[1:]))
        elif letter == 'b':
            for bond_id in self.bonds:
                invalid_nums.add(int(bond_id[1:]))
        else:
            raise ValueError(
                "What kind of id do you want? "
                "Must be an atom ('a') or a bond ('b')."
            )

        for i in range(len(invalid_nums) + 1):
            if i not in invalid_nums:
                return "{0}{1}".format(letter, i)

    def _node_matcher(self, first, second):
        """Check if two nodes are isomorphically equivalent.

        Parameters
        ----------
        first, second : dict
            Dictionaries of the contents of two nodes.

        Returns
        -------
        bool
            Whether or not two nodes are isographically equivalent, in
            this case meaning that they have the same atomic symbol.
        """

        return first['symbol'] == second['symbol']

    def __eq__(self, other):
        return is_isomorphic(self, other, node_match=self._node_matcher)

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return '\n'.join(
            [
                json.dumps(self.atoms),
                json.dumps(self.bonds)
            ]
        )
