import requests
from com.rt.request_svr.core.base import RequestSvrMixin
from com.rt.request_svr.core.req_resp import RequestMaker

class HttpRequestSvrMixin(RequestSvrMixin):

    def makeRequest(self, objReq = None, **kwArgs):
        if objReq.dictOptions.get("statelessRequest", False):
            self.makeStatelessRequest(objReq, **kwArgs)

        if objReq == None:
            objReq = RequestMaker.make_request(*kwArgs)

    def makeStatelessRequest(self, objReq = None, **kwArgs):
        if objReq == None:
            objReq = RequestMaker.make_request(*kwArgs)

        url             = objReq["url"]
        method          = objReq["method"] or "GET"
        dictOtherOpts   = objReq["reqOpts"] or {}
        resp            = requests.request(method, url, **dictOtherOpts)