from __future__ import print_function, division, unicode_literals, \
    absolute_import
from future.builtins import *
from future.builtins.disabled import *

from nose.tools import with_setup

from CAOS.dispatch import react, register_reaction_mechanism, \
    ReactionDispatcher
from CAOS.util import raises
from CAOS.exceptions.reaction_errors import FailedReactionError


def requirement1(r, c):
    return True


def requirement2(r, c):
    return False


class TestGeneratePotentialMechanisms(object):

    def teardown(self):
        for key in ['a', 'b', 'c']:
            if key in ReactionDispatcher._test_namespace:
                del ReactionDispatcher._test_namespace[key]

    # Test some stupidly simple cases without any real requirements
    def test_find_options_all_valid(self):

        @register_reaction_mechanism([requirement1], True)
        def a(r, c):
            return ["Hello, world!"]

        @register_reaction_mechanism([requirement1], True)
        def b(r, c):
            return ["Hello, world!"]

        @register_reaction_mechanism([requirement1], True)
        def c(r, c):
            return ["Hello, world!"]

        potential_mechanisms = ReactionDispatcher._generate_likely_reactions(
            None, None, ReactionDispatcher._get_namespace(True)
        )
        assert all(function in potential_mechanisms for function in [a, b, c])

    def test_find_options_some_valid(self):

        @register_reaction_mechanism([requirement1], True)
        def a(r, c):
            return ["Hello, world!"]

        @register_reaction_mechanism([requirement2], True)
        def b(r, c):
            return ["Hello, world!"]

        @register_reaction_mechanism([requirement1], True)
        def c(r, c):
            return ["Hello, world!"]

        potential_mechanisms = ReactionDispatcher._generate_likely_reactions(
            None, None, ReactionDispatcher._get_namespace(True)
        )
        assert a in potential_mechanisms
        assert c in potential_mechanisms
        assert b not in potential_mechanisms

    def test_find_options_none_valid(self):

        @register_reaction_mechanism([requirement2], True)
        def a(r, c):
            return ["Hello, world!"]

        @register_reaction_mechanism([requirement2], True)
        def b(r, c):
            return ["Hello, world!"]

        @register_reaction_mechanism([requirement2], True)
        def c(r, c):
            return ["Hello, world!"]

        potential_mechanisms = ReactionDispatcher._generate_likely_reactions(
            None, None, ReactionDispatcher._get_namespace(True)
        )

        assert not any(function in potential_mechanisms for function in [a, b, c])


class TestPerformReactions(object):

    def teardown(self):
        for key in ['a', 'b', 'c']:
            if key in ReactionDispatcher._test_namespace:
                del ReactionDispatcher._test_namespace[key]

    def test_single_option(self):
        @register_reaction_mechanism([requirement1], True)
        def a(r, c):
            return ["Hello, world!"]

        assert react(None, None, True) == ["Hello, world!"]

    def test_multiple_options(self):
        @register_reaction_mechanism([requirement1], True)
        def a(r, c):
            return ["a"]

        @register_reaction_mechanism([requirement1], True)
        def b(r, c):
            return ["b"]

        # The order is not guaranteed, but it should equal one of them.
        # This will be fixed once ordering is worked out.
        assert react(None, None, True) in (["a"], ["b"])

    def test_multiple_options_some_invalid(self):
        @register_reaction_mechanism([requirement1], True)
        def a(r, c):
            return ["a"]

        @register_reaction_mechanism([requirement1], True)
        def b(r, c):
            return ["b"]

        @register_reaction_mechanism([requirement2], True)
        def c(r, c_):
            return ["c"]
            
        assert react(None, None, True) in (["a"], ["b"])

    def test_no_options(self):
        function = react
        args = [None, None, True]
        exception_type = FailedReactionError
        assert raises(exception_type, function, args)
