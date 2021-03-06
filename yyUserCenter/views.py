from django import forms
from django.http.response import HttpResponse, HttpResponseRedirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from weibo import APIClient

from YoYoProject import customSettings
from YoYoProject.customSettings import WEIBO_AUTH_TOKEN
from YoYoProject.customResponse import ErrorResponse
from yoyoUtil import yyResponseUtil
from yyMongoImgManager import imgService
from yyMongoImgManager.models import YYImgInfo
from yyUserCenter.auth import yyLogin, yyAuthenticateByID, \
    yyGetUserByPhone, yyIsPasswordEquas, yyIsWrongUser, yyHasLogin, \
    yySessionHasKey, yyGetUserByID, yyGetUserFromRequest
from yyUserCenter.models import YYAccountInfo
from yyUserCenter.serializers import YYUserInfoSerializer
import logging
from virtualenv import REQUIRED_FILES


APP_KEY = '3920803036' # app key  
APP_SECRET = 'c9bc705bf2bbf8335d3b6f6157f49f15' # app secret  
RYU_CLIENT_ID = '3920803036'
  
  
MY_APP_SECRET = APP_SECRET  
REDIRECT_URL = 'http://127.0.0.1:8000/userCenter/weibo_login_callback/'

client = APIClient(APP_KEY, APP_SECRET, REDIRECT_URL)

logger = logging.getLogger('yyUserCenter.views')


class BindUserWithPhoneForm(forms.Form):
    phoneNum = forms.CharField(max_length=20,required=True)
    
class AuthUserForm(forms.Form):
    type = forms.IntegerField(min_value=customSettings.USER_CERTIFICATION_TYPE_IDENTITY, 
                              max_value=customSettings.USER_CERTIFICATION_TYPE_WECHAT, 
                              required=True)
    userID = forms.IntegerField(required=True)
    otherID = forms.CharField(max_length=30, required=False) #OTHER SNS ID, such as weibo or wechat
    

def lookUserBySinaID(sinaID):
    authWeiboID = customSettings.WEIBO_ID_PREFIX + sinaID
    
    if not YYAccountInfo.objects.filter(authWeiboID=authWeiboID).exists():
        accountInfo = YYAccountInfo()
         
        accountInfo.authWeiboID  = authWeiboID
        accountInfo.save()
        return accountInfo
    
    return YYAccountInfo.objects.get(authWebboID=authWeiboID)
        

def weibo_login(request):
    
    url = client.get_authorize_url(redirect_uri = REDIRECT_URL)
    return HttpResponseRedirect(url)

