"""Classes and functions associated with default molecule objects."""

from __future__ import print_function, division, unicode_literals

import networkx as nx

from ..dispatch import register_molecule_type


@register_molecule_type('default')
class Molecule(nx.Graph):
	"""Representation of a molecule as a graph."""

	@classmethod
	def from_default(cls, other):
		"""

		"""

		return other
