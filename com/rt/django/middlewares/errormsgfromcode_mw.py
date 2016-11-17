import json

from django.http import HttpResponse
from com.rt.django.middlewares.standardreqresp_mw import StandardReqRespMiddleware
from django.http.response import HttpResponseBadRequest

class ErrorMsgFromCodeMiddleware(StandardReqRespMiddleware):

    dictErrorCodes  = {}

    def __init__(self, *tupArgs, **kwArgs):
        super(StandardReqRespMiddleware, self).__init__(*tupArgs, **kwArgs)

    @staticmethod
    def registerErrorCode(iErrorCode, strMsg):
        ErrorMsgFromCodeMiddleware.dictErrorCodes[iErrorCode] = strMsg

        return ErrorMsgFromCodeMiddleware

    def process_request(self, request):
      return

    def process_exception(self, request, exception, httpErrorCode=500):
      raise

    def process_view(self, request, view, tupArgs, kwArgs):
      return None

    def process_response(self, request, response):
        if (self._isDataRequest(request) and type(response) == dict):
            strStatusKey    = self._getStatusKey()
            if response[strStatusKey] == self._getFailureKey():
                iStatusCode = response.get("errorCode", 1)    #   unexpected error
                response[self._getMsgKey()]    = dictErrorCodes.get(iStatusCode)

        return response

class HttpResponseWrapperMiddleware(StandardReqRespMiddleware):

    def process_request(self, request):
      return

    def process_exception(self, request, exception, httpErrorCode=500):
      raise

    def process_view(self, request, view, tupArgs, kwArgs):
      return None


    def process_response(self, request, response):
        #import pdb
        #pdb.set_trace()
        if (self._isDataRequest(request)):
          if (response.get(self.HTTP_STATUS_CODE_KEY) == 400):
            return HttpResponseBadRequest(response)       #  for http error responses in data requests
          elif(dict == type(response)):
            return HttpResponse(json.dumps(response)) # for successful requests


        return response

