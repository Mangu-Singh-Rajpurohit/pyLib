#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Krishna
#
# Created:     10/11/2016
# Copyright:   (c) Krishna 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import time
import sys
sys.setrecursionlimit(10000)

def memoize(func):
   dictOut = {}
   def out(i):
       if dictOut.get(i) != None:
          return dictOut[i]
       out = func(i)
       dictOut[i] = out
       return out
   return out

@memoize
def findFact(i):
    return 1 if i <= 1 else i * findFact(i - 1)

startTime = time.time()
totalSum = 0
for i in range(4000):
   totalSum += findFact(i)

endTime = time.time()
print totalSum, endTime - startTime
