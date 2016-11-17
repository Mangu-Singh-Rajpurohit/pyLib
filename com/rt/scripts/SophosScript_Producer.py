#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Krishna
#
# Created:     20/08/2016
# Copyright:   (c) Krishna 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import zlib
import Crypto.Cipher.AES

objFile = open(r"E:\temp\others\2016_08_19_14_17_28\urllist.txt", "w")
objFile.writelines(["http://www.google.co.in", "http://www.yahoo.com"])
objFile.close()

objFile = open(r"E:\temp\others\2016_08_19_14_17_28\urllist.txt", "r")
strFileContents = objFile.read()
objFile.close()

objFile = open(r"E:\temp\others\2016_08_19_14_17_28\urllist.txt", "w")

strPadding = ' ' * (16 - (len(strFileContents) % 16))
strFileContents += strPadding
strKey = "1471596448      "
objAES = Crypto.Cipher.AES.new(strKey)
objFile.write(zlib.compress(objAES.encrypt(strFileContents)))
objFile.close()
