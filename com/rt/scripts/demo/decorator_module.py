import decorator

def f(strVal):
    @decorator.decorator
    def f_n(f, *tupArgs, **kwArgs):
        print "decorator called " + str(strVal)
        t = f(*tupArgs, **kwArgs)
        return t

    return f_n


@f("TED")
@f("MSRP")
def printHelloWorld(a, b):
    """abcd"""
    print a, b

printHelloWorld("SA", "TE")