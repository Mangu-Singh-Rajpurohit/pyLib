#   data descr  have __set__ and __get__ method
class B(object):

    def __get__(self, ins, type = None):
        return ins, type

    def __set__(self, ins, val):
        return ins, val

#  non data descr  have only __get__ method
class C(object):
    def __get__(self, ins, type = None):
        return ins, type

class A(object):

    data = B()  #   data desc takes priority over objects' __dict__ VALUE
    nonData = C()
    def __call__(self):
        print "called"

    def __init__(self):
        self.data = "data"
        self.nonData = "nonData" # value in object's dict takes
                                # priority over on-data desc.


a = A()
a()