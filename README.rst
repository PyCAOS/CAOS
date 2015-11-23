CAOS - Computer Assisted Organic Synthesis (in Python!)
=======================================================

|Build status| |Coverage Status| |Documentation Status|

CAOS is a useful tool for many organic chemists, but is often a hard one
to use in practice. This library will seek to provide an easy method of
predicting reactions.

Documentation
~~~~~~~~~~~~~

Is available at `readthedocs.org <http://caos.readthedocs.org/en/latest/>`__.

Examples
~~~~~~~~

Are not available at this time - much of it hasn't been implemented to
the point where an example would be helpful.

Currently the registration of reaction mechanisms has been implemented,
as well as performing reactions. No work on loading molecules,
representing those molecules, or analyzing them has been completed.

Todos:
~~~~~~

-  [X] Add CI
-  [X] Add reaction registration and dispatch
-  [ ] Add loading molecules
-  [ ] Add molecule inspection
-  [ ] Add common requirements functions
-  [ ] ???

CAOS is still in early stages of development. Information will be added
as it becomes available.

Motivation
----------

This is a project for my Fall 2015 DSLs class. It is loosely based off
of a `previous project <https://github.com/Dannnno/Chemistry>`__ however
with the intent of being more modular, extensible, and language-like.
While I can't say much about how it should look, I can say that I'd like
to eventually provide this sort of interface to users.

.. code:: python

    import my_reaction_mechanisms
    from CAOS import react, load_molecule_from_file

    reactant1 = load_molecule_from_file("filename.cml")
    reactant2 = load_molecule_from_file("filename.smiles", type="SMILES")
    products = react([reactant1, reactant2], conditions={})

    products.show()

I'd also like to allow users to register new reaction mechanisms in order to
meet their own needs

.. code:: python

    @register_reaction_mechanism(name, requirements)
    def diels_alder_reaction(reactants, conditions):
        ...

As these details become more firmly defined, this file will become more
useful.

Licensing
~~~~~~~~~

CAOS is licensed using the `MIT License <https://opensource.org/licenses/MIT>`_.

.. include:: ../LICENSE

.. |Build status| image:: https://travis-ci.org/PyCAOS/CAOS.svg?branch=master
   :target: https://travis-ci.org/PyCAOS/CAOS
.. |Coverage Status| image:: https://coveralls.io/repos/PyCAOS/CAOS/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/PyCAOS/CAOS?branch=master
.. |Documentation Status| image:: https://readthedocs.org/projects/caos/badge/?version=latest
   :target: http://caos.readthedocs.org/en/latest/?badge=latest
