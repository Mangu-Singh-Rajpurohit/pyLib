import sys
import weakref

class Student(dict):

    def __len__(self):
        return 45

t = Student()
print sys.getrefcount(t)
m = weakref.ref(t)
print sys.getrefcount(t)
print t is m()


