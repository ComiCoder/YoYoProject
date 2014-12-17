'''

'''



class yyError(Exception):
    ERROR_ID_PARAMETER_EMPTY = 1
    def __init__(self, errorID=0, errorDesc=""):
        self.errorID = errorID
        self.errorDesc = errorDesc
    def __str__(self, *args, **kwargs):
        formatError = "ErrorID: %d ErrorDesc: %s" %(self.errorID, self.errorDesc)
        return formatError