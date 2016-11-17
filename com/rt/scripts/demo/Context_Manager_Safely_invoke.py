#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Krishna
#
# Created:     09/09/2016
# Copyright:   (c) Krishna 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import contextlib

@contextlib.contextmanager
def safelyinvoke(defaultObj):
    try:
        yield defaultObj
    except Exception as e:
        print str(e)
    finally:
        print "Executing finally"

def divOp(no1, no2):
    return no1/ no2

def main():
    with safelyinvoke(6) as returnType:
        #returnType = divOp(5, 2)
        returnType = divOp(4, 0)
        #print divOp(4, 2)

    print returnType
    #print divOp(4, 1)

class ParClosable(object):

    class Temp(object):

        def __get__(self, *tupArgs, **kwargs):
            print tupArgs, kwargs
            return 455

    b = property(lambda x: 444)
    c = Temp()

class Closable(ParClosable):

    a = 23
    b = 23
    def close(self):
        print "closing"

if __name__ == '__main__':
    main()
    with contextlib.closing(Closable()):
        print "in context"
