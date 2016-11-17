#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      Krishna
#
# Created:     04/09/2016
# Copyright:   (c) Krishna 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

class A(object):

    def __init__(self):

        self.__a__ = "abc"
        self.pub = "TT"

    def set(self, val):
        self.__a__ = val

    def printABC(self):
        print self.__a__

    def printPublic(self):
        print self.pub

class B(A):

    def __init__(self):

        super(B, self).__init__()
        self.__a__ = "Tbc"
        self.pub = "MS"

    def spec(self):
        print self.__a__

if __name__ == '__main__':
    a = A()
    a.printABC()
    a.printPublic()
    b = B()
    b.printPublic()
    b.printABC()

    b.set("TED")
    b.printABC()
    b.spec()