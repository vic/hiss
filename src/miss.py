import types


def miss(thing):
    """ Little Miss - A minimal SS prove of concept """
    def decorator(fun):
        def decorated(*args, **kwargs):
            if _is_fun(thing):
                return _apply_fun(thing, fun, args, kwargs)
            return _apply_value(thing, fun, args, kwargs)
        return decorated
    return decorator


def _is_fun(thing):
    return isinstance(thing, (types.FunctionType, types.LambdaType))


def _apply_fun(thing, fun, args, kwargs):
    result = thing(*args, **kwargs)
    result = result if isinstance(result, tuple) \
        else (result, )
    return fun(*result)


def _apply_value(thing, fun, args, kwargs):
    args = (thing, ) + args
    return fun(*args, **kwargs)