def weibo_callback(request):
    
    code = request.GET['code']
    
    weiboToken = client.request_access_token(code, redirect_uri=REDIRECT_URL)
    user = lookUserBySinaID(weiboToken.uid)
    if user:
        user = yyAuthenticateByID(user.pk)
        
        if yyLogin(request,user) == True:
     
            request.session[WEIBO_AUTH_TOKEN] = weiboToken
            userInfoSerializer = YYUserInfoSerializer(user)
            return Response(userInfoSerializer.data,status=status.HTTP_200_OK)
            
    return HttpResponse("Failed to Logon",status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def login(request):
    #first check if the user has been logged already
    if not request.POST.get('phoneNum'):
        return HttpResponse("No PhoneNum",status=status.HTTP_400_BAD_REQUEST)
    
    if not request.POST.get('password'):
        return HttpResponse("No password",status=status.HTTP_400_BAD_REQUEST)
    
    phoneNum = request.POST.get('phoneNum')
    password = request.POST.get('password')
    
    user = yyGetUserByPhone(phoneNum)
    if user == None:
        return HttpResponse("No This User",status=status.HTTP_401_UNAUTHORIZED)
    
    if yyIsWrongUser(request, user):
        return HttpResponse("Another User has Logged on in this session",status=status.HTTP_401_UNAUTHORIZED)
    
    if yyHasLogin(request, user):
        return HttpResponse("This user had logged on already",status=status.HTTP_100_CONTINUE)
    
    
    if yyIsPasswordEquas(user, password) == True:
        yyLogin(request, user)
        userInfoSerializer = YYUserInfoSerializer(user)
        return Response(userInfoSerializer.data,status=status.HTTP_200_OK)
        
    else:
        return HttpResponse("Password Error",status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['GET'])      
def logout(request):
    sessionUserID = request.session.get(customSettings.USER_SESSION_KEY)
    
    if sessionUserID == None:
        return HttpResponse(content='Not Logon', status=status.HTTP_401_UNAUTHORIZED)
    
    tempUserInfo= yyGetUserByID(sessionUserID)
    if tempUserInfo==None:
        return HttpResponse(content='User not found', status=status.HTTP_401_UNAUTHORIZED)
    request.session.pop('user_id')
    return HttpResponse(status=status.HTTP_200_OK)

@api_view(['POST'])       
def register(request, format=None):  
    #first check if the user has been logged already
    if not request.POST.get('phoneNum'):
        return HttpResponse("No PhoneNum",status=status.HTTP_400_BAD_REQUEST)
    
    if not request.POST.get('password'):
        return HttpResponse("No password",status=status.HTTP_400_BAD_REQUEST)
    
    phoneNum = request.POST.get('phoneNum')
    password = request.POST.get('password')
    
    userInfoSet = queryUserByPhone(phoneNum)
    if userInfoSet == None:
        userInfo = YYAccountInfo()
        userInfo.phoneNum = phoneNum
        userInfo.password = password
        userInfo.save()
        
        userInfoSerializer = YYUserInfoSerializer(userInfo)
        return Response(userInfoSerializer.data,status=status.HTTP_201_CREATED)
    else:
        return Response("error",status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def updateIcon(request):
    fromUser =  yyGetUserFromRequest(request)
    
    if fromUser == None:
        return ErrorResponse(request.path, yyResponseUtil.ERR_SVC_20000_USER_NOT_LOGON)
    
    if request.FILES['userIcons'] ==None:
        return HttpResponse(content="no image upload", status=status.HTTP_400_BAD_REQUEST)
    
    
    #upload the image to mongodb
    try:
        imgPK =  imgService.uploadImg(request.FILES['userIcons'])
        if imgPK<0:
            return ErrorResponse(request.path,yyResponseUtil.ERR_SVC_20008_UPLOAD_EMPTY_IMG)
        fromUser.iconID = imgPK
        
    except:
        return ErrorResponse(request.path, yyResponseUtil.ERR_SVC_20009_UPLOAD_EXCEPTION)
    
    fromUser.save()
    
    userInfoSerializer = YYUserInfoSerializer(fromUser)
    return Response(userInfoSerializer.data,status=status.HTTP_200_OK)

@api_view(['POST'])
def bindWithPhone(request):
    user =  yyGetUserFromRequest(request)
    
    if user == None:
        return ErrorResponse(request.path, yyResponseUtil.ERR_SVC_20000_USER_NOT_LOGON)
    
    if user.phoneNum != None:
        return ErrorResponse(request.path, yyResponseUtil.ERR_SVC_20014_ALREADY_BIND_PHONE)
    
    form = BindUserWithPhoneForm(request)
    
    if form.is_valid():
        phoneNum = form.cleaned_data['phoneNum']
        user.phoneNum = phoneNum
        try:
            user.save()
        except:
            logger.error("Failed to update userinfo")
            return ErrorResponse(request.path, yyResponseUtil.ERR_SVC_20013_DB_EXCEPTION)
        
    else:
        return ErrorResponse(request.path, yyResponseUtil.ERR_SVC_20006_FORMAT_ERROR)
        
    #return None
@api_view(['POST'])
def userAuth(request):
    user =  yyGetUserFromRequest(request)
    if user == None:
        return ErrorResponse(request.path, yyResponseUtil.ERR_SVC_20000_USER_NOT_LOGON)
    
    
    pass
  
def queryUserByPhone(phoneNum):
    userInfoSet = YYAccountInfo.objects.filter(phoneNum=phoneNum)
    if userInfoSet == None or userInfoSet.count() == 0:
        return None
    else:
        return userInfoSet[0]  




    