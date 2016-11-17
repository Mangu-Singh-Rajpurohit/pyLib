from pydoc import safeimport

class CReflectUtils(object):

    @staticmethod
    def resolve_name(path, forceload=0):
        """Locate an object by name or dotted path, importing as necessary."""
        parts = [part for part in path.split('.') if part]
        module, n = None, 0
        while n < len(parts):
            nextmodule = safeimport('.'.join(parts[:n+1]), forceload)
            if nextmodule:
                module, n = nextmodule, n + 1
            else:
                break
        if module:
            object = module
        else:
            object = __builtin__

        for part in parts[n:]:
            try:
                object = getattr(object, part)
            except AttributeError:
                return None
        return object

t = CReflectUtils.resolve_name("com.rt.py_reflect.inspect_utils.InspectUtilities.convertPosParamsToKeyParams")