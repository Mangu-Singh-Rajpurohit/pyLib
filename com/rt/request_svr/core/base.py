from com.rt.multithreading.threading_utils import CThreadUtils

class RequestSvrMixin(object):

    def makeSingleRequest(self, *tupArgs, **kwArgs):
        makeRequest(*tupArgs, **kwArgs)

    def makeNRequest(self, iNo, *tupArgs, **kwArgs):
        for i in xrange(iNo):
            self.makeRequest(*tupArgs, **kwArgs)

    def makeRequest(self, *tupArgs, **kwArgs):
        raise NotImplemented("Implement this method in chiid classes")

class AsynchronousRequestSvrMixin(object):

    @CThreadUtils.invoke_async()
    def makeRequest(self, *tupArgs, **kwArgs):
        objCallable = super(AsynchronousRequestSvrMixin, self).makeRequest
