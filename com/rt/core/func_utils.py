from com.rt.core.type_utils import CTypeUtils
from com.rt.py_reflect.reflect_utils import CReflectUtils

class RTFuncUtils(object):

    @staticmethod
    def invokeAlternatively(objCallableSpec):
        objReturnVal = None
        if CTypeUtils.isCallable(objCallableSpec) or CTypeUtils.isString(objCallableSpec):
            objOnStartMethodToInvoke    = objCallableSpec

            if CTypeUtils.isString(objCallableSpec):
                objOnStartMethodToInvoke  = CReflectUtils.resolve_name(objCallableSpec)

            objReturnVal = objOnStartMethodToInvoke()

        elif CTypeUtils.isIndexable(objCallableSpec):
            objOnStartMethodToInvoke    = objCallableSpec[0]
            tupOnStartMethodArgs        = objCallableSpec[1] if len(objCallableSpec) >= 1 else ()
            dictOnStartMethodKwArgs     = objCallableSpec[2] if len(objCallableSpec) >= 2 else {}

            if not (
                    CTypeUtils.isCallable(objOnStartMethodToInvoke) or
                    CTypeUtils.isString(objOnStartMethodToInvoke)
                    ) :
                raise Exception("Expecting a callable at first position in objCallableSpec")

            if CTypeUtils.isString(objOnStartMethodToInvoke):
                objOnStartMethodToInvoke    = CReflectUtils.resolve_name(objOnStartMethodToInvoke)

            objReturnVal = objOnStartMethodToInvoke(*tupOnStartMethodArgs, **dictOnStartMethodKwArgs)

        return objReturnVal