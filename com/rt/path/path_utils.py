import os
import functools
from decorator import decorator
from com.rt.py_reflect.inspect_utils import InspectUtilities

def normalize_path_param(*tupParamNames):
    @decorator
    def normalize_decor(objCallable, *tupArgs, **dictArgs):
        dictArgs = InspectUtilities.convertPosParamsToKeyParams(objCallable, tupArgs, dictArgs)

        for strArg in tupParamNames:
            if dictArgs.has_key(strArg) and dictArgs[strArg]:
                dictArgs[strArg] = os.path.normpath(dictArgs[strArg])

        return objCallable(**dictArgs)
    return normalize_decor

def ensure_dir_path_deco(*tupParams):
    @decorator
    def ensure_dir_path(objFunc, *tupArgs, **dictKWArgs):
        dictNewArgs = InspectUtilities.convertPosParamsToKeyParams(objFunc, tupArgs, dictKWArgs)

        for strParam in tupParams:
            if dictNewArgs[strParam]:
                strParDirPath = os.path.dirname(dictNewArgs[strParam])
                if not os.path.exists(strParDirPath):
                    os.makedirs(strParDirPath)

        return objFunc(*tupArgs, **dictKWArgs)
    return ensure_dir_path

def ensure_path_exists_deco(*tupParams):
    @decorator
    def ensure_path_exists(objFunc, *tupArgs, **dictKWArgs):
        dictNewArgs = InspectUtilities.convertPosParamsToKeyParams(objFunc, tupArgs, dictKWArgs)

        for strParam in tupParams:
            if dictNewArgs[strParam]:
                if not os.path.exists(dictNewArgs[strParam]):
                    raise Exception("Path {} doesn't exists".format(dictNewArgs[strParam]))

        return objFunc(*tupArgs, **dictKWArgs)
    return ensure_path_exists

def ensure_path_deco(*tupParams):
    @decorator
    def ensure_path(objFunc):
        dictNewArgs = InspectUtilities.convertPosParamsToKeyParams(objFunc, tupArgs, kwargs)

        for strParam in tupParams:
            if dictNewArgs[strParam]:
                if not os.path.exists(dictNewArgs[strParam]):
                    os.makedirs(dictNewArgs[strParam])

        return objFunc(*tupArgs, **kwargs)
    return ensure_path

class CPathUtils(object):

    @staticmethod
    @normalize_path_param("strDirPath")
    def normalised_join(strDirPath, lsOrStrChildDirPaths):
        try:
            assert lsOrStrChildDirPaths, "lsOrStrChildDirPaths must be list or string"
        except AssertionError as e:
            return []

        if isinstance(lsOrStrChildDirPaths, basestring):
            return os.path.join(strDirPath, lsOrStrChildDirPaths)

        return map(os.path.normpath, map(functools.partial(os.path.join, strDirPath), lsOrStrChildDirPaths))

    @staticmethod
    @normalize_path_param("strSrcPath")
    def rel_path(strSrcPath, lsPaths):
        assert strSrcPath, "strSrcPath must be a valid string"
        assert lsPaths or lsPaths == [], "lsPath must be a list or string"

        if isinstance(lsPaths, basestring):
            return os.path.relpath(os.path.normpath(lsPaths), os.path.normpath(strSrcPath))

        return map(functools.partial(os.path.relpath, start = strSrcPath), lsPaths)
