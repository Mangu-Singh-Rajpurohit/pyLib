#-------------------------------------------------------------------------------
# Name:         SophosScript.py
# Purpose:      Daemon service, which can watch for the changes made at, shared
#               storage location.
#
# Author:      Mangu Singh Rajpurohit
#
# Created:     19/08/2016
#-------------------------------------------------------------------------------

#   imports
import os
import time
import zlib
import requests
import Crypto.Cipher.AES

"""
NOTE :- Following assumptions are made, while writing this service :-
        1)  Gzip compression algorithm is used to compress file
        2)  AES cipher is used for compression and key size is 128 bits.
"""

class RecurringURISvc(object):

    TIMESTAMP_FMT = "%Y_%m_%d_%H_%M_%S"     #   timestamp format

    def __init__(self, strSharedLoc, iPollingIntervalInSeconds = 60, *tupArgs, **kwargs):
        """
        Constructor Method
        Initializes sharedLocation path and polling interval.
        """
        super(RecurringURISvc, self).__init__(*tupArgs, **kwargs)
        self.strSharedLoc = strSharedLoc
        self.strLastInspectedFolder = ""
        self.iPollingIntervalInSeconds = iPollingIntervalInSeconds

        ########################################################################

    def checkForUpdate(self):
        """
        Checks whether new folder have been published on a given shared location.
        """
        bHasUpdated = True
        lsDirInSharedLoc = os.listdir(self.strSharedLoc)

        if not self.strLastInspectedFolder:
            if len(lsDirInSharedLoc) <= 0:
                bHasUpdated = False
            else:
                self.strLastInspectedFolder = lsDirInSharedLoc[0]
        else:
            if len(lsDirInSharedLoc) > 0:
                if lsDirInSharedLoc[0] == self.strLastInspectedFolder:
                    bHasUpdated = False
                else:
                    self.strLastInspectedFolder = lsDirInSharedLoc[0]

        return bHasUpdated
        ########################################################################

    def getUnixEpochFromTimestamp(self, strDirName):
        """
        Returns time since unix epoch from human readable timestamp value.
        """
        objDt = time.strptime(strDirName, self.TIMESTAMP_FMT)
        return int(time.mktime(objDt))

        ########################################################################

    def adjustKey(self, strPassword):
        """
        Alters/modifies the key/password to 16 bit by using padding of space.

        Note :- It's assumed that file have been encrypted using AES Cipher and
        128 bit key is used.
        """
        return "".join([" " if iIdx >= len(strPassword) else strPassword[iIdx] for iIdx in range(16)])

        ########################################################################

    def decryptFile(self, strEncryptedContents, strPassword):
        """
        Descrypts file usng AES cipher.

        Note :- It's assumed that file have been encrypted using AES Cipher and
        128 bit key is used.
        """
        strModifiedPassword = self.adjustKey(strPassword)
        objAES = Crypto.Cipher.AES.new(strModifiedPassword)
        strUnencryptedText = objAES.decrypt(strEncryptedContents)

        return strUnencryptedText

        ########################################################################

    def uncompress(self, strCompressedContents):
        """
        Uncompresses the string, passed as argument

        Note :- It's assumed that file have been compressed using GZip compressing
                algorithm.
        """
        return  zlib.decompress(strCompressedContents)

        ########################################################################

    def isRecurringURI(self, strURI):
        """
        Method, which implements logic for determining, if URI is a recurring URI
        Note :- This method assumes that URIs are accessible usng GET HTTP verb.
        """
        bIsRecurringURI = False
        try:
            objResp = requests.get(strURI)
            if objResp.status_code == 200 and objResp.text:
                bIsRecurringURI = True
        except Exception as e:
            traceback.format_exc()

        return bIsRecurringURI

        ########################################################################

    def findRecurringURI(self, lsStrURIs):
        """
        This method iterates over each URI, to find which URI is recurring URI
        """
        strRecurringURI = ""
        lsRecurringURIs = []
        for strURI in lsStrURIs:
            if self.isRecurringURI(strURI):
                lsRecurringURIs.append(strURI)

        return lsRecurringURIs

        ########################################################################

    def run(self):
        """
        This is the heart of service, which periodically, checks if new
        URI set have been published, and if yes, then decompresses and decrypts
        URI set to find recurring URIs.
        """
        while True:
            try:
                if self.checkForUpdate():
                    print "*********** Detected new URISet **************"
                    lsDirInSharedLoc = os.listdir(self.strSharedLoc)
                    strCurDir = lsDirInSharedLoc[0]

                    iUnixEpochTime = self.getUnixEpochFromTimestamp(strCurDir)
                    strRecentPasswd = str(iUnixEpochTime)
                    strCurDirAbsPath = os.path.join(self.strSharedLoc, strCurDir)
                    lsStrFileName = os.listdir(strCurDirAbsPath)
                    strURIFile = lsStrFileName[0]

                    strFileContents = ""
                    with open(os.path.join(strCurDirAbsPath, strURIFile), "r") as fin:
                        strFileContents = fin.read()

                    if strFileContents:
                        strUncompressFileContents = self.uncompress(strFileContents)
                        strDecryptedFileContents = self.decryptFile(strUncompressFileContents, strRecentPasswd)

                        lsStrURIs = strDecryptedFileContents.replace(" ", "").splitlines()
                        lsRecurringURIs = self.findRecurringURI(lsStrURIs)

                        print "Following is the list of recurring URI's {}".format("".join(lsRecurringURIs))
                    else:
                        print "Found empty file."
                else:
                    print "No new folder found"
            except Exception as e:
                import traceback
                traceback.print_exc()
            finally:
                time.sleep(self.iPollingIntervalInSeconds)

        ########################################################################


if __name__ == '__main__':
    objRecurringSvc = RecurringURISvc("E:/temp/others")
    objRecurringSvc.run()
