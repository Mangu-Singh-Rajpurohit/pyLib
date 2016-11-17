import json
from django.http import HttpResponseBadRequest
from django.conf import settings
import traceback

class StandardReqRespMiddleware(object):

    REQ_PARAMS_KEY      = "reqParams"
    APP_PARAMS_KEY      = "appParams"
    OTHER_INFO_KEY      = "otherInfo"

    lsStdReqFields      = [REQ_PARAMS_KEY, APP_PARAMS_KEY, OTHER_INFO_KEY]

    STATUS_KEY          = "status"
    DATA_KEY            = "data"
    MESSAGE_KEY         = "msg"
    HTTP_STATUS_CODE_KEY= "httpStatusCode"

    lsStdRespFields     = [STATUS_KEY, DATA_KEY, MESSAGE_KEY]

    SUCCESS_KEY         = "success"
    FAILURE_KEY         = "failed"

    def __init__(self, *tupArgs, **kwArgs):
        for strKey, xVal in kwArgs.items():
            setattr(self, strKey, xVal)

        """__________________________________________________________________"""

    def _isDataRequest(self, request):
        if (
            request.path.find(settings.DATA_URL_PREFIX) == 1 and
            request.META["CONTENT_TYPE"].find("application/json") == 0
          ):
            return True

        return False

        """__________________________________________________________________"""

    def _isUIRequest(self, request):
        strRelativeURL = request.path
        if strRelativeURL.find(settings.UI_URL_PREFIX) == 1 or strRelativeURL[1:] == settings.FIRST_PAGE:
            return True

        return False

        """__________________________________________________________________"""

    def _getReqParamsKey(self):
        return self.REQ_PARAMS_KEY

        """__________________________________________________________________"""

    def _getSuccessKey(self):
        return self.SUCCESS_KEY

        """__________________________________________________________________"""

    def _getFailureKey(self):
        return self.FAILURE_KEY

        """__________________________________________________________________"""

    def _getStatusKey(self):
        return self.STATUS_KEY

        """__________________________________________________________________"""

    def _getDataKey(self):
        return self.DATA_KEY

        """__________________________________________________________________"""

    def _getMsgKey(self):
        return self.MESSAGE_KEY

        """__________________________________________________________________"""

    def _validateReq(self, objRequestData):
        for strRequiredField in self.lsStdReqFields:
            if not objRequestData.has_key(strRequiredField):
                raise Exception("Invalid request format. Missing required key {}".format(strRequiredField))

        """__________________________________________________________________"""

    def _getDefaultResp(self):
        dictDefaultResp = {}
        for strResponseField in self.lsStdRespFields:
            dictDefaultResp[strResponseField] = {}

        return dictDefaultResp

        """__________________________________________________________________"""

    def process_request(self, request):
        if (not self._isDataRequest(request)):
            return

        try:
            objReqData  = json.loads(request.body)
            self._validateReq(objReqData)
        except Exception as e:
            e.status = 400
            return self.process_exception(request, e, 400)

        """__________________________________________________________________"""

    def process_response(self, request, response):
        if (not self._isDataRequest(request)):
            return response

        if type(response) != dict:
          return response

        dictDefaultResp     = self._getDefaultResp()
        dictDefaultResp[self._getStatusKey()]   = self.SUCCESS_KEY
        dictDefaultResp[self._getDataKey()]     = response

        return dictDefaultResp

        """__________________________________________________________________"""

    def process_view(self, request, view, tupArgs, kwArgs):
        if (self._isDataRequest(request)):
            #import pdb
            #pdb.set_trace()
            objReqData  = json.loads(request.body)
            setattr(request, "_body", objReqData[self._getReqParamsKey()])

            try:
              return view(request, *tupArgs, **kwArgs)
            except Exception as e:
              traceback.print_exc();
              raise

        """__________________________________________________________________"""

    def process_exception(self, request, exception, httpErrorCode=500):
        if (self._isDataRequest(request)):
            dictDefaultResp     = self._getDefaultResp()
            dictDefaultResp[self._getStatusKey()]   = self.FAILURE_KEY
            dictDefaultResp[self._getDataKey()]     = {}
            dictDefaultResp["errorCode"]        = exception.status
            dictDefaultResp[self.HTTP_STATUS_CODE_KEY] = httpErrorCode

            return dictDefaultResp

        raise

        """__________________________________________________________________"""