#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Krishna
#
# Created:     27/08/2016
# Copyright:   (c) Krishna 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from itertools import *
import sys
import logging

class LoggerMeta(type):

    def __new__(cls, *tupArgs, **kwArgs):
        kwArgs["logger"] = logging.Logger()
        inst = super(LoggerMeta, cls).__new__(*tupArgs, **kwArgs)
        return inst

class StudentFilter(logging.Filter):

    def filter(self, record):
        return True

class Student(object):
    iRollNo = 0
    strName = ""
    dPercent = 0.0
    logger = logging.Logger("rt.scripts.demo.IdealClass.Student")
    logger.addFilter(StudentFilter())
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.setLevel(logging.INFO)
    logger.info("Student Logger created")
    logger.propagate = True
    logger.info("Student propogate set to True")

    def __init__(self, **dictArgs):
        self.logger.debug("Student object created")
        self.__dict__.update(dictArgs)

    def __unicode__(self):
        return "Roll No : {}, Name : {}, Percent : {}".format(
                self.iRollNo, self.strName, self.dPercent)

    def __str__(self):
        return unicode(self).encode("UTF-8")

    def __cmp__(self, b):
        if not isinstance(b, Student):
            raise Exception("Non-Student type received as argument " + b)
        if self.dPercent > b.dPercent:
            return 1
        elif self.dPercent < b.dPercent:
            return -1
        return 0

class Temp(object):

    logger = logging.Logger("rt.scripts.demo.IdealClass.Temp")

    def __init__(self):
        self.logger.debug("Temp object created")

if __name__ == '__main__':

    logging.basicConfig(level = logging.DEBUG)
    logging.debug("Script starts")

    lsStudents = []
    lsStudents.append(Student(strName = "Viru", dPercent = 45))
    lsStudents.append(Student(strName = "Sachin", dPercent = 54))
    lsStudents.append(Student(strName = "Viru", dPercent = 50))

    lsStudents.append(Student(strName = "Saurav", dPercent = 56))
    lsStudents.append(Student(strName = "Sachin", dPercent = 51))

    for strGroup, lsGrpMembers in groupby(sorted(lsStudents), lambda objStudent: objStudent.strName):
        if strGroup == "Sachin":
            print map(str, map(lambda objStdTemp: objStdTemp.dPercent * 2, lsGrpMembers))
        elif strGroup == "Viru":
            print map(str, map(lambda objStdTemp: objStdTemp.dPercent * 4, lsGrpMembers))
        elif strGroup == "Saurav":
            print map(str, map(lambda objStdTemp: objStdTemp.dPercent * 5, lsGrpMembers))

    print lsGrpMembers
    import sys
    print sys.argv
    a = Temp()
    b = Student()
    logging.debug("Script ends")