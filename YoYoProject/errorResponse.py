from rest_framework.response import Response
from rest_framework import status

from yoyoUtil import yyErrorUtil

class ErrorResponse(Response):
    def __init__(self, path, errorID):
        Response.__init__(self, yyErrorUtil.generateRsp(path, yyErrorUtil.ERR_SVC_20003), status=status.HTTP_400_BAD_REQUEST)