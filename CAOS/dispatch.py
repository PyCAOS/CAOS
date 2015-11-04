"""Handles registering and dispatching reaction mechanisms and molecule
types.  This happens dynamically, at runtime.
"""

from __future__ import print_function, division, unicode_literals

import six

from .exceptions.dispatch_errors import ExistingReactionError, \
    InvalidReactionError
from .exceptions.reaction_errors import FailedReactionError
from .logging import logger


mechanism_namespace = {}


class ReactionDispatcher(object):
    REACTION_ATTEMPT_MESSAGE = ("Trying to react reactants {}"
                                " in conditions {} as a {} type reaction.")
    REACTION_FAILURE_MESSAGE = ("Couldn't react reactants {}"
                                " in conditions {}.")

    ADDED_MECHANISM_MESSAGE = "Added mechanism {} with requirements {}."

    def __init__(self, mechanism_name, requirements):
        self._validate_mechanism_name(mechanism_name)
        self._validate_requirements(requirements)
        mechanism_namespace[mechanism_name] = requirements
        logger.log(
            ReactionDispatcher.ADDED_MECHANISM_MESSAGE.format(
                mechanism_name, six.viewkeys(requirements)
            )
        )

    def __call__(self, mechanism_function):
        def _(reactants, conditions):
            potential_reactions = self._generate_likely_reactions(
                reactants, conditions
            )

            for potential_reaction in potential_reactions:
                product = potential_reaction(reactants, conditions)
                logger.log(
                    ReactionDispatcher.REACTION_ATTEMPT_MESSAGE.format(
                        reactants, conditions, potential_reaction
                    )
                )
                if product is not None:
                    return product

            message = ReactionDispatcher.REACTION_FAILURE_MESSAGE.format(
                reactants, conditions
            )
            logger.log(message)
            raise FailedReactionError(message)

        return _

    @staticmethod
    def _validate_mechanism_name(mechanism):
        if mechanism in mechanism_namespace:
            message = "A mechanism named {} already exists.".format(mechanism)
            logger.error(message)
            raise ExistingReactionError(message)

    @staticmethod
    def _validate_requirements(requirements=None):
        for req_name, req_function in six.iteritems(requirements):
            if not six.callable(req_function):
                message = "Requirement {} is not a function.".format(req_name)
                logger.error(message)
                raise InvalidReactionError(message)
