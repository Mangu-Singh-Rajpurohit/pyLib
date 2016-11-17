import unittest

from com.rt.multithreading.threading_utils import CThreadUtils

class TestCThreadUtils(unittest.TestCase):

    @staticmethod
    def onStartCB():
        print "on start cb"

    @staticmethod
    def onFinishCB():
        print "on finish cb"

    @CThreadUtils.invoke_async(
        onStartCBDtls = "com.rt.tests.multithreading.threading_utils_rt_test.TestCThreadUtils.onStartCB",
        onFinishCBDlts = "com.rt.tests.multithreading.threading_utils_rt_test.TestCThreadUtils.onFinishCB"
    )
    def test_invoke_async(self):
        print "Hello World"


if __name__ == "__main__":
    unittest.main()