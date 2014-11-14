from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status

from django import forms
from django.http.response import HttpResponse
from yyImgManager.models import YYAlbumInfo, YYImageInfo, YYAlbum2Image
from yoyoUtil import yoyoUtil
from YoYoProject.customSettings import USER_SESSION_KEY
from PIL import Image

    
class PostStaffForm(forms.Form):
    dealType = forms.IntegerField(max_value=10,required=True)
    staffDesc = forms.CharField(max_length=300,required=True)
    price = forms.FloatField(required=False)
    position = forms.CharField(max_length=100)
    longitude = forms.FloatField(required=False)
    latitude = forms.FloatField(required=False)
    postDesc = forms.CharField(max_length=300, required=False)
    
    
def handleUploadFiles(request):
    
    
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
        return False
    
    return True

# Create your views here.
@api_view(['POST'])
def postStaff(request):
    
    postStaffForm = PostStaffForm(request.POST)
    
    if postStaffForm.is_valid():
        if handleUploadFiles(request):
            return HttpResponse(status=status.HTTP_200_OK)
        else:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    else:
        return HttpResponse("Format Error",status=status.HTTP_400_BAD_REQUEST)
    
    return HttpResponse(status=status.HTTP_200_OK)