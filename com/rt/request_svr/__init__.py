"""
RequestSvrMixin
	->	makeSingleRequest
	->	makeNRequest
	->	makeRequest

AsynchronousRequestSvrMixin
	->	makeRequest

ParallelRequestSvrMixin
	->	makeRequest

HttpRequestSvrMixin
	->	makeSingleRequest
	->	makeNRequest
	->	makeRequest
	->	makeStatelessRequest

RequestTrackerMixin
	->	lsRequest
	->	repeatPrevRequest

RequestMixin
HttpRequestMixin
HttpResponseMixin

HttpRequestMaker
	->	makeRequest

ResponseHandler
	->	__init__(response, successHandler, failureHandler)
	->	_processedResponse

JSONResponseHandler
	->	_processedResponse

XMLResponseHandler
	->	_processedResponse

FileOutputResponseHandler
	->	_processHandler
"""