import unittest
from com.rt.core.func_utils import RTFuncUtils

objCallble = RTFuncUtils.invokeAlternatively

class TestRTFuncUtils(unittest.TestCase):

    @staticmethod
    def tempMethod(a, b):
        return a + b

    @staticmethod
    def tempMethod1():
        return "Hello World"

    def test_invokeAlternatively(self):
        out = objCallble([TestRTFuncUtils.tempMethod, (2, 3), {}])
        self.assertEqual(out, 5)
        out = objCallble([TestRTFuncUtils.tempMethod, (2,), {"b": 5}])
        self.assertEqual(out, 7)
        out = objCallble(TestRTFuncUtils.tempMethod1)
        self.assertEqual(out, "Hello World")

        strMethod = "com.rt.tests.core.func_utils_rt_test.TestRTFuncUtils.tempMethod"

        out = objCallble([strMethod, (2, 3), {}])
        self.assertEqual(out, 5)
        out = objCallble([strMethod, (2,), {"b": 5}])
        self.assertEqual(out, 7)
        out = objCallble(strMethod + "1")
        self.assertEqual(out, "Hello World")

if __name__ == "__main__":
    unittest.main()