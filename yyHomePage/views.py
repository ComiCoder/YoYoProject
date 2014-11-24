from PIL import Image
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction
from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from yyFriendshipManager.models import YYFriendShipInfo
from yyImgManager.models import YYAlbumInfo, YYImageInfo, YYAlbum2Image
from yyMongoImgManager import imgService
from yyStaffManager.models import YYStaffInfo, YYPostInfo
from yyStaffManager.serializers import YYPaginatedPostInfoSerializer, YYPaginatedStaffInfoSerializer, \
    YYPostInfoSerializer
from yyUserCenter.auth import yyGetUserFromRequest, yyGetUserByID

class PostTimeLineForm(forms.Form):
    sincePostID = forms.CharField(max_length=20,required=False)
    maxPostID = forms.CharField(max_length=20,required=False)
    pageIndex = forms.IntegerField(min_value=1, max_value=200,required=True)
    pageCount = forms.IntegerField(min_value=20, max_value=100,required=True)
    
# Create your views here.
@api_view(['GET'])   
def postTimeLine(request):
    user =  yyGetUserFromRequest(request)
    if user == None:
        return HttpResponse(status.HTTP_401_UNAUTHORIZED)
    
    postTimeLineForm = PostTimeLineForm(request.GET)
    
    if postTimeLineForm.is_valid():
        sincePostID = postTimeLineForm.cleaned_data['sincePostID']
        if sincePostID == None:
            sincePostID = 0
        
        sincePostID = int(sincePostID)
        
        maxPostID = postTimeLineForm.cleaned_data['maxPostID']
        if maxPostID == None:
            maxPostID = 0
            
        pageCount = postTimeLineForm.cleaned_data['pageCount']
        pageIndex = postTimeLineForm.cleaned_data['pageIndex']
        
        if pageIndex < 1:
            pageIndex = 1
        
        
        if sincePostID > 0:
            
            try:
                #allPostInfoList  = YYFriendShipInfo.objects.filter(fromUser__pk=user.pk).select_related('toUser').prefetch_related('yy_post_info').get(pk__gt=sincePostID)
                findPostInfoList = '''select post.*
                 from yy_post_info post,yy_friendship_info friend 
                 where (post.id > %d) and ((post.postUser_id = friend.toUser_id and friend.fromUser_id = %d) or (post.postUser_id = %d))
                 ''' % (sincePostID, user.pk, user.pk)

                allPostInfoList = YYFriendShipInfo.objects.raw(findPostInfoList)
                paginator = Paginator(list(allPostInfoList), pageCount)
                
                try:
                    postList = paginator.page(pageIndex)
                    
                    paginateObj = YYPaginatedPostInfoSerializer(instance=postList)
                    return Response(paginateObj.data,status=status.HTTP_200_OK)
        
                    #paginateObj = YYPostInfoSerializer(allPostInfoList, many=True)
                    #return Response(paginateObj.data,status=status.HTTP_200_OK)
                except EmptyPage:
                    return HttpResponse("No Content",status=status.HTTP_204_NO_CONTENT)
                except Exception,e:
                    print e
                    return HttpResponse("Error",status=status.HTTP_200_OK)
            except Exception,e:
                print e
                return HttpResponse("Error",status=status.HTTP_200_OK)
            
            if allPostInfoList==None:
                return HttpResponse("No Result",status=status.HTTP_200_OK)