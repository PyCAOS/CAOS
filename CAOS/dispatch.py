"""Handles registration and dispatch of reactions and molecule types.

Provides two decorators that are aliases for classes:

    decorator alias -> ClassName
    =================================================
    register_reaction_mechanism -> ReactionDispatcher
    register_molecule_type -> MoleculeTypeDispatcher

This allows for the reaction system to dynamically determine which type
of reaction and molecules should be used.

This all happens dynamically, at runtime.
"""

from __future__ import print_function, division, unicode_literals

import six

from .exceptions.dispatch_errors import ExistingReactionError, \
    InvalidReactionError
from .exceptions.reaction_errors import FailedReactionError
from .logging import logger


class ReactionDispatcher(object):
    """Class that dispatches on reaction types.

    Attributes
    ==========
    mechanism_namespace: dict
        Dictionary of the registered mechanisms.  Class-level attribute.
    """

    mechanism_namespace = {}

    REACTION_ATTEMPT_MESSAGE = ("Trying to react reactants {}"
                                " in conditions {} as a {} type reaction.")
    REACTION_FAILURE_MESSAGE = ("Couldn't react reactants {}"
                                " in conditions {}.")
    REGISTERED_MECHANISM_MESSAGE = "Added mechanism {} with requirements {}."
    REQUIREMENT_NOT_MET_MESSAGE = ("Requirement {} for mechanism {} not met"
                                   " by reactants {} in conditions {}")
    REQUIREMENT_PASSED_MESSAGE = "Passed requirement {} for mechanism {}"
    ADDED_POSSIBLE_MECHANISM = "Added potential mechanism {}"

    _function = None
    _namespace = None
    _requirements = None
    _name = ""

    @property
    def name(self):
        """The name of the mechanism."""

        return self._name

    @name.setter
    def name(self, mechanism_name):
        """Set the name of the mechanism and add to namespace.

        The name must not exist in the namespace.
        """

        if mechanism_name in ReactionDispatcher.mechanism_namespace:
            message = "A mechanism named {} already exists.".format(
                mechanism_name
            )
            logger.error(message)
            raise ExistingReactionError(message)
        self._name = mechanism_name

        ReactionDispatcher.mechanism_namespace[self._name] = {}

    @property
    def namespace(self):
        """Shortcut to this mechanism's part of the namespace."""

        if self._namespace is None:
            self._namespace = ReactionDispatcher.mechanism_namespace[self.name]
        return self._namespace

    @property
    def function(self):
        """The function to be called when using this reaction."""

        if self._function is None:
            self._function = self.namespace['function']
        return self._function

    @function.setter
    def function(self, func):
        """Set the function to be called when using this reaction."""

        self.namespace['function'] = func

    @property
    def requirements(self):
        """The requirements of this reaction mechanism."""

        if self._requirements is None:
            self._requirements = self.namespace['requirements']
        return self._requirements

    @requirements.setter
    def requirements(self, req):
        """Set the requirements of this function.

        Notes
        =====
        All of the individual requirements must be callable.
        """

        for req_name, req_function in six.iteritems(req):
            if not six.callable(req_function):
                del ReactionDispatcher.mechanism_namespace[self.name]

                message = "Requirement {} is not a function.".format(req_name)
                logger.error(message)
                raise InvalidReactionError(message)
        self.namespace['requirements'] = req

    def __init__(self, mechanism_name, requirements):
        """Register a new reaction mechanism.

        Parameters
        ==========
        mechanism_name: string
            The name that the mechanism should be registered as
        requirements: dict
            Dictionary of requirements that provided reactants and
            conditions must meet for this reaction to be considered.
        """

        self.name = mechanism_name
        self.requirements = requirements
        logger.log(
            ReactionDispatcher.REGISTERED_MECHANISM_MESSAGE.format(
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

        This really only exists for testing purposes.
        """

        cls.mechanism_namespace = {}

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

        for mech_name, mech_info in six.iteritems(cls.mechanism_namespace):
            mechanism = mech_info['function']
            requirements = mech_info['requirements']

            for req_name, req_function in six.iteritems(requirements):
                if not req_function(reactants, conditions):
                    logger.log(cls.REQUIREMENT_NOT_MET_MESSAGE.format(
                        req_name, mech_name, reactants, conditions
                    ))
                    break
                else:
                    logger.log(cls.REQUIREMENT_PASSED_MESSAGE.format(
                        req_name, mech_name
                    ))
            else:
                logger.log(cls.ADDED_POSSIBLE_MECHANISM.format(mech_name))
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
                cls.REACTION_ATTEMPT_MESSAGE.format(
                    reactants, conditions, potential_reaction
                )
            )
            if product is not None:
                return product

        message = cls.REACTION_FAILURE_MESSAGE.format(reactants, conditions)
        logger.log(message)
        raise FailedReactionError(message)

    @classmethod
    def is_registered(cls, reaction):
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
            for name, info in six.iteritems(cls.mechanism_namespace):
                if reaction is info['function']:
                    return True
            else:
                return False
        else:
            return reaction in cls.mechanism_namespace


# Provide friendlier way to call things
react = ReactionDispatcher._react
register_reaction_mechanism = ReactionDispatcher
_clear = ReactionDispatcher._ReactionDispatcher__clear
reaction_is_registered = ReactionDispatcher.is_registered
