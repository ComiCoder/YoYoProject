from django.shortcuts import render

from weibo import APIClient
from rest_framework import status
from django.http.response import HttpResponse, HttpResponseRedirect
from YoYoProject import customSettings
from yyUserCenter.models import YYAccountInfo
from django.contrib.auth import authenticate
from YoYoProject.customSettings import WEIBO_AUTH_TOKEN
from yyUserCenter.auth import login

APP_KEY = '3920803036' # app key  
APP_SECRET = 'c9bc705bf2bbf8335d3b6f6157f49f15' # app secret  
RYU_CLIENT_ID = '3920803036'
  
  
MY_APP_SECRET = APP_SECRET  
REDIRECT_URL = 'http://127.0.0.1:8000/userCenter/weibo_login_callback/'

client = APIClient(APP_KEY, APP_SECRET, REDIRECT_URL)

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
    
    #test 
    #code = RYU_CLIENT_ID
    
    
    weiboToken = client.request_access_token(code, redirect_uri=REDIRECT_URL)
    user = lookUserBySinaID(weiboToken.uid)
    if user:
        user = authenticate(user.pk)
        
        if login(request,user) == True:
     
            request.session[WEIBO_AUTH_TOKEN] = weiboToken
            
    return HttpResponse("Failed to Logon",status=status.HTTP_401_UNAUTHORIZED)




'''
def weibo_login(request):
    
    api = APIClient(APP_KEY, MY_APP_SECRET, redirect_uri=REDIRECT_URL)  
    client_id = 0
    try:
        
        authorize_url = api.get_authorize_url()
        
        print(authorize_url)
        
        client_id_idx = authorize_url.index("client_id=")
        #get the client id
        client_id = authorize_url[client_id_idx:]
    except:
        return HttpResponse("Failed to get client_id", status=status.HTTP_400_BAD_REQUEST)
    
    if client_id != 0:
        
    return HttpResponse(status=status.HTTP_200_OK)
    
    '''
    