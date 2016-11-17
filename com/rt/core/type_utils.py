class CTypeUtils(object):

    @staticmethod
    def isCallable(obj):
        return callable(obj)

    @staticmethod
    def isIndexable(obj):
        return hasattr(obj, "__len__") and hasattr(obj, "__getitem__")

    @staticmethod
    def isSequence(obj):
        return CTypeUtils.isIndexable(obj) and CTypeUtils.isIterable(obj)

    @staticmethod
    def isWritableSequence(obj):
        return CTypeUtils.isSequence(obj) and hasattr(obj, "__setitem__")

    @staticmethod
    def isIterable(obj):
        return hasattr(obj, "__iter__")

    @staticmethod
    def isString(obj):
        return isinstance(obj, basestring)