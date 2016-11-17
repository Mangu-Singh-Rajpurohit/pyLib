#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Krishna
#
# Created:     11/09/2016
# Copyright:   (c) Krishna 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import fnmatch
import functools
import collections

from com.rt.path.path_utils import CPathUtils, normalize_path_param, ensure_dir_path_deco, ensure_path_exists_deco
from com.rt.core.process_utils import ProcessUtils

class ContentDirMixin(object):

    FILE_LABEL      = "files"
    DIR_LABEL       = "dirs"
    dictFileSys     = {}

    def get_file_label(self):
        return self.FILE_LABEL

    def get_dir_label(self):
        return self.DIR_LABEL

    def printTree(self, strNodeName = None, objCurNode = None, iLevel = 1):

        if not strNodeName:
            strNodeName = self.path

        if not objCurNode:
            objCurNode  = self.dictFileSys

        print (" " * iLevel) + " + " + strNodeName

        for strFileName in objCurNode[self.get_file_label()]:
            print (" " * (iLevel + 2)) + " - " + strFileName

        for strDirName, dictVal in objCurNode[self.get_dir_label()].items():
            self.printTree(strDirName, dictVal, iLevel + 1)

class FileSystemMappedDirMixin(ContentDirMixin):

    def _getCurrentDirDict(self, strDirName):
        strRelPath  = os.path.relpath(os.path.normpath(strDirName), self.path)

        if strRelPath == os.curdir:
            return self.dictFileSys

        lsComponents= strRelPath.split(os.sep)
        assert len(lsComponents) > 0
        objDict     = self.dictFileSys

        for strComponent in lsComponents:
            objDict = objDict[self.get_dir_label()][strComponent]

        return objDict

    def loadFromFS(self, **dictKWArgs):
        strDirLabel     = self.get_dir_label()
        strFileLabel    = self.get_file_label()

        def _categorizeFileAndDir(tempArg, strDirName, lsFilesAndDirs):
            dictTarget                  = self._getCurrentDirDict(strDirName)
            objDefaultDict              = collections.defaultdict(dict)
            dictTarget[strDirLabel]     = objDefaultDict
            lsAbsPaths                  = map(functools.partial(os.path.join, strDirName), lsFilesAndDirs)
            lsDirPaths                  = filter(lambda x: os.path.isdir(x), lsAbsPaths)
            lsDirNames                  = map(os.path.basename, filter(lambda x: os.path.isdir(x), lsAbsPaths))

            lsDicts = map(objDefaultDict.__getitem__, lsDirNames)
            dictTarget[strFileLabel]    = map(os.path.basename, filter(lambda x: os.path.isfile(x), lsAbsPaths))
            assert len(lsDirPaths) == len(lsDicts)

        os.path.walk(self.path, _categorizeFileAndDir, None)

class AutoGenFSMappedDirMixin(ContentDirMixin):

    def createFile(self, strFileName):
        objFile = open(strFileName, "w")
        objFile.close()

    def create(self, strCurNodeName = None, objCurNode = None):
        if strCurNodeName == None:
            strCurNodeName = self.path

        if objCurNode == None:
            objCurNode = self.dictFileSys

        if not (os.path.exists(strCurNodeName) and os.path.isdir(strCurNodeName)):
            os.makedirs(strCurNodeName)

        for strFileName in objCurNode[self.get_file_label()]:
            self.createFile(os.path.join(strCurNodeName, strFileName))

        for strDirName, dictVal in objCurNode[self.get_dir_label()].items():
            self.create(os.path.join(strCurNodeName, strDirName), dictVal)

