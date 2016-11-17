import os
import unittest

from com.rt.directory import RTDirectory, FileSystemMappedDir, AutoGenFSMappedDir
from com.rt.tests.directory import *

class DirectoryTestCase(unittest.TestCase):

    def setUp(self):
        setupTempTestDir()
        self.objDir = RTDirectory()

    def tearDown(self):
        self.objDir = None
        teardownTempTestDir()

    def test_name(self):
        self.assertRaises(AssertionError, getattr, self.objDir, "name")
        self.objDir.name = "ABC"
        self.assertEqual("ABC", self.objDir.name)

    def test_path(self):
        self.assertRaises(AssertionError, getattr, self.objDir, "path")
        self.objDir.path = r"c:/temp/temp1.txt"
        self.assertEqual(self.objDir.path, os.path.normpath(self.objDir.path))
        self.objDir.name = "SBD.MS"
        self.assertEqual(self.objDir.path, os.path.normpath(os.path.join(self.objDir.parent, self.objDir.name)))

    def test_parent(self):
        self.assertRaises(AssertionError, getattr, self.objDir, "parent")
        self.objDir.parent = "ABC"
        self.assertEqual("ABC", self.objDir.parent)

    def test_name_path_parent(self):
        self.assertRaises(AssertionError, getattr, self.objDir, "path")
        self.objDir.path = r"c:/temp/temp1.txt"

        self.assertEqual(self.objDir.path, os.path.normpath(self.objDir.path))
        self.assertEqual(self.objDir.parent, os.path.dirname(os.path.normpath(self.objDir.path)))
        self.assertEqual(self.objDir.name, os.path.basename(os.path.normpath(self.objDir.path)))

    def test_integrated_test(self):
        objDir = FileSystemMappedDir()
        objDir.path = r"E:\temp1"
        objDir.loadFromFS()

        objDir1 = AutoGenFSMappedDir()
        objDir1.path = "e:/tempABC"
        objDir1.dictFileSys = objDir.dictFileSys
        objDir1.create()

        objDir1.delete_dir_recursive()

        print objDir.search("*.txt", bSearchRecursively = True, bReturnAbsPaths = False)
        print objDir.search("*.txt", bSearchRecursively = True, bReturnAbsPaths = True)
        print objDir.search("*.txt", bSearchRecursively = True,
                            bReturnAbsPaths = True, bReturnDirectory = True
                        )
        print objDir.search("*", bSearchRecursively = True,
                            bReturnAbsPaths = True, bReturnDirectory = True
                        )
        print objDir.search("*.txt", bSearchRecursively = True,
                            bReturnAbsPaths = True, bReturnDirectory = False
                        )

if __name__ == "__main__":
    unittest.main()