import threading
from decorator import decorator
import com.rt.core.type_utils as rt_type_utils
import com.rt.core.func_utils as rt_func_utils

objIsCallble    = rt_type_utils.CTypeUtils.isCallable
objIsSequence   = rt_type_utils.CTypeUtils.isIndexable
objInvokeAlternatively = rt_func_utils.RTFuncUtils.invokeAlternatively

class CThreadUtils(object):

    @staticmethod
    def invoke_async(onStartCBDtls = None, onFinishCBDlts = None, *tupArgs, **kwArgs):
        @decorator
        def invoke_async_decorator(objCB, *tupInnerArgs, **dictInnerArgs):
            def temp_wrapper(objCallable, onStartCBDtls = None, onFinishCBDlts = None,
                                        *tupArgsTempWrapper, **kwArgsTempWrapper):

                if not objIsCallble(objCallable):
                    raise Exception("Expecting callable to be executed in thread")

                objInvokeAlternatively(onStartCBDtls)
                objReturnVal = objCallable(*tupArgsTempWrapper, **kwArgsTempWrapper)
                objInvokeAlternatively(onFinishCBDlts)

            tupNewArgs = (objCB, onStartCBDtls, onFinishCBDlts) + tupInnerArgs
            objThread = threading.Thread(target = temp_wrapper, args = tupNewArgs, kwargs = dictInnerArgs)
            objThread.start()
        return invoke_async_decorator