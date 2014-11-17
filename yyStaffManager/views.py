from PIL import Image
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction
from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PaginationSerializer
from rest_framework.response import Response

from YoYoProject.customSettings import USER_SESSION_KEY
from yoyoUtil import yoyoUtil
from yyImgManager.models import YYAlbumInfo, YYImageInfo, YYAlbum2Image
from yyStaffManager.models import YYStaffInfo, YYPostInfo
from yyStaffManager.serializers import YYPaginatedStaffInfoSerializer
from yyUserCenter.auth import yyGetUserFromRequest, yyGetUserByID


class PostStaffForm(forms.Form):
    dealType = forms.IntegerField(max_value=10,required=True)
    staffDesc = forms.CharField(max_length=300,required=True)
    price = forms.FloatField(required=False)
    position = forms.CharField(max_length=100)
    longitude = forms.FloatField(required=False)
    latitude = forms.FloatField(required=False)
    postDesc = forms.CharField(max_length=300, required=False)
    
    
class ViewUserStaffForm(forms.Form):
    userID = forms.CharField(max_length=20, required=True)
    pageIndex = forms.IntegerField(min_value=1, max_value=200,required=True)
    pageCount = forms.IntegerField(min_value=20, max_value=100,required=True)
    
def handleUploadFiles(request):
    
    album = None
    
    try:
        fileCount = 0
        imgList = []
        for afile in request.FILES.getlist('images'):
            fileCount=fileCount+1
            
            img = YYImageInfo()
            img.imgURL = afile
            print(img.imgURL.width)
            img.width = img.imgURL.width
            img.height = img.imgURL.height
            img.save()
            
            imgList.append(img)
        
        if fileCount>0:   
            album = YYAlbumInfo()
            #album.title = "UPLOAD_IMGS_" + yoyoUtil.generateFileName(request.session[USER_SESSION_KEY])
            album.title = "UPLOAD_IMGS_"
            album.description = "-"
            album.save()
            
        imgCount = 0
        for img in imgList:
            album2Img = YYAlbum2Image()
            album2Img.albumInfo = album
            album2Img.ImageInfo = img
            
            album2Img.isPrimary = (imgCount == 0)
            
            imgCount = imgCount + 1
            album2Img.save()
    except:
        return None
    if album == None:
        return None
    else:
         return album

# Create your views here.
@api_view(['POST'])
def postStaff(request):
    
    
    user =  yyGetUserFromRequest(request)
    if user == None:
        return HttpResponse(status.HTTP_401_UNAUTHORIZED)
    
    postStaffForm = PostStaffForm(request.POST)
    
    
    if postStaffForm.is_valid():
        albumInfo = handleUploadFiles(request)
        if albumInfo == None:
            return HttpResponse("Failed to upload images",status=status.HTTP_400_BAD_REQUEST)   
        else:
            #after save the image, then create a new staff and reference post info
            with transaction.commit_on_success():
                
                staffInfo = YYStaffInfo()
                
                
                staffInfo.staffDesc = postStaffForm.cleaned_data['staffDesc']
                price = postStaffForm.cleaned_data['price']
                if price:
                    staffInfo.price = price
                latitude = postStaffForm.cleaned_data['latitude']
                if latitude:
                    staffInfo.latitude = latitude
                    
                longitude = postStaffForm.cleaned_data['longitude']
                if longitude:
                    staffInfo.longitude = longitude
                
                staffInfo.position = postStaffForm.cleaned_data['position']
                staffInfo.dealType = postStaffForm.cleaned_data['dealType']
                staffInfo.albumInfo = albumInfo
                staffInfo.publisher = user
                staffInfo.save()
                
                postInfo = YYPostInfo()
                postInfo.postStaff = staffInfo
                postInfo.postUser = user
                postInfo.description = postStaffForm.cleaned_data['postDesc']
                
                postInfo.save()
                
                        
            return HttpResponse("POST successfully",status=status.HTTP_200_OK)
        
    else:
        return HttpResponse("Format Error",status=status.HTTP_400_BAD_REQUEST)
    
    return HttpResponse(status=status.HTTP_200_OK)


@api_view(['GET'])
def viewStaff(request):
    user =  yyGetUserFromRequest(request)
    if user == None:
        return HttpResponse(status.HTTP_401_UNAUTHORIZED)
    
    viewUserStaffForms = ViewUserStaffForm(request.GET)
    if viewUserStaffForms.is_valid():
        userID = viewUserStaffForms.cleaned_data['userID']
        
        user = yyGetUserByID(int(userID))
        if user==None:
            return HttpResponse("User can't be found", status=status.HTTP_404_NOT_FOUND)
        
        
        pageCount = viewUserStaffForms.cleaned_data['pageCount']
        pageIndex = viewUserStaffForms.cleaned_data['pageIndex']
        
        allStaffList = YYStaffInfo.objects.filter(publisher__pk = user.pk)
        
        paginator = Paginator(allStaffList, pageCount)
        
        try:
            staffList = paginator.page(pageIndex)
            paginateObj = YYPaginatedStaffInfoSerializer(instance=staffList)
            return Response(paginateObj.data,status=status.HTTP_200_OK)
        except EmptyPage:
            return HttpResponse("No Content",status=status.HTTP_204_NO_CONTENT)
        
    else:
        return HttpResponse("Format Error",status=status.HTTP_400_BAD_REQUEST)
    
    
    
    