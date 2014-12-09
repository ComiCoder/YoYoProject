from django import forms
from django.shortcuts import render

from YoYoProject.customResponse import ErrorResponse
from yoyoUtil import yyResponseUtil
from yyUserCenter.auth import yyGetUserFromRequest
from yyUserCenter.models import YYAccountInfo
from rest_framework.decorators import api_view
from yyTagManager.models import YYTagInfo
import datetime
from yyTagManager.serializers import YYTagInfoSerializer,\
    YYPaginatedTagInfoSerializer
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage
from rest_framework import status
from django.http.response import HttpResponse
from django.core.cache import cache


class CreateTagForm(forms.Form):
    tagType = forms.IntegerField(required=False)
    tagValue = forms.CharField(max_length=50, required=True)
    status = forms.IntegerField(required=False)
    overTime = forms.IntegerField(min_value=0, max_value=300, required=False)
    
class ViewTagListForm(forms.Form):
    pageIndex = forms.IntegerField(min_value=1, max_value=200,required=True)
    pageCount = forms.IntegerField(min_value=20, max_value=100,required=True)
    
class EditTagForm(forms.Form):
    tagID = forms.IntegerField(required=True)
    tagType = forms.IntegerField(required=False)
    tagValue = forms.CharField(max_length=50, required=False)
    status = forms.IntegerField(required=False)
    overTime = forms.IntegerField(min_value=0, max_value=300, required=False)
    

# Create your views here.
@api_view(['POST'])
def createTag(request):
    user =  yyGetUserFromRequest(request)
    if user == None:
        return ErrorResponse(request.path, yyResponseUtil.ERR_SVC_20000_USER_NOT_LOGON)
    
    if user.type != YYAccountInfo.USER_TYPE_ADMIN:
        return ErrorResponse(request.path, yyResponseUtil.ERR_SVC_20016_NOT_ADMIN)
    
    form = CreateTagForm(request.POST)
    if form.is_valid():
        tagType = form.cleaned_data['tagType']
        tagValue = form.cleaned_data['tagValue']
        tagStatus = form.cleaned_data['status']
        
        tagInfo = YYTagInfo()
        if tagType:
            tagInfo.tagType = tagType
            
        tagInfo.tagValue = tagValue
        if tagStatus:
            tagInfo.status = tagStatus
        if tagType == YYTagInfo.TAG_TYPE_OVERTIME:
            overTime = form.cleaned_data['overTime']
            overTime = int(overTime)
            
            
            if overTime > 0:
                nowTime = datetime.datetime.now()
                overTime = nowTime + datetime.timedelta(days=overTime)
                tagInfo.validTime = overTime
            else:
                #the default overtime is 30 days
                overTime = nowTime + datetime.timedelta(30)
                tagInfo.validTime = overTime
        
        tagInfo.save()
        
        tagInfoSerializer = YYTagInfoSerializer(tagInfo)
        return Response(tagInfoSerializer.data, status=status.HTTP_200_OK)
    else:
        return ErrorResponse(request.path,yyResponseUtil.ERR_SVC_20006_FORMAT_ERROR)    
            
@api_view(['GET'])
def viewTagList(request):
    user =  yyGetUserFromRequest(request)
    if user == None:
        return ErrorResponse(request.path, yyResponseUtil.ERR_SVC_20000_USER_NOT_LOGON)
    
    forms = ViewTagListForm(request.GET)
    if forms.is_valid():
        pageCount = forms.cleaned_data['pageCount']
        pageIndex = forms.cleaned_data['pageIndex']
        
        allStaffList = YYTagInfo.objects.all()
        paginator = Paginator(allStaffList, pageCount)
        
        try:
            staffList = paginator.page(pageIndex)
            paginateObj = YYPaginatedTagInfoSerializer(instance=staffList)
            return Response(paginateObj.data,status=status.HTTP_200_OK)
        except EmptyPage:
            return ErrorResponse(request.path,yyResponseUtil.ERR_SVC_20018_EMPTY_PAGE)
    else:
        return ErrorResponse(request.path,yyResponseUtil.ERR_SVC_20006_FORMAT_ERROR)
    
@api_view(['POST'])
def editTag(request):
    user =  yyGetUserFromRequest(request)
    if user == None:
        return ErrorResponse(request.path, yyResponseUtil.ERR_SVC_20000_USER_NOT_LOGON)
    
    form = ViewTagListForm(request.GET)
    if form.is_valid():
        tagID = forms.cleand_data['tagID']
        tagInfo = YYTagInfo.objects.get(pk=tagID)
        if not tagInfo:
            return ErrorResponse(request.path,yyResponseUtil.ERR_SVC_20017_TAG_NOT_EXIST)
        tagType = form.cleand_data['tagType']
        tagValue = form.cleaned_data['tagValue']
        status = form.cleaned_data['status']
        
        if tagType:
            tagInfo.tagType = tagType
        
        if tagValue:
            tagInfo.tagValue = tagValue
            
        if status:
            tagInfo.status = status
        
        if tagType == YYTagInfo.TAG_TYPE_OVERTIME:
            overTime = form.cleaned_data['overTime']
            overTime = int(overTime)
            
            if overTime > 0:
                overTime = tagInfo.createTime + datetime.timedelta(days=overTime)
                tagInfo.validTime = overTime  
            
        tagInfo.save()
        tagInfoSerializer = YYTagInfoSerializer(tagInfo)
        return Response(tagInfoSerializer.data, status=status.HTTP_200_OK)
        
    else:
        return ErrorResponse(request.path,yyResponseUtil.ERR_SVC_20006_FORMAT_ERROR)   
    
    
@api_view(['POST'])
def refreshToMem(request):
    
    list = ['1','2','3']
    cache.set("list",list,0)
    
    print cache.get('list')
    return ErrorResponse(request.path,yyResponseUtil.ERR_SVC_20006_FORMAT_ERROR)   
            
    