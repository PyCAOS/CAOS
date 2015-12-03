CAOS - Computer Assisted Organic Synthesis (in Python!)
=======================================================

|Build Status| |Coverage Status| |Documentation Status| |Codacy Status|

Traditional Computer Assisted Organic Synthesis is a useful tool for many
organic chemists, but can often be more difficult to use in practice. The
CAOS library seeks to provide an easy way of predicting organic chemsitry
reactions.

Documentation
~~~~~~~~~~~~~

Is available at `readthedocs.org <http://caos.readthedocs.org/en/latest/>`__.

Examples
~~~~~~~~

Simple reactions can be performed like so:

.. code:: python

    from CAOS.dispatch import react
    from CAOS.structures.molecule import Molecule

    acid = Molecule(
        {'a1': 'H', 'a2': 'H', 'a3': 'H', 'a4': 'O'},
        {'b1': {'nodes': ('a1', 'a4'), 'order': 1},
         'b2': {'nodes': ('a2', 'a4'), 'order': 1},
         'b3': {'nodes': ('a3', 'a4'), 'order': 1}
        },
        id='Hydronium'
    )

    base = Molecule(
        {'a1': 'H', 'a2': 'O'},
        {'b1': {'nodes': ('a1', 'a2'), 'order': 1}},
        id='Hydroxide'
    )

    conditions = {
        'pkas': {'Hydronium': -1.74, 'Hydroxide': 15.7},
        'pka_points': {'Hydronium': 'a1', 'Hydroxide': 'a2'}
    }

    products = react([acid, base], conditions)

In this case, based on the information in the molecules and the conditions,
the system will predict an acid base reaction that results in the creation of
two water molecules and no salt.

Additionally, user-defined reaction mechanisms can be added to the system.

.. code:: python

    # aqueous_mechanism.py
    from CAOS.dispatch import register_reaction_mechanism

    def aqueous(reactants, conditions):
        return conditions.get('aqeuous', False)

    @register_reaction_mechanism([aqueous])
    def some_mechanism(reactants, conditions):
        # do something
        return products

    # reaction.py
    import aqueous_mechanism
    from CAOS.dispatch import react
    from CAOS.structures.molecule import Molecule

    m1 = Molecule(...)
    m2 = Molecule(...)
    conditions = {'aqueous': True}

    products = react([m1, m2], conditions)

Here the system would use the aqueous mechanism that you have defined,
because the conditions match the aqueous requirement the mechanism was
decorated with.

The system is under active development, and the goal is to eventually
take as much of the work out of the hands of the user.


Todos:
~~~~~~

-  [X] Add CI
-  [X] Add reaction registration and dispatch
-  [ ] Add loading molecules
-  [X] Add molecule inspection
-  [ ] Add common requirements functions
-  [ ] ???

CAOS is still in early stages of development. Information will be added
as it becomes available.

Motivation
----------

This is a project for my Fall 2015 DSLs class. It is loosely based off
of a `previous project <https://github.com/Dannnno/Chemistry>`__ however
with the intent of being more modular, extensible, and language-like.

Licensing
~~~~~~~~~

CAOS is licensed using the `MIT License <https://opensource.org/licenses/MIT>`_.

.. include:: ../LICENSE

.. |Build Status| image:: https://travis-ci.org/PyCAOS/CAOS.svg?branch=master
   :target: https://travis-ci.org/PyCAOS/CAOS
.. |Coverage Status| image:: https://codecov.io/github/PyCAOS/CAOS/coverage.svg?branch=master
    :target: https://codecov.io/github/PyCAOS/CAOS?branch=master
.. |Documentation Status| image:: https://readthedocs.org/projects/caos/badge/?version=latest
   :target: http://caos.readthedocs.org/en/latest/?badge=latest
.. |Codacy Status| image:: https://api.codacy.com/project/badge/grade/8ed5a7c79ff14231a23747d0171b7120
    :target: https://www.codacy.com/app/dannnno16/CAOS
