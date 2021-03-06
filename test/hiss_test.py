from hamcrest import *
import unittest

from hiss.callable_tuple import s, run
from hiss.builtin import *
from hiss.primitive import *


class HissTest(unittest.TestCase):

    def test_has_a_version(self):
        from hiss import VERSION
        assert_that(VERSION, not_none())


class TupleFunTest(unittest.TestCase):

    def test_car_returns_first_element(self):
        from hiss.tuple_fun import car
        x = s(1, 2)
        assert_that(car(x), equal_to(1))

    def test_cdr_return_rest_of_tuple(self):
        from hiss.tuple_fun import cdr
        x = s(1, 2)
        assert_that(cdr(x), equal_to((2,)))


def assert_s(program, data, expected_program=None, expected_data=None):
    real_program, real_data = run(program, data)
    if expected_program is not None:
        assert_that(real_program, equal_to(expected_program))
    if expected_data is not None:
        assert_that(real_data, equal_to(expected_data))
    return real_program, real_data


class CallableTupleTest(unittest.TestCase):

    def test__repr__includes_s(self):
        x = s(1, 2)
        assert_that(x.__repr__(), equal_to("s(1, 2)"))

    def test_program_literal_produces_value(self):
        assert_s(
            program=(1,), data=(2,),
            expected_program=(), expected_data=(1, 2))

    def test_program_seq_of_literals(self):
        assert_s(
            program=(1, 2, 3), data=(),
            expected_program=(1, 2, 3), expected_data=())


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

    def test_constructor_invoked(self):
        class Foo:
            def __init__(self, bar):
                self.bar = bar

        _, (foo,) = assert_s(
            program=(Foo,),
            data=(3,),
            expected_program=(),
        )
        assert_that(foo.bar, equal_to(3))

    def test_invokes_bound_method(self):
        class Foo:
            def __init__(self, a):
                self.a = a

            def bar(self, x):
                return self.a + x

        assert_s(
            program=(Foo(99).bar,),
            data=(1,),
            expected_program=(),
            expected_data=(100,)
        )

    def test_invokes_callable_object(self):
        class Foo:
            def __call__(self, a):
                return 12 * a
        assert_s(program=(Foo(),),
                 data=(2,),
                 expected_program=(),
                 expected_data=(24,))


class CoreTest(unittest.TestCase):

    def test_concat_and_create_symbol(self):
        assert_s(
            program=('hell', add, sym),
            data=('o',),
            expected_program=(), expected_data=('hello',)
        )


    def test_quote_value(self):
        program, data = assert_s(
            program=(quote,3),
            data=(1,2),
        )
        raise ArithmeticError, (program, data)



