from PIL import Image
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction
from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from YoYoProject.customSettings import USER_SESSION_KEY
from YoYoProject.errorResponse import ErrorResponse
from yoyoUtil import yoyoUtil
from yyFriendshipManager.models import YYFriendShipInfo
from yyImgManager.models import YYAlbumInfo, YYImageInfo, YYAlbum2Image
from yyStaffManager.models import YYStaffInfo, YYPostInfo
from yyStaffManager.serializers import YYPaginatedPostInfoSerializer,YYPaginatedStaffInfoSerializer,\
    YYPostInfoSerializer, YYStaffInfoSerializer
from yyUserCenter.auth import yyGetUserFromRequest, yyGetUserByID
from yoyoUtil import yyErrorUtil
from yyMongoImgManager import imgService
from yyStaffManager import staffSvc
import logging

logger = logging.getLogger('staffManager.models')

class PostStaffForm(forms.Form):
    dealType = forms.IntegerField(max_value=10,required=True)
    staffDesc = forms.CharField(max_length=300,required=True)
    price = forms.FloatField(required=False)
    position = forms.CharField(max_length=100,required=False)
    longitude = forms.FloatField(required=False)
    latitude = forms.FloatField(required=False)
    postDesc = forms.CharField(max_length=300, required=False)
    
class EditStaffForm(forms.Form):
    staffID = forms.CharField(max_length=20, required=True)
    dealType = forms.IntegerField(max_value=10,required=False)
    staffDesc = forms.CharField(max_length=300,required=False)
    price = forms.FloatField(required=False)
    position = forms.CharField(max_length=100,required=False)
    longitude = forms.FloatField(required=False)
    latitude = forms.FloatField(required=False)
    postDesc = forms.CharField(max_length=300, required=False)
    
    
class ViewStaffListForm(forms.Form):
    userID = forms.CharField(max_length=20, required=True)
    pageIndex = forms.IntegerField(min_value=1, max_value=200,required=True)
    pageCount = forms.IntegerField(min_value=20, max_value=100,required=True)
    
    
class ViewStaffDetailForm(forms.Form):
    staffID = forms.CharField(max_length=20, required=True)

class DelStaffForm(forms.Form):
    staffID = forms.CharField(max_length=20, required=True)
    
class ForwardStaffForm(forms.Form):
    staffID = forms.CharField(max_length=20, required=True)
    postDesc = forms.CharField(max_length=300, required=False)
    
def handleUploadFiles(request):
    
    album = None
    
    try:
        fileCount = 0
        imgList = []
        for afile in request.FILES.getlist('images'):
            fileCount=fileCount+1
            img = YYImageInfo()
            try:
                imgPK =  imgService.uploadImg(afile)
                if imgPK<0:
                    #TODO: raise a exception
                    return None
                img.imgID = imgPK
        
            except:
                #TODO: raise a exception
                return None
            
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
        return ErrorResponse(request.path, yyErrorUtil.ERR_SVC_20000_USER_NOT_LOGON)
    
    postStaffForm = PostStaffForm(request.POST)
    
    
    if postStaffForm.is_valid():
        albumInfo = handleUploadFiles(request)
        if albumInfo == None:
            return ErrorResponse(request.path, yyErrorUtil.ERR_SVC_20010_UPLOAD_ALBUM_EXCEPTION)   
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
def staffList(request):
    user =  yyGetUserFromRequest(request)
    if user == None:
        return ErrorResponse(request.path, yyErrorUtil.ERR_SVC_20000_USER_NOT_LOGON)
    
    viewUserStaffForms = ViewStaffListForm(request.GET)
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

@api_view(['GET'])
def staffDetail(request, format=None): 
    user =  yyGetUserFromRequest(request)
    if user == None:
        return ErrorResponse(request.path, yyErrorUtil.ERR_SVC_20000_USER_NOT_LOGON)
    viewUserStaffForms = ViewStaffDetailForm(request.GET)
    if viewUserStaffForms.is_valid():
        staffID = viewUserStaffForms.cleaned_data['staffID']
        
        staff = staffSvc.getStaffByID(int(staffID))
        if staff==None:
            return ErrorResponse(request.path, yyErrorUtil.ERR_SVC_20011_STAFF_NOT_EXIST)
        
        staffSerializer = YYStaffInfoSerializer(staff)
        return Response(staffSerializer.data, status=status.HTTP_200_OK)
        
    else:
        return ErrorResponse(request.path,yyErrorUtil.ERR_SVC_20006_FORMAT_ERROR)    
    

