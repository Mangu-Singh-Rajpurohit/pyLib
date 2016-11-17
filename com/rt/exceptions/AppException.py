#-------------------------------------------------------------------------------
# Name:         AppException.py
# Purpose:      Represents exceptions that can be raised
#               in any python application.
#
# Author:       Mangu Singh Rajpurohit
#
# Created:     07/08/2016
# Copyright:   (c) rtCorporation 2016
# Licence:     all_rights_reserved
#-------------------------------------------------------------------------------

class AppException(Exception):
    iAppErrorCode       = 1
    strExceptionTrack   = "";

    def __init__(self, **kwArgs):
        for strArg, objVal in kwArgs.items():
            setattr(self, strArg, objVal)