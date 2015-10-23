
def hiss_primitive(spec=None):
    def decorator(fun):
        fun.__hiss_primitive__ = (spec,)
        return fun
    return decorator

@hiss_primitive()
def quote(self, program, data):
    return program, data