@api_view(['POST'])
def staffEdit(request):
    user =  yyGetUserFromRequest(request)
    if user == None:
        return ErrorResponse(request.path, yyErrorUtil.ERR_SVC_20000_USER_NOT_LOGON)
    
    editStaffForm = EditStaffForm(request.POST)
    if editStaffForm.is_valid():
        staffID = editStaffForm.cleaned_data['staffID']
        
        staff = staffSvc.getStaffByID(int(staffID))
        if staff==None:
            return ErrorResponse(request.path, yyErrorUtil.ERR_SVC_20011_STAFF_NOT_EXIST)
        
        dealType = editStaffForm.clean_data['dealType']
        
        if dealType:
            dealType = int(dealType)
             
        
        staffDesc = editStaffForm.clean_data['staffDesc']
        price = editStaffForm.clean_data['price']
        
        
        
        if dealType == YYStaffInfo.STAFF_DEAL_TYPE_TRADE and price== None:
            return ErrorResponse(request.path,yyErrorUtil.ERR_SVC_20006_FORMAT_ERROR)
        if price == None:
            price = 0.0
        postDesc = editStaffForm.clean_data['postDesc']
        
        
        if dealType > 0 and staff.dealType != dealType:
            staff.dealType = dealType
        
        if staff.staffDesc != staffDesc:
            staff.staffDesc = staffDesc
        
        if price > 0 and staff.price != staff.price:
            staff.price = price
        
        if price == 0.0:
            staff.price = price
        
        if staff.postDesc!=postDesc:
            staff.postDesc
            
        staff.save()
        staffSerializer = YYStaffInfoSerializer(staff)
        return Response(staffSerializer.data, status=status.HTTP_200_OK)
        
    else:
        return ErrorResponse(request.path,yyErrorUtil.ERR_SVC_20006_FORMAT_ERROR)
   

@api_view(['GET'])
def staffDel(request):
    user =  yyGetUserFromRequest(request)
    if user == None:
        return ErrorResponse(request.path, yyErrorUtil.ERR_SVC_20000_USER_NOT_LOGON)
    viewUserStaffForms = ViewStaffDetailForm(request.GET)
    if viewUserStaffForms.is_valid():
        staffID = viewUserStaffForms.cleaned_data['staffID']
        
        staff = staffSvc.getStaffByID(int(staffID))
        if staff==None:
            return ErrorResponse(request.path, yyErrorUtil.ERR_SVC_20011_STAFF_NOT_EXIST)
        
        if staff.publisher.pk != user.pk:
            return ErrorResponse(request.path,yyErrorUtil.ERR_SVC_20012_NO_AUTHORITY)
        staffSerializer = YYStaffInfoSerializer(staff)
        try:
            
            staff.delete()
        except Exception, e:
            logger.error("Failed to delete Staff, error %s" %e)
            return ErrorResponse(request.path,yyErrorUtil.ERR_SVC_20013_DB_EXCEPTION)
        
        return Response(staffSerializer.data, status=status.HTTP_200_OK)
        
    else:
        return ErrorResponse(request.path,yyErrorUtil.ERR_SVC_20006_FORMAT_ERROR)    

@api_view(['POST'])
def forwardStaff(request):
    user =  yyGetUserFromRequest(request)
    if user == None:
        return ErrorResponse(request.path, yyErrorUtil.ERR_SVC_20000_USER_NOT_LOGON)
    forwardForms = ForwardStaffForm(request)
    if forwardForms.is_valid():
        staffID = forwardForms.cleaned_data['staffID']
        staff = staffSvc.getStaffByID(int(staffID))
        if staff==None:
            return ErrorResponse(request.path, yyErrorUtil.ERR_SVC_20011_STAFF_NOT_EXIST)
        postStaff = YYPostInfo()
        postStaff.postStaff = staff
        postStaff.postUser = user
        
        postDesc = forwardForms.cleaned_data['postDesc']
        
        if postDesc:
            
            postStaff.description = postDesc
            
        postStaff.save()
    else:
        return ErrorResponse(request.path,yyErrorUtil.ERR_SVC_20006_FORMAT_ERROR)    

    