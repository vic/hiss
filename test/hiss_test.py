from hamcrest import *
import unittest
from hiss import s, run
from hiss.tuple_fun import *


class HissTest(unittest.TestCase):

    def test_has_a_version(self):
        import hiss
        assert_that(hiss.VERSION, not_none())


class TupleFunTest(unittest.TestCase):

    def test_car_returns_first_element(self):
        x = s(1, 2)
        assert_that(car(x), equal_to(1))

    def test_cdr_return_rest_of_tuple(self):
        x = s(1, 2)
        assert_that(cdr(x), equal_to((2,)))


def assert_s(program, data, expected_program, expected_data):
    real_program, real_data = run(program, data)
    assert_that(real_data, equal_to(expected_data))
    assert_that(real_program, equal_to(expected_program))


class CallableTupleTest(unittest.TestCase):

    def test__repr__includes_s(self):
        x = s(1, 2)
        assert_that(x.__repr__(), equal_to("s(1, 2)"))

    def test_program_literal_produces_value(self):
        assert_s(
            program=(1,), data=(2,),
            expected_program=(), expected_data=(1, 2))

    def test_program_pure_invokes_function(self):
        add = lambda x, y: x + y
        assert_s(
            program=(add, add),
            data=(1, 2, 3),
            expected_program=(), expected_data=(6,))

    def test_program_pure_curries_function(self):
        add = lambda x, y: x + y
        assert_s(
            program=(add, add),
            data=(1, 2),
            expected_program=(3, add), expected_data=())

    def test_program_pure_continues(self):
        add = lambda x, y: x + y
        assert_s(
            program=(3, add),
            data=(1, 2),
            expected_program=(), expected_data=(4, 2))