class RTDirectory(object):

    _name           = ""
    _parent         = ""
    _path           = ""

    def __init__(self, **dictArgs):
        self.dictFileSys = {}
        self.__dict__.update(**dictArgs)

    def _set_path(self):
        try:
            self._path = os.path.join(self.parent, self.name)
        except AssertionError as e:
            pass

    def _set_name_parent(self):
        self.parent, self.name = os.path.split(self.path)

    @property
    def name(self):
        assert self._name, "{} not set".format(self._name)
        return self._name

    @name.setter
    def name(self, value):
        assert value, "Invalid value received".format(value)
        self._name = os.path.normpath(value)
        self._set_path()

    @property
    def parent(self):
        assert self._parent, "{} not set".format(self._parent)
        return self._parent

    @parent.setter
    def parent(self, value):
        assert value, "{} not set".format(value)
        self._parent = os.path.normpath(value)
        self._set_path()

    @property
    def path(self):
        if not self._path:
            self._path = os.path.normpath(os.path.join(self.parent, self.name))

        return self._path

    @path.setter
    def path(self, val):
        self._path = os.path.normpath(val)
        self._set_name_parent()

    @staticmethod
    def search_static(
        strPath, strPattern = "*",
        bSearchRecursively  = False,
        bReturnDirectory    = False,
        bReturnAbsPaths     = True
    ):
        lsSearchResults     = []
        for strDirName, lsSubDir, lsFiles in os.walk(strPath):
            if bReturnDirectory:
                for strDir in lsSubDir:
                    if fnmatch.fnmatch(strDir, strPattern):
                        if bReturnAbsPaths:
                            lsSearchResults.append(os.path.normcase(os.path.join(strDirName, strDir)))
                        else:
                            lsSearchResults.append(strDir)
            else:
                for strFile in lsFiles:
                    if fnmatch.fnmatch(strFile, strPattern):
                        if bReturnAbsPaths:
                            lsSearchResults.append(os.path.normcase(os.path.join(strDirName, strFile)))
                        else:
                            lsSearchResults.append(strFile)

            if not bSearchRecursively:
                break

        return lsSearchResults

    def search(
            self, strPattern    = "*",
            bSearchRecursively  = False,
            bReturnDirectory    = False,
            bReturnAbsPaths     = True
        ):

        return RTDirectory.search_static(
            self.path, strPattern,
            bSearchRecursively, bReturnDirectory,
            bReturnAbsPaths
        )

    def delete_dir(self):
        self.delete_dir_static(self.path)

    @staticmethod
    def delete_dir_static(strPath):
        return ProcessUtils.run_cmd('rmdir /S /Q "' + strPath + '"' )

    def delete_dir_recursive(self):
        self.delete_dir_recursive_static(self.path)

    @staticmethod
    def delete_dir_recursive_static(strDirPath):
        t = os.walk(strDirPath)
        (strDir, lsDirs, lsFiles) = next(t)
        if lsFiles:
            map(os.unlink, CPathUtils.normalised_join(strDir, lsFiles))

        if lsDirs:
            map(RTDirectory.delete_dir_recursive_static, CPathUtils.normalised_join(strDir, lsDirs))

        RTDirectory.delete_dir_static(strDir)

    @staticmethod
    def copy_dir_static(*tupArgs, **dictArgs):
        dictArgs["objCallable"] = RTDirectory.copy_files_static
        RTDirectory._traverse_dir_static(*tupArgs, **dictArgs)

    @staticmethod
    def move_dir_static(*tupArgs, **dictArgs):
        dictArgs["objCallable"] = RTDirectory.move_files_static
        RTDirectory._traverse_dir_static(*tupArgs, **dictArgs)

    @staticmethod
    def _traverse_dir_static(strSrcPath, strDestPath,
                            strPattern = "*", bCopyRecursively = True,
                            objCallable = None):

        lsFileNames = RTDirectory.search_static(strSrcPath, strPattern, bCopyRecursively)
        lsRelPaths  = CPathUtils.rel_path(strSrcPath, lsFileNames)
        lsNewPaths  = CPathUtils.normalised_join(strDestPath, lsRelPaths)
        objCallable(lsFileNames, lsNewPaths)

    @staticmethod
    @normalize_path_param("strSrcPath", "strDestPath")
    @ensure_dir_path_deco("strDestPath")
    @ensure_path_exists_deco("strSrcPath")
    def copy_file_static(strSrcPath, strDestPath):
        assert os.path.exists(strSrcPath), "Src {} doesn't exists. ".format(strSrcPath)
        with open(strSrcPath, "rb") as objSrc:
            with open(strDestPath, "wb") as objDest:
                while True:
                    strVal = objSrc.read(10000)
                    if len(strVal) <= 0:
                        break
                    objDest.write(strVal)

    @staticmethod
    def copy_files_static(lsSrcPath, lsDestPath):
        map(RTDirectory.copy_file_static, lsSrcPath, lsDestPath)

    @staticmethod
    def move_files_static(lsSrcPath, lsDestPath):
        map(RTDirectory.move_file_static, lsSrcPath, lsDestPath)

    @staticmethod
    @normalize_path_param("strOldLoc", "strNewLoc")
    def move_file_static(strOldLoc, strNewLoc):
        os.rename(strOldLoc, strNewLoc)

class FileSystemMappedDir(RTDirectory, FileSystemMappedDirMixin):
    pass

class AutoGenFSMappedDir(RTDirectory, AutoGenFSMappedDirMixin):
    pass

if __name__ == '__main__':
    objDir = FileSystemMappedDir()
    objDir.path = r"E:\temp1"
##    objDir.loadFromFS()
##
##    objDir1 = AutoGenFSMappedDir()
##    objDir1.path = "e:/tempABC"
##    objDir1.dictFileSys = objDir.dictFileSys
##    objDir1.create()
##
##    objDir1.delete_dir_recursive()
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

    #RTDirectory.copy_dir_static(r"E:\code\Codebase\New Code\python\com\rt\tests", r"e:/asdfasdf/asdfasdfa", "*.*")
    objDir1 = AutoGenFSMappedDir()
    objDir1.path = "e:/asdfasdf/asdfasdfa"
    objDir1.delete_dir_recursive()

##directory comparision
##directory initialization from filesystem
##directory traversal
##directory copy
##directory search and copy
##deleting directory
##renaming directory
##zipping directory
##changing directory attributes
##directory exists

