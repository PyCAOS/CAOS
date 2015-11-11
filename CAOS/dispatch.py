"""Handles registration and dispatch of reactions and molecule types.

Provides two decorators that are used to register reactions and
molecules, `register_reaction_mechanism` and `register_molecule_type`.
This allows the reaction system to determine which type of reaction and
what representation of molecules should be used, all occuring
dynamically, at runtime.

Attributes
----------
react: function
    Function that attempts to react molecules under given conditions
register_reaction_mechanism: function
    Registers a reaction mechanism with the dispatch system.
reaction_is_registered: function
    Checks whether or not a reaction has been registered.
register_molecule_type: function
    Registers a molecule type (i.e. a class) with the dispatch system.
"""

from __future__ import print_function, division, unicode_literals

import six

from .exceptions.dispatch_errors import ExistingReactionError, \
    InvalidReactionError, InvalidMoleculeStructureError, \
    ExistingMoleculeTypeError
from .exceptions.reaction_errors import FailedReactionError
from .chem_logging import logger


class ReactionDispatcher(object):
    """Class that dispatches on reaction types."""

    _REACTION_ATTEMPT_MESSAGE = ("Trying to react reactants {}"
                                 " in conditions {} as a {} type reaction.")
    _REACTION_FAILURE_MESSAGE = ("Couldn't react reactants {}"
                                 " in conditions {}.")
    _REGISTERED_MECHANISM_MESSAGE = "Added mechanism {} with requirements {}."
    _REQUIREMENT_NOT_MET_MESSAGE = ("Requirement {} for mechanism {} not met"
                                    " by reactants {} in conditions {}")
    _REQUIREMENT_PASSED_MESSAGE = "Passed requirement {} for mechanism {}"
    _ADDED_POSSIBLE_MECHANISM = "Added potential mechanism {}"
    _UNKNOWN_STRUCTURE_MESSAGE = ("Unkown molecular structure {} required for "
                                  "mechanism {}")
    _EXISTING_MOLECULE_TYPE_ERROR = "Molecule type {} already registered."

    _mechanism_namespace = {}
    _structure_namespace = {}
    _namespace = None
    _name = ""

    @property
    def name(self):
        """The name assigned to the mechanism.

        Returns
        -------
        string
            The name the mechanism has been registered as.

        Raises
        ------
        ExistingReactionError
            The name must be unique - if an existing mechanism shares
            this name it will cause an error.
        """

        return self._name

    @name.setter
    def name(self, mechanism_name):
        """Set the name of the mechanism and add to namespace.

        The name must not exist in the namespace.
        """

        if mechanism_name in ReactionDispatcher._mechanism_namespace:
            message = "A mechanism named {} already exists.".format(
                mechanism_name
            )
            logger.error(message)
            raise ExistingReactionError(message)
        self._name = mechanism_name

        ReactionDispatcher._mechanism_namespace[self._name] = {}

    @property
    def namespace(self):
        """Shortcut to this mechanism's part of the namespace.

        Returns
        -------
        dict
            Contains the requirements that must be met to dispatch this
            function, the data structure needed, as well as the function
            itself.

        Notes
        -----
        Assumes that the name of this mechanism is already known.  If
        you unset the name, this will behave strangely or error.
        """

        if self._namespace is None:
            self._namespace = ReactionDispatcher._mechanism_namespace[self.name]
        return self._namespace

    @property
    def function(self):
        """The function to be called when using this reaction.

        Returns
        -------
        callable
            The function that has been registered for this reaction.

        Notes
        -----
        Should not be called directly - let the `react` function handle
        that.
        """

        return self.namespace['function']

    @function.setter
    def function(self, func):
        """Set the function to be called when using this reaction."""

        self.namespace['function'] = func

    @property
    def requirements(self):
        """The requirements of this reaction mechanism.

        Returns
        -------
        dict
            Mapping from requirement name to some callable that can be
            used to determine if the parameters meet the requirement.

        Raises
        ------
        InvalidReactionError
            If any of the requirements aren't callable then an error is
            raised.
        """

        return self.namespace['requirements']

    @requirements.setter
    def requirements(self, req):
        """Set the requirements of this function."""

        for req_name, req_function in six.iteritems(req):
            if not six.callable(req_function):
                del ReactionDispatcher._mechanism_namespace[self.name]

                message = "Requirement {} is not a function.".format(req_name)
                logger.error(message)
                raise InvalidReactionError(message)
        self.namespace['requirements'] = req

    @property
    def molecule_type(self):
        """The representation of molecules this reaction requires.

        Returns
        -------
        type
            The class of the data structure that should be used.

        Raises
        ------
        InvalidMoleculeStructureError
            If the molecule doesn't meet the interface required for
            dispatch then an error is raised.
        """

        return self.namespace['molecule_type']

    @molecule_type.setter
    def molecule_type(self, type_):
        """Set the molecule type."""

        if ReactionDispatcher._is_registered_molecule_type(type_):
            if isinstance(type_, str):
                self.namespace['molecule_type'] = \
                    ReactionDispatcher._structure_namespace[type_]
            else:
                self.namespace['molecule_type'] = type_
        else:
            message = ReactionDispatcher._UNKNOWN_STRUCTURE_MESSAGE.format(
                type_, self.name
            )
            logger.error(message)
            raise InvalidMoleculeStructureError(message)

    def __init__(self, mechanism_name, requirements, molecule_type='default'):
        """Register a new reaction mechanism.

        Parameters
        ==========
        mechanism_name: string
            The name that the mechanism should be registered as
        requirements: dict
            Dictionary of requirements that provided reactants and
            conditions must meet for this reaction to be considered.
        molecule_type: Optional[string], Optional[type]
            The name or type of data structure that should be used for
            this type of reaction.
        """

        self.name = mechanism_name
        self.requirements = requirements
        self.molecule_type = molecule_type
        logger.log(
            ReactionDispatcher._REGISTERED_MECHANISM_MESSAGE.format(
                mechanism_name, list(six.iterkeys(requirements))
            )
        )

    def __call__(self, mechanism_function):
        """Register the function.

        Parameters
        ==========
        mechanism_function: callable
            The function that should be called when the reaction is
            attempted.

        Returns
        =======
        mechanism_function: callable
            The function that was decorated, unaltered.

        Notes
        =====
        Callables that are decorated with this will not have any
        difference in behavior than if they were not decorated.  In
        order to get dispatching behavior, the `react` function must
        be used instead.
        """

        self.function = mechanism_function

        return mechanism_function

    @classmethod
    def __clear(cls):
        """Clear out the namespace.

        Notes
        -----
        This really only exists for testing purposes.
        """

        cls._mechanism_namespace = {}

    @classmethod
    def _generate_likely_reactions(cls, reactants, conditions):
        """Generate a list of potential reactions.

        Parameters
        ==========
        reactants: collection[Molecule]
            A list of molecules to be reacted
        conditions: mapping[String -> Object]
            Dictionary of the conditions in this molecule.

        Returns
        =======
        mechanisms: list[function]
            A list of mechanisms to try.

        Notes
        =====
        Currently this list is in no particular order - this will change
        and should not be relied on.
        """

        mechanisms = []

        for mech_name, mech_info in six.iteritems(cls._mechanism_namespace):
            mechanism = mech_info['function']
            requirements = mech_info['requirements']

            for req_name, req_function in six.iteritems(requirements):
                if not req_function(reactants, conditions):
                    logger.log(cls._REQUIREMENT_NOT_MET_MESSAGE.format(
                        req_name, mech_name, reactants, conditions
                    ))
                    break
                else:
                    logger.log(cls._REQUIREMENT_PASSED_MESSAGE.format(
                        req_name, mech_name
                    ))
            else:
                logger.log(cls._ADDED_POSSIBLE_MECHANISM.format(mech_name))
                mechanisms.append(mechanism)

        return mechanisms

    @classmethod
    def _react(cls, reactants, conditions):
        """The method that actually performs a reaction.

        Parameters
        ==========
        reactants: collection[Molecule]
            A list of molecules to be reacted
        conditions: mapping[String -> Object]
            Dictionary of the conditions in this molecule.

        Returns
        =======
        products: list[Molecule]
            Returns a list of the products.
        """

        potential_reactions = cls._generate_likely_reactions(
            reactants, conditions
        )

        for potential_reaction in potential_reactions:
            product = potential_reaction(reactants, conditions)
            logger.log(
                cls._REACTION_ATTEMPT_MESSAGE.format(
                    reactants, conditions, potential_reaction
                )
            )
            if product is not None:
                return product

        message = cls._REACTION_FAILURE_MESSAGE.format(reactants, conditions)
        logger.log(message)
        raise FailedReactionError(message)

    @classmethod
    def _is_registered_reaction(cls, reaction):
        """Check if a reaction has been registered.

        Parameters
        ==========
        reaction: string, callable
            The reaction to be checked.

        Returns
        =======
        bool
            Whether or not the reaction has been registered.
        """

        if callable(reaction):
            for name, info in six.iteritems(cls._mechanism_namespace):
                if reaction is info['function']:
                    return True
            else:
                return False
        else:
            return reaction in cls._mechanism_namespace

    @classmethod
    def _is_registered_molecule_type(cls, molecule_type):
        """Check if a molecule type has been registered.

        Parameters
        ==========
        molecule_type: string, type
            The molecule type to be checked.

        Returns
        =======
        bool
            Whether or not the molecule type has been registered.
        """

        for name, type_ in six.iteritems(cls._structure_namespace):
            if name == molecule_type or type_ is molecule_type:
                return True
        return False

    @classmethod
    def _register_molecule_type(cls, name, method_name='from_default'):
        """Register a molecule.

        Parameters
        ==========
        name : string
            The name of the molecule type.
        method_name : Optional[string]
            The name of the `classmethod` that can be used to construct
            an instance of the registered object from a default Molecule
            object. If not provided it is assumed to be 'from_default'.

        Returns
        =======
        register : function
            The actual decorator that can be used to decorate the class.
        """

        def register(class_):
            """Register a class representing a molecule.

            Registers the class with the dispatch system.

            Parameters
            ==========
            class_ : type
                Class object for the representation.

            Raises
            ======
            ExistingMoleculeTypeError
                The molecule type should not have been previously
                registered with the dispatch system.

            Returns
            =======
            class_ : type
                The same class object that was passed in, unaltered.
            """

            if name in cls._structure_namespace:
                message = cls._EXISTING_MOLECULE_TYPE_ERROR.format(name)
                logger.error(message)
                raise ExistingMoleculeTypeError(message)

            cls._structure_namespace[name] = {
                'type': class_, 'method_name': method_name
            }

            return class_

        return register


# Provide friendlier way to call things
react = ReactionDispatcher._react
register_reaction_mechanism = ReactionDispatcher
_clear = ReactionDispatcher._ReactionDispatcher__clear
reaction_is_registered = ReactionDispatcher._is_registered_reaction
register_molecule_type = ReactionDispatcher._register_molecule_type
molecule_type_is_registered = ReactionDispatcher._is_registered_molecule_type
