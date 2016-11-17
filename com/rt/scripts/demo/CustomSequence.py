#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Krishna
#
# Created:     08/09/2016
# Copyright:   (c) Krishna 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import copy

"""
In Python 2.7, for loop works in this way :-
    for i in obj:
        print i

Here python will look for __iter__ method in obj and if present,
it uses the object returned by __iter__ method and invokes its
next() method(The object returned by __iter__ method must have
next method defined in it.

If __iter__ is not present, then it'll look for __getitem__()
method and invokes it.

If __getitem__() is also not defined, then it give error that
obj is not iterable.
"""

#   immutable sequence
#   define only __len__ and __getitem__ for immutable sequence.
class MSSequence(object):

    def __init__(self, start, stop, step):

        self.start = start
        self.stop = stop
        self.step = step

        self.len = abs((self.stop - self.start) / self.step)

    def _validateIndex(self, iIdx):
        if iIdx >= self.len:
            raise IndexError("index out of range " + str(iIdx))

    def __len__(self):
        return self.len

    def __getitem__(self, iIdx):

        self._validateIndex(iIdx)
        return (self.start) + ((iIdx - 1) * self.step)

#
class MSMutableSequence(MSSequence):

    def __init__(self, *tupArgs, **kwargs):
        self.dictVal = {}
        super(MSMutableSequence, self).__init__(*tupArgs, **kwargs)

    def __getitem__(self, iIdx):
        print "getitem called"
        return self.dictVal.get(iIdx, None) or super(MSMutableSequence, self).__getitem__(iIdx)

    def __setitem__(self, iIdx, iVal):
        self._validateIndex(iIdx)
        self.dictVal[iIdx] = iVal

    def __iter__(self):
        print "iter called"
        return MSMutableSequenceIter(self.__dict__)

class MSMutableSequenceIter(MSMutableSequence):

    curIdx = 0
    def __init__(self, dictArgs):
        self.__dict__.update(dictArgs)

    def __iter__(self):
        return self

    def next(self):
        print "next called"
        self.curIdx += 1
        try:
            return self.__getitem__(self.curIdx - 1)
        except IndexError:
            raise StopIteration

from memory_profiler import profile

@profile
def main():
    a = [1]
    b = [1, 2, 3]*int(1e5)

if __name__ == '__main__':
    main()
    a = MSMutableSequence(1, 10, 1)
    for i in a:
        print i
