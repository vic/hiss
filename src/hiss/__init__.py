"""

Hiss is a minimalist language built on python.

"""

VERSION = '1.0'


class CallableTuple(tuple):

    def __new__(cls, *args, **kwargs):
        return tuple.__new__(cls, args)

    def __repr__(self):
        return self.__class__.__name__ + tuple.__repr__(self)


CallableTuple.__name__ = 's'
s = CallableTuple




