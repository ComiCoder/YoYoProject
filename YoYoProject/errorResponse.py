from rest_framework.response import Response
from rest_framework import status

from yoyoUtil import yyErrorUtil

class ErrorResponse(Response):
    def __init__(self, path='', errorID=yyErrorUtil.ERR_SVC_20000_USER_NOT_LOGON):
        Response.__init__(self, yyErrorUtil.generateRsp(path, errorID), status=status.HTTP_400_BAD_REQUEST)