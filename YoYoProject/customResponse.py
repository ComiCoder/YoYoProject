from rest_framework.response import Response
from rest_framework import status

from yoyoUtil  import yyResponseUtil

class SuccessResponse(Response):
     def __init__(self, path='', errorID=yyResponseUtil.ERR_SVC_20000_USER_NOT_LOGON):
        Response.__init__(self, yyResponseUtil.generateRsp(path, errorID), status=status.HTTP_400_BAD_REQUEST)

class ErrorResponse(Response):
    def __init__(self, path='', errorID=yyResponseUtil.ERR_SVC_20000_USER_NOT_LOGON):
        Response.__init__(self, yyResponseUtil.generateRsp(path, errorID), status=status.HTTP_400_BAD_REQUEST)