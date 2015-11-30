"""Handles registration and dispatch of reactions and molecule types.

Provides a decorator that is used to register reaction mechanisms,
`register_reaction_mechanism`. This allows the reaction system to
determine which type of reaction should be attempted, dynamically at
runtime.

Attributes
----------
react: function
    Function that attempts to react molecules under given conditions
register_reaction_mechanism: function
    Registers a reaction mechanism with the dispatch system.
reaction_is_registered: function
    Checks whether or not a reaction has been registered.
"""

from __future__ import print_function, division, unicode_literals, \
    absolute_import

import six

from .exceptions.dispatch_errors import ExistingReactionError, \
    InvalidReactionError
from .exceptions.reaction_errors import FailedReactionError
from . import logger


class ReactionDispatcher(object):
    """Class that dispatches on reaction types."""

    _REACTION_ATTEMPT_MESSAGE = ("Trying to react reactants {0}"
                                 " in conditions {1} as a {2} type reaction.")
    _REACTION_FAILURE_MESSAGE = ("Couldn't react reactants {0}"
                                 " in conditions {1}.")
    _REGISTERED_MECHANISM_MESSAGE = "Added mechanism {0} with requirements {1}."
    _REQUIREMENT_NOT_MET_MESSAGE = ("Requirement {0} for mechanism {1} not met"
                                    " by reactants {2} in conditions {3}")
    _REQUIREMENT_PASSED_MESSAGE = "Passed requirement {0} for mechanism {1}"
    _ADDED_POSSIBLE_MECHANISM = "Added potential mechanism {0}"
    _EXISTING_MECHANISM_ERROR = "A mechanism named {0} already exists."

    _mechanism_namespace = {}
    _test_namespace = {}

    def __init__(self, requirements, __test=False):
        """Register a new reaction mechanism.

        Parameters
        ==========
        requirements: collection
            List of requirements that provided reactants and conditions
            must meet for this reaction to be considered.
        __test: bool
            Whether or not the reaction being registered is a test
            reaction and shouldn't be in the real namespace.
        """

        self.requirements = requirements
        self.__test = __test

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
            The function that was decorated, with a `logger` attribute
            added to it.

        Notes
        =====
        Callables that are decorated with this will not have any
        difference in behavior than if they were not decorated (with the
        exception of having a `logger` attribute added to them). In
        order to get dispatching behavior, the `react` function must
        be used instead.
        """

        mechanism_function.logger = logger
        ReactionDispatcher._register(
            mechanism_function, self.requirements,
            self._ReactionDispatcher__test
        )

        return mechanism_function

    @classmethod
    def _register(cls, function, requirements, __test):
        """Register a function with the dispatch system.

        Parameters
        ----------
        function : callable
            The mechanism to be registered.
        requirements : collection
            List of requirement functions.
        __test : bool
            Whether or not to use the testing namespace.
        """

        namespace = cls._get_namespace(__test)
        cls._validate_function(function, namespace)
        cls._validate_requirements(requirements)

        name = function.__name__

        namespace[name] = {
            "requirements": requirements,
            "function": function
        }

        if not __test:
            logger.log(
                cls._REGISTERED_MECHANISM_MESSAGE.format(
                    name, requirements
                )
            )

    @classmethod
    def _get_namespace(cls, __test):
        """Get the namespace depending on if it is a test or not.

        Parameters
        ----------
        __test : bool
            The condition.

        Returns
        -------
        dict
            The namespace to be used.
        """

        return cls._test_namespace if __test else cls._mechanism_namespace

    @classmethod
    def _validate_function(cls, function, namespace):
        """Check that a function is valid.

        Parameters
        ----------
        function : callable
            A function or callable object that is serving as a reaction
            mechanism.
        namespace : dict
            The namespace being used.

        Raises
        ------
        ExistingReactionError
            The name of the function must be unique - if an existing
            mechanism shares this name it will cause an error.
        """

        mechanism_name = function.__name__

        if mechanism_name in namespace:
            message = cls._EXISTING_MECHANISM_ERROR.format(
                mechanism_name
            )
            logger.error(message)
            raise ExistingReactionError(message)

    @classmethod
    def _validate_requirements(cls, requirements):
        """Validate that the requirements are all callables.

        Parameters
        ----------
        requirements : collection
            List of all the requirements. Each must be a function or
            callable object.

        Raises
        ------
        InvalidReactionError
            If any of the requirements aren't callable then an error is
            raised.
            If the requirements is an empty list then an error is
            raised.
        """

        if not requirements:
            message = "There must be at least one requirement."
            logger.error(message)
            raise InvalidReactionError(message)

        for function in requirements:
            if not callable(function):
                if hasattr(function, '__name__'):
                    message = "Requirement named {0} is not a function.".format(
                        function.__name__
                    )
                else:
                    message = "Requirement {0} is not a function.".format(
                        function
                    )
                logger.error(message)
                raise InvalidReactionError(message)

    @classmethod
    def _generate_likely_reactions(cls, reactants, conditions, namespace):
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

        for mech_name, mech_info in six.iteritems(namespace):
            mechanism = mech_info['function']
            requirements = mech_info['requirements']

            for req_function in requirements:
                req_name = req_function.__name__
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
    def _react(cls, reactants, conditions, __test=False):
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

        namespace = cls._get_namespace(__test)

        potential_reactions = cls._generate_likely_reactions(
            reactants, conditions, namespace
        )

        for potential_reaction in potential_reactions:
            products = potential_reaction(reactants, conditions)
            logger.log(
                cls._REACTION_ATTEMPT_MESSAGE.format(
                    reactants, conditions, potential_reaction
                )
            )
            if products:
                return products

        message = cls._REACTION_FAILURE_MESSAGE.format(reactants, conditions)
        logger.log(message)
        raise FailedReactionError(message)

    @classmethod
    def _is_registered_reaction(cls, reaction, __test=False):
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

        namespace = cls._get_namespace(__test)

        if callable(reaction):
            for name, info in six.iteritems(namespace):
                if reaction is info['function']:
                    return True
            else:
                return False
        else:
            return reaction in namespace


# Provide friendlier way to call things
react = ReactionDispatcher._react
register_reaction_mechanism = ReactionDispatcher
reaction_is_registered = ReactionDispatcher._is_registered_reaction
