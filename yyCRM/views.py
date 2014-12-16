from django.shortcuts import render
from django import forms
from yyUserCenter.models import YYAccountInfo
from django.core.paginator import Paginator, EmptyPage
from yyUserCenter.auth import yyGetUserFromRequest
from django.views.decorators.csrf import csrf_exempt

class QueryUserForm(forms.Form):
    userName = forms.CharField(max_length=30,required=False)
    pageIndex = forms.IntegerField(min_value=1, max_value=200,required=False)
    

class ViewUserForm(forms.Form):
    userID = forms.CharField(max_length=20,required=True)

# Create your views here.
def crmIndex(request):
    user =  yyGetUserFromRequest(request)
    #if not user:
    #    return render(request, 'index/login.html')
    return render(request, 'index/index.html')

@csrf_exempt
def cmsViewUser(request):
    form = ViewUserForm(request.GET)
    if form.is_valid():
        userID = form.cleaned_data['userID']
        userID = long(userID)
        user = YYAccountInfo.objects.get(pk = userID)
        if user == None:
            return render(request, 'errMsg/errMsg.html',{'errMsg':"format error!"})
        else:
            return render(request, 'userCMS/viewUser.html',{'user':user})
    else:
       return render(request, 'errMsg/errMsg.html', {'errMsg':"format error!"})

@csrf_exempt
def cmsUserList(request):
    
    
    
    form = QueryUserForm(request.GET)
    if form.is_valid():
        pageCount = 10
        pageIndex = 1
        
        if form.cleaned_data and form.cleaned_data.has_key('pageIndex'):
            pageIndex = form.cleaned_data['pageIndex']
        
        if pageCount == 0:
            pageCount = 20
        if pageIndex <=0:
            pageIndex = 1
        
        allUserList = YYAccountInfo.objects.all()
        
        paginator = Paginator(allUserList, pageCount)
        
        try:
            userListPage = paginator.page(pageIndex)
            return render(request, 'userCMS/userList.html', {'userListPage':userListPage})
        except EmptyPage:
            return render(request, 'userCMS/userList.html')
    else:
        return render(request, 'userCMS/userList.html')
    
    