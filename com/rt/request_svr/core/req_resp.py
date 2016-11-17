from com.rt.core.type_utils import CTypeUtils

class Request(object):

    reqSvrIdentifier    = ""
    reqArgs             = ()
    respHandler         = None
    dictOptions         = {}

    def __init__(self, **kwArgs):
        self.__dict__.update(kwArgs)

    def __getitem__(self, idxOrKey):
        if isinstance(self.reqArgs, dict):
            return self.reqArgs[idxOrKey]

        elif isinstance(self.reqArgs, list):
            if (
                len(self.reqArgs) == 2 and
                type(self.reqArgs[0]) in (tuple, list) and
                type(self.reqArgs[1]) == dict
            ):
                try:
                    return self.reqArgs[0][idxOrKey]
                except (IndexError, TypeError) as e:
                    pass

                return self.reqArgs[1].get(idxOrKey, None)

            else:
                return self.reqArgs[idxOrKey]

        return None

class RequestMaker(object):

    @staticmethod
    def make_request(self, **dictArgs):
        objReq = Request(**dictArgs)
        return objReq