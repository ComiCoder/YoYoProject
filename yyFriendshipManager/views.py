from django import forms
from django.http.response import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from yyFriendshipManager import friendshipSvc
from yyFriendshipManager.models import YYFriendShipInfo
from yyFriendshipManager.serializers import YYFriendshipInfoSerializer
from yyUserCenter.auth import yyGetUserFromRequest, yyGetUserByID
from yoyoUtil import yyErrorUtil
from YoYoProject.errorResponse import ErrorResponse


# Create your views here.
class CreateFriendshipForm(forms.Form):
    userID = forms.CharField(max_length=20,required=True)
    


@api_view(['POST'])
def create(request):
    fromUser =  yyGetUserFromRequest(request)
    
    if fromUser == None:
        return ErrorResponse(request.path, yyErrorUtil.ERR_SVC_20000)
    
    
    createFriendshipForm = CreateFriendshipForm(request.POST)
    
    if createFriendshipForm.is_valid():
        
        fromUserID = fromUser.pk
        toUserID = createFriendshipForm.cleaned_data['userID']
        
        if fromUserID == toUserID:
            return ErrorResponse(request.path, yyErrorUtil.ERR_SVC_20004)
            
        
        toUser = yyGetUserByID(int(toUserID))
        
        if toUser==None:
            return ErrorResponse(request.path, yyErrorUtil.ERR_SVC_20003)
        
        if friendshipSvc.isFocusAlready(fromUserID, toUserID):
            return ErrorResponse(request.path, yyErrorUtil.ERR_SVC_20005)
        
        
        
        friendShipInfo = YYFriendShipInfo()
        friendShipInfo.fromUser = fromUser
        friendShipInfo.toUser = toUser
        friendShipInfo.save()
        
        serializer = YYFriendshipInfoSerializer(friendShipInfo)
        return Response(serializer.data,status=status.HTTP_200_OK)
        
    else:
        return HttpResponse("format Error",status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def destroy(request):
    return None
    