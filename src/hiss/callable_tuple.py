import types
import inspect

from tuple_fun import *


class CallableTuple(tuple):

    def __new__(cls, *args, **kwargs):
        return tuple.__new__(cls, args)

    def __repr__(self):
        return self.__class__.__name__ + tuple.__repr__(self)

    def __call__(self, *data, **kwargs):
        return invoke(car(self), cdr(self), data)


s = CallableTuple
s.__name__ = 's'


def invokable(prog):
    if is_primitive(prog):
        return _primitive
    if is_builtin(prog):
        return _builtin
    if is_function(prog):
        return _function
    if is_method(prog):
        return _method
    if is_class(prog):
        return _class
    if is_callable(prog):
        return _callable
    if is_literal(prog):
        return _literal


def invoke(prog, rest, data):
    return invokable(prog)(prog, rest, data)


def is_primitive(value):
    return hasattr(value, '__hiss_primitive__')


def is_builtin(value):
    return hasattr(value, '__hiss_builtin__')


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


def _primitive(primitive, program, data):
    return primitive(primitive, program, data)


def _builtin(builtin, program, data):
    (impl, spec) = builtin.__hiss_builtin__
    argspec = inspect.getargspec(spec)
    return _invoke_(builtin, program, data, argspec, impl=impl)


def _class(cls, program, data):
    argspec = inspect.getargspec(cls.__init__)
    argn = len(argspec.args) - 1
    return _invoke_(cls, program, data, argspec, argn=argn)


def _method(method, program, data):
    argspec = inspect.getargspec(method)
    argn = len(argspec.args) - 1
    return _invoke_(method, program, data, argspec, argn=argn)


def _callable(callable, program, data):
    argspec = inspect.getargspec(callable.__call__)
    argn = len(argspec.args) - 1
    return _invoke_(callable, program, data, argspec, argn=argn)


def _function(function, program, data):
    return _invoke_(function, program, data, inspect.getargspec(function))


def _invoke_(invocable, program, data, argspec, argn=None, impl=None):
    impl = impl or invocable
    argn = argn or len(argspec.args)
    args, rest = data[0:argn], data[argn:]
    if len(args) < argn:
        program = args + (invocable,) + program
        return program, rest
    else:
        value = impl(*args)
        return _literal(value, program, rest)


def _literal(literal, program, data):
    return program, (literal,)+data


def run(program, data):
    while program and data:
        program = program if isinstance(program, CallableTuple) else CallableTuple(*program)
        program, data = program(*data)
    return program, data
