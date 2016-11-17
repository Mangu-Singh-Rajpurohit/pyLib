import os
import unittest

from com.rt.path.path_utils import CPathUtils

class TestPath_Utils(unittest.TestCase):

    def test_normalised_join(self):
        strFileName     = r"c:\temp\parentdir"
        lsFileNames     = ["ABC", "DEF", "GHI"]
        objCallableObj  = CPathUtils.normalised_join

        self.assertListEqual(objCallableObj(strFileName, None), [])

        lsVal           = objCallableObj(strFileName, lsFileNames)
        self.assertListEqual(lsVal, [
                                        r"c:\temp\parentdir\ABC",
                                        r"c:\temp\parentdir\DEF",
                                        r"c:\temp\parentdir\GHI"
                                    ])

        self.assertEqual(objCallableObj(strFileName, "ABC"), r"c:\temp\parentdir\ABC")

    def test_rel_path(self):
        strFileName     = "c:/temp"
        lsFileNames     = [r"c:\temp/temp.txt", "c:/temp/temp2.txt"]
        objCallableObj  = CPathUtils.rel_path

        self.assertRaises(AssertionError, objCallableObj, strFileName, None)
        self.assertRaises(AssertionError, objCallableObj, None, lsFileNames)

        lsVal           = objCallableObj(strFileName, lsFileNames)
        self.assertListEqual(lsVal, ['temp.txt', 'temp2.txt'])

        self.assertEqual(objCallableObj(strFileName, r"c:\temp/temp.txt"), "temp.txt")


if __name__ == "__main__":
    unittest.main()