import operator


def hiss_builtin(impl, spec):
    def decorator(fun):
        fun.__hiss_builtin__ = (impl, spec)
        return fun
    return decorator


@hiss_builtin(operator.add, lambda x, y: None)
def add():
    pass


@hiss_builtin(intern, lambda x: None)
def sym():
    pass


