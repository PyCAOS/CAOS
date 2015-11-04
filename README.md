# CAOS - Computer Assisted Organic Synthesis (in Python!)

[![Build status](https://travis-ci.org/PyCAOS/CAOS.svg)](https://travis-ci.org/PyCAOS/CAOS)
[![Coverage Status](https://coveralls.io/repos/PyCAOS/CAOS/badge.svg?branch=master&service=github)](https://coveralls.io/github/PyCAOS/CAOS?branch=master)

CAOS is a useful tool for many organic chemists, but is often a hard
one to use in practice.  This library will seek to provide an easy 
method of predicting reactions.

### Documentation
Coming soon!

### Examples
Coming soon!

CAOS is still in early stages of development.  Information will be added
as it becomes available.

## Motivation

This is a project for my Fall 2015 DSLs class.  It is loosely based off of
a [previous project](https://github.com/Dannnno/Chemistry) however with the
intent of being more modular, extensible, and language-like.  While I can't
say much about how it should look, I can say that I'd like to eventually
provide this sort of interface to users.

```python
import my_reaction_mechanisms
from CAOS import react, load_molecule_from_file

reactant1 = load_molecule_from_file("filename.cml")
reactant2 = load_molecule_from_file("filename.smiles", type="SMILES")
products = react([reactant1, reactant2], conditions={})

products.show()
```

I'd also like to allow users to register new reaction mechanisms and
new moleuclar data structures in order to meet their own needs

```python
@register_reaction_mechanism(name, requirements, molecule_type)
def diels_alder_reaction(products, conditions=None):
    ...
    
@register_molecule_type()
class DielsAlderStructure(object):

  @classmethod
  def from_default(cls, molecule):
      ...
```

As these details become more firmly defined, this file will
become more useful.
