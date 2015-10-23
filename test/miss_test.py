from hamcrest import *
import unittest

from miss import miss


class MissTest(unittest.TestCase):

    def test_injects_literal(self):
        @miss(2)
        def three(two):
            return two + 1

    def test_injects_partially_applied(self):
        @miss(2)
        @miss(lambda x, y: x * y)
        def double(x):
            return x
        assert_that(double(12), equal_to(24))
