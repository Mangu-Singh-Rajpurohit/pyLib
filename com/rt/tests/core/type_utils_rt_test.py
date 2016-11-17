import unittest
from com.rt.core.type_utils import CTypeUtils

class A(object):
    def __len__(self):
        return 5

    def __getitem__(self, iIdx):
        return 6

class B(A):

    def __iter__():
        return self

    def __next__(self):
        return 1

class C(B):

    def __setitem__(self, iIdx, val):
        pass

class TestCTypeUtils(unittest.TestCase):

    def test_isCallble(self):
        def tempFunc():
            pass

        self.assertTrue(CTypeUtils.isCallable(tempFunc))

    def test_isIndexable(self):
        self.assertTrue(CTypeUtils.isIndexable(A()))
        self.assertTrue(CTypeUtils.isIndexable([]))
        self.assertTrue(CTypeUtils.isIndexable(()))
        self.assertTrue(CTypeUtils.isIndexable({}))
        self.assertFalse(CTypeUtils.isIndexable({2}))   #   sets are not indexable
        self.assertFalse(CTypeUtils.isIndexable(object()))

    def test_isSequence(self):
        self.assertTrue(CTypeUtils.isSequence(B()))
        self.assertTrue(CTypeUtils.isSequence([]))
        self.assertTrue(CTypeUtils.isSequence(()))
        self.assertTrue(CTypeUtils.isSequence({}))
        self.assertFalse(CTypeUtils.isSequence({54}))   #   sets are not iterable
        self.assertFalse(CTypeUtils.isSequence(object()))
        self.assertFalse(CTypeUtils.isSequence(A()))

    def test_isWritableSequence(self):
        self.assertTrue(CTypeUtils.isWritableSequence([]))
        self.assertTrue(CTypeUtils.isWritableSequence({}))
        self.assertTrue(CTypeUtils.isWritableSequence(C()))
        self.assertFalse(CTypeUtils.isWritableSequence({54}))   #   sets are not writable by indexing them
        self.assertFalse(CTypeUtils.isWritableSequence(()))
        self.assertFalse(CTypeUtils.isWritableSequence(object()))
        self.assertFalse(CTypeUtils.isWritableSequence(A()))
        self.assertFalse(CTypeUtils.isWritableSequence(B()))

    def test_isIterable(self):
        self.assertTrue(CTypeUtils.isIterable([]))
        self.assertTrue(CTypeUtils.isIterable({}))
        self.assertTrue(CTypeUtils.isIterable({55}))
        self.assertTrue(CTypeUtils.isIterable(()))
        self.assertTrue(CTypeUtils.isIterable(C()))
        self.assertTrue(CTypeUtils.isIterable(B()))
        self.assertFalse(CTypeUtils.isIterable(object()))
        self.assertFalse(CTypeUtils.isIterable(A()))

if __name__ == "__main__":
    unittest.main()