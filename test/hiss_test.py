from hamcrest import *
import unittest
import hiss
from hiss import s


class HissTest(unittest.TestCase):

    def test_has_a_version(self):
        assert_that(hiss.VERSION, not_none())


class CallableTupleTest(unittest.TestCase):

    def test__repr__includes_s(self):
        x = s(1, 2)
        assert_that(x.__repr__(), equal_to("s(1, 2)"))

