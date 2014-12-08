from datetime import datetime
import logging

from django  import forms
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from YoYoProject.errorResponse import ErrorResponse
from yoyoUtil import yyErrorUtil
from yyCommentCenter.models import YYCommentInfo
from yyCommentCenter.serializers import YYCommentInfoSerializer,\
    YYPaginatedCommentInfoSerializer
from yyStaffManager import staffSvc
from yyUserCenter.auth import yyGetUserFromRequest, yyGetUserByID
from django.http.response import HttpResponse
from YoYoProject import customSettings
from yyCommentCenter import commentSvc
from django.core.paginator import Paginator, EmptyPage


#     (TARGET_TYPE_STAFF,"staff"),
#     (TARGET_TYPE_DEAL,"deal"),
logger = logging.getLogger()

class CreateCommentForm(forms.Form):
    toUserID = forms.CharField(max_length=20, required=False)
    targetID = forms.CharField(max_length=20, required=True)
    targetType = forms.IntegerField(min_value=1, max_value=2, required=True)
    commentDesc = forms.CharField(max_length=300, required=True)
    
class DeleteCommentForm(forms.Form):
    commentID = forms.CharField(max_length=20, required=True)
    
class ViewCommentForm(forms.Form):
    targetID = forms.CharField(max_length=30, required=True)
    sinceID = forms.IntegerField(required=False)
    maxID = forms.IntegerField(required=False)
    pageIndex = forms.IntegerField(min_value=1, max_value=200,required=True)
    pageCount = forms.IntegerField(min_value=20, max_value=100,required=True)
    
# Create your views here.
@api_view(['POST'])
def createComment(request):
    user =  yyGetUserFromRequest(request)
    if user == None:
        return ErrorResponse(request.path, yyErrorUtil.ERR_SVC_20000_USER_NOT_LOGON)
    
    forms = CreateCommentForm(request.POST)
    if forms.is_valid():
        targetType = forms.cleaned_data['targetType']
        comment = YYCommentInfo()
        if targetType == YYCommentInfo.TARGET_TYPE_STAFF:
            comment.targetType = targetType
        elif targetType == YYCommentInfo.TARGET_TYPE_DEAL:
            comment.targetType = targetType
        
        commentDesc = forms.cleaned_data['commentDesc']
        comment.comment = commentDesc
        
        targetID = long(forms.cleaned_data['targetID'])
        
        if targetType == YYCommentInfo.TARGET_TYPE_STAFF:
            targetStaff = staffSvc.getStaffByID(targetID)
            if targetStaff == None:
                return ErrorResponse(request.path, yyErrorUtil.ERR_SVC_20011_STAFF_NOT_EXIST)
        elif targetType == YYCommentInfo.TARGET_TYPE_DEAL:
            return ErrorResponse()
        
        comment.targetID = targetID
        
        toUserID = forms.cleaned_data['toUserID']
        if toUserID:
            toUser = yyGetUserByID(toUserID)
            if toUser==None:
                return ErrorResponse(request.path, yyErrorUtil.ERR_SVC_20015_TARGET_USER_NOT_EXIST)
            comment.toUserID = long(toUserID)
            
        comment.fromUserID = user.pk
        comment.createTime = datetime.now()
        comment.updateTime = datetime.now()
        
        try:
            
            comment.save()
        except Exception,e:
            logger.error("Failed to save comments",e)
            return ErrorResponse(request.path, yyErrorUtil.ERR_SVC_20013_DB_EXCEPTION)
        
        serializer = YYCommentInfoSerializer(comment)
        return Response(serializer.data,status=status.HTTP_200_OK)
        
    else:
        return ErrorResponse(request.path, yyErrorUtil.ERR_SVC_20006_FORMAT_ERROR)
    return None

@api_view(['POST'])
def deleteComment(request):
    user =  yyGetUserFromRequest(request)
    if user == None:
        return ErrorResponse(request.path, yyErrorUtil.ERR_SVC_20000_USER_NOT_LOGON)
    forms = CreateCommentForm(request.POST)
    if forms.is_valid():
        commentID = long(forms.cleaned_data['commentID'])
       
        comment = commentSvc.getCommentByID(commentID)
        if comment == None:
            return ErrorResponse(request.path, yyErrorUtil.ERR_SVC_20011_STAFF_NOT_EXIST)
        #targetStaff.deleteStatus = customSettings.INFO_DELETE_YES
        #targetStaff.save()
        comment.deleteStatus = customSettings.INFO_DELETE_YES
        comment.save()    
        
        serializer = YYCommentInfoSerializer(comment)
        return Response(serializer.data,status=status.HTTP_200_OK)  
        
    else:
        return ErrorResponse(request.path, yyErrorUtil.ERR_SVC_20006_FORMAT_ERROR)
    
@api_view(['POST'])
def replyComment(request):
    user =  yyGetUserFromRequest(request)
    if user == None:
        return ErrorResponse(request.path, yyErrorUtil.ERR_SVC_20000_USER_NOT_LOGON)
    
    
    
    return None

@api_view(['GET'])
def showComments(request):
    user =  yyGetUserFromRequest(request)
    if user == None:
        return ErrorResponse(request.path, yyErrorUtil.ERR_SVC_20000_USER_NOT_LOGON)
    form = ViewCommentForm(request.GET)
    if form.is_valid():
        pageCount = form.cleaned_data['pageCount']
        pageIndex = form.cleaned_data['pageIndex']
        
        targetID = form.cleaned_data['targetID']
        
        allCommentList = YYCommentInfo.objects(targetID = targetID, deleteStatus = customSettings.INFO_DELETE_NO)
        
        paginator = Paginator(allCommentList, pageCount)
        try:
            staffList = paginator.page(pageIndex)
            paginateObj = YYPaginatedCommentInfoSerializer(instance=staffList)
            return Response(paginateObj.data,status=status.HTTP_200_OK)
        except EmptyPage:
            return HttpResponse("No Content",status=status.HTTP_204_NO_CONTENT)
    else:
        return ErrorResponse(request.path, yyErrorUtil.ERR_SVC_20006_FORMAT_ERROR)


