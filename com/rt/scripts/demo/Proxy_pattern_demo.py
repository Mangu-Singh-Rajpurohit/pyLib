class Student(object):

    rollNo  = 0
    name    = ""

    def __unicode__(self):
        return u"RollNo : {}, Name : {}".format(self.rollNo, self.name)

    def __str__(self):
        return self.__unicode__().encode("UTF-8")

class StudentProxy(object):

    _lsPrivateAttrs = ["closed", "close", "objStd"]
    def __new__(cls, *tupArgs, **kwArgs):
        objStd      = Student(*tupArgs, **kwArgs)
        objNewObj   = super(StudentProxy, cls).__new__(cls, *tupArgs, **kwArgs)
        objNewObj.objStd = objStd
        objNewObj.closed = False
        return objNewObj

    def __getattribute__(self, attr):
        objClosed   = super(StudentProxy, self).__getattribute__("closed")
        lsPrivateAttrs = super(StudentProxy, self).__getattribute__("_lsPrivateAttrs")
        if objClosed and (attr not in lsPrivateAttrs):
            raise Exception("You can not access closed object")

        if attr in lsPrivateAttrs:
            return super(StudentProxy, self).__getattribute__(attr)

        objStd = super(StudentProxy, self).__getattribute__("objStd")
        return getattr(objStd, attr)

    def __setattr__(self, attr, val):
        if attr in self._lsPrivateAttrs:
            raise Exception("Can not set the value of " + attr)

        setattr(self.objStd, attr, val)

    def __str__(self):
        return str(self.objStd)

    def close(self):
        self.closed = True

class StudentProxy1(object):

    _closed = False
    objStd  = None
    def __new__(cls, *tupArgs, **kwArgs):
        objStd                       = Student(*tupArgs, **kwArgs)
        objNewObj                    = super(StudentProxy1, cls).__new__(cls, *tupArgs, **kwArgs)
        objNewObj.__dict__["objStd"] = objStd

        return objNewObj

    def __getattribute__(self, attr):
        #   see if the attribute is the part of proxy class.
        try:
            attrVal     = super(StudentProxy1, self).__getattribute__(attr)
        except AttributeError as e:
            pass
        else:
            return attrVal

        #   if attribute is not the part of proxy class, then check
        #   if it's still valid to access contained/proxied class.
        objClosed       = super(StudentProxy1, self).__getattribute__("_closed")
        if objClosed:
            raise Exception("You can not access closed object")

        #   access contained/proxy class method.
        objStd          = super(StudentProxy1, self).__getattribute__("objStd")
        return getattr(objStd, attr)

    def __setattr__(self, attr, val):
        #   Don't allow the user to set the value of any
        #   variables of proxy class(as they are all
        #   internally set.
        if attr in self.__dict__:
            raise Exception("Can not set the value of " + attr)

        #   check if it's still valid reference to contained/proxied
        #   object.
        if getattr(self, "_closed"):
            raise Exception("You can not access closed object")

        #   set attribute of proxied class.
        setattr(self.objStd, attr, val)

    def __str__(self):
        if self._closed:
            return "Can not print closed object"
        return str(self.objStd)

    def close(self):
        self.__dict__["_closed"] = True

objStudent = StudentProxy1()
print str(objStudent)
objStudent.name = "Sachin"
print str(objStudent)
objStudent.close()
print str(objStudent)
objStudent.name = "Sachin1"