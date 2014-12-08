from django import forms
from django.shortcuts import render

from YoYoProject.errorResponse import ErrorResponse
from yoyoUtil import yyErrorUtil
from yyUserCenter.auth import yyGetUserFromRequest
from yyUserCenter.models import YYAccountInfo
from rest_framework.decorators import api_view
from yyTagManager.models import YYTagInfo
import datetime
from yyTagManager.serializers import YYTagInfoSerializer
from rest_framework.response import Response


class CreateTagForm(forms.Form):
    tagType = forms.IntegerField(required=False)
    tagValue = forms.CharField(max_length=50, required=True)
    status = forms.IntegerField(required=False)
    
    overTime = forms.IntegerField(min_value=0, max_value=300, required=False)
    

# Create your views here.
@api_view(['POST'])
def createTag(request):
    user =  yyGetUserFromRequest(request)
    if user == None:
        return ErrorResponse(request.path, yyErrorUtil.ERR_SVC_20000_USER_NOT_LOGON)
    
    if user.type != YYAccountInfo.USER_TYPE_ADMIN:
        return ErrorResponse(request.path, yyErrorUtil.ERR_SVC_20016_NOT_ADMIN)
    
    form = CreateTagForm(request.POST)
    if form.is_valid():
        tagType = form.cleaned_data['tagType']
        tagValue = form.cleaned_data['tagValue']
        status = form.cleaned_data['status']
        
        tagInfo = YYTagInfo()
        if tagType:
            tagInfo.tagType = tagType
            
        tagInfo.tagValue = tagValue
        if status:
            tagInfo.status = status
        if tagType == YYTagInfo.TAG_TYPE_OVERTIME:
            overTime = form.cleaned_data['overTime']
            overTime = int(overTime)
            
            
            if overTime > 0:
                nowTime = datetime.datetime.now()
                overTime = nowTime + datetime.timedelta(days=overTime)
        
        tagInfo.save()
        
        tagInfoSerializer = YYTagInfoSerializer(tagInfo)
        return Response(tagInfoSerializer.data, status=status.HTTP_200_OK)
    else:
        return ErrorResponse(request.path,yyErrorUtil.ERR_SVC_20006_FORMAT_ERROR)    
            
            
            
    