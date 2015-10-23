"""

Hiss is a minimalist language built on function composition.


"""

from tuple_fun import *

VERSION = '1.0'

class CallableTuple(tuple):

    def __new__(cls, *args, **kwargs):
        return tuple.__new__(cls, args)

    def __repr__(self):
        return self.__class__.__name__ + tuple.__repr__(self)

    def __call__(self, *data, **kwargs):
        prog, rest = car(self), cdr(self)
        if is_function(prog):
            return _function(rest, prog, data)
        if is_literal(prog):
            return _literal(rest, prog, data)


CallableTuple.__name__ = 's'
s = CallableTuple


def is_function(value):
    import types
    return isinstance(value, (types.FunctionType, types.LambdaType))


def _function(program, function, data):
    arity = function.func_code.co_argcount
    args, rest = data[0:arity], data[arity:]
    if len(args) < arity:
        program = args + (function,) + program
        return program, rest
    else:
        value = function(*args)
        return _literal(program, value, rest)


def is_literal(value):
    return True


def _literal(program, literal, data):
    return program, (literal,)+data


def run(program, data):
    while program and data:
        program = program if isinstance(program, CallableTuple) \
            else CallableTuple(*program)
        program, data = program(*data)
    return program, data
