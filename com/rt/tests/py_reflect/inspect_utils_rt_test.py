import unittest
from com.rt.py_reflect.inspect_utils import InspectUtilities

class InspectTestCase(unittest.TestCase):

    def inspect_func_deco(func):
        def newFunc(*tupArgs, **kwArgs):
            return InspectUtilities.convertPosParamsToKeyParams(func, tupArgs, kwArgs)

        return newFunc

    @inspect_func_deco
    def inspect_func(self, no1, no2 = 43, no3 = 34, *tupArgs, **kwArgs):
        return None

    def test_convertPosParamsToKeyParams(self):
        self.assertDictEqual(self.inspect_func(1, 2, 3),
                {'self': self, 'no1': 1, 'no2': 2, 'no3': 3})
        self.assertDictEqual(self.inspect_func(1),
                {'self': self, 'no1': 1, 'no2': 43, 'no3': 34})
        self.assertDictEqual(self.inspect_func(333, no3 = 445),
                {'self': self, 'no1': 333, 'no2': 43, 'no3': 445})

if __name__ == "__main__":
    unittest.main()