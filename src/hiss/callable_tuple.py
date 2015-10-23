import types
import inspect

from tuple_fun import *


class CallableTuple(tuple):

    def __new__(cls, *args, **kwargs):
        return tuple.__new__(cls, args)

    def __repr__(self):
        return self.__class__.__name__ + tuple.__repr__(self)

    def __call__(self, *data, **kwargs):
        prog, rest = car(self), cdr(self)
        if is_function(prog):
            return _function(rest, prog, data)
        if is_method(prog):
            return _method(rest, prog, data)
        if is_class(prog):
            return _class(rest, prog, data)
        if is_callable(prog):
            return _callable(rest, prog, data)
        if is_literal(prog):
            return _literal(rest, prog, data)


s = CallableTuple
s.__name__ = 's'


def is_function(value):
    return isinstance(value, (types.FunctionType, types.LambdaType))


def is_class(value):
    return isinstance(value, types.ClassType)


def is_callable(value):
    return hasattr(value, '__call__')


def is_method(value):
    return isinstance(value, types.MethodType)


def is_literal(value):
    return True


def _class(program, cls, data):
    argspec = inspect.getargspec(cls.__init__)
    argn = len(argspec.args) - 1
    return _invoke_function(program, cls, data, argspec, argn=argn)


def _method(program, method, data):
    argspec = inspect.getargspec(method)
    argn = len(argspec.args) - 1
    return _invoke_function(program, method, data, argspec, argn=argn)

def _callable(program, callable, data):
    argspec = inspect.getargspec(callable.__call__)
    argn = len(argspec.args) - 1
    return _invoke_function(program, callable, data, argspec, argn=argn)

def _function(program, function, data):
    return _invoke_function(program, function, data, inspect.getargspec(function))


def _invoke_function(program, function, data, argspec, argn=None):
    argn = argn or len(argspec.args)
    args, rest = data[0:argn], data[argn:]
    if len(args) < argn:
        program = args + (function,) + program
        return program, rest
    else:
        value = function(*args)
        return _literal(program, value, rest)


def _literal(program, literal, data):
    return program, (literal,)+data


def run(program, data):
    while program and data:
        program = program if isinstance(program, CallableTuple) else CallableTuple(*program)
        program, data = program(*data)
    return program, data
