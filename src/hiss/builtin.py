import operator


def _s_builtin(fun):
    class Builtin:
        def __repr__(self):
            return fun.__name__
    return Builtin()


@_s_builtin
def add(x, y):
    return operator.add(x, y)


@_s_builtin
def sym(str):
    return intern(str)

