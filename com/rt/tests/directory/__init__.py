import os
import tempfile
import os.path
import functools

TEST_DIR_PARENT_NAME    = "directory_rtTest"
TEST_DIR_PATH           = os.path.join(os.path.abspath("."), TEST_DIR_PARENT_NAME)
TEST_DIR_STRUCT         = {}

def clearDir(strDirName):
    def delDirTree(tempArgs, dirName, lsFilesOrDirPaths):
        lsAbsFilesOrDirPaths = map(functools.partial(os.path.join, dirName), lsFilesOrDirPaths)
        map(os.unlink, filter(os.path.isfile, lsAbsFilesOrDirPaths))
        map(functools.partial(os.path.walk, func = delDirTree, arg = ()), filter(os.path.isdir, lsAbsFilesOrDirPaths))
        os.rmdir(dirName)

    os.path.walk(strDirName, delDirTree, ())

def setupTempTestDir():

    if not os.path.exists(TEST_DIR_PATH):
        os.mkdir(TEST_DIR_PATH)

    tempfile.tempdir = TEST_DIR_PATH
    strTempDir = tempfile.mkdtemp()
    return strTempDir

def teardownTempTestDir():
    clearDir(TEST_DIR_PATH)

__all__ = ("TEST_DIR_PARENT_NAME", "TEST_DIR_PATH", "TEST_DIR_STRUCT", "setupTempTestDir", "teardownTempTestDir")