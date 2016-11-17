import inspect

class InspectUtilities(object):

    @staticmethod
    def convertPosParamsToKeyParams(objMethod, tupParam, dictParams):
        objArgSpecs = inspect.getargspec(objMethod)
        lsArgs      = objArgSpecs.args

        dictNewArgs = {}

        iIdx        = 0
        for iIdx, strArg in enumerate(lsArgs):
            dictNewArgs[strArg]     = dictParams.get(strArg, None)

            if not dictNewArgs[strArg]:
                if iIdx < len(tupParam):
                    dictNewArgs[strArg] = tupParam[iIdx]

        if objArgSpecs.defaults:
            lsReversedDef  = reversed(objArgSpecs.defaults)
            for iIdx, defVal in enumerate(lsReversedDef):
                strArgName = lsArgs[-(iIdx + 1)]
                if dictNewArgs[strArgName] == None:
                    dictNewArgs[strArgName] = defVal

        return dictNewArgs