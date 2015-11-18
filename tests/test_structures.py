from CAOS.structures.molecule import Molecule
from CAOS.util import raises


def test_from_default():
    a = Molecule(
        {'a1': 'H', 'a2': 'O'},
        {'b1': {'nodes': ('a1', 'a2')}}
    )
    b = Molecule.from_default(a)
    assert a == b
    assert a is b


def test_to_default():
    a = Molecule(
        {'a1': 'H', 'a2': 'O'},
        {'b1': {'nodes': ('a1', 'a2')}}
    )
    b = a.to_default()
    assert a == b
    assert a is b


def test_add_node():
    a = Molecule(
        {'a1': 'H', 'a2': 'O'},
        {'b1': {'nodes': ('a1', 'a2')}}
    )
    a._add_node('a3', 'H')
    assert 'a3' in a.atoms
    assert a.atoms['a3'] == 'H'


def test_add_existing_node():
    a = Molecule(
        {'a1': 'H', 'a2': 'O'},
        {'b1': {'nodes': ('a1', 'a2')}}
    )

    args = ['a2', 'H']
    function = a._add_node
    exception_type = KeyError
    assert raises(exception_type, function, args)


def test_add_edge():
    a = Molecule(
        {'a1': 'H', 'a2': 'O'},
        {'b1': {'nodes': ('a1', 'a2')}}
    )
    a._add_edge('b2', {'nodes': ('a1', 'a2')})
    assert 'b2' in a.bonds
    assert a.bonds['b2'] == {'nodes': ('a1', 'a2'), 'id': 'b2'}


def test_add_existing_edge():
    a = Molecule(
        {'a1': 'H', 'a2': 'O'},
        {'b1': {'nodes': ('a1', 'a2')}}
    )

    args = ['b1', {'nodes': ('a1', 'a2')}]
    function = a._add_edge
    exception_type = KeyError
    assert raises(exception_type, function, args)


def test_simple_equality():
    a = Molecule(
        {'a1': 'H', 'a2': 'O'},
        {'b1': {'nodes': ('a1', 'a2')}}
    )
    b = Molecule(
        {'a1': 'H', 'a2': 'O'},
        {'b1': {'nodes': ('a1', 'a2')}}
    )

    assert a == b


def test_isomorphic_equality():
    a = Molecule(
        {'a1': 'H', 'a2': 'O'},
        {'b1': {'nodes': ('a1', 'a2')}}
    )
    b = Molecule(
        {'a2': 'H', 'a1': 'O'},
        {'b2': {'nodes': ('a1', 'a2')}}
    )

    assert a == b


def test_inequality():
    a = Molecule(
        {'a1': 'H', 'a2': 'O'},
        {'b1': {'nodes': ('a1', 'a2')}}
    )
    b = Molecule(
        {'a1': 'N', 'a2': 'O'},
        {'b1': {'nodes': ('a1', 'a2')}}
    )

    assert a != b


def test_stupid_repr_test():
    a = Molecule(
        {'a1': 'H', 'a2': 'O'},
        {'b1': {'nodes': ('a1', 'a2')}}
    )

    assert repr(a)
