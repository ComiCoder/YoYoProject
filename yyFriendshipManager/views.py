from django import forms
from django.http.response import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view

from yyUserCenter.auth import yyGetUserFromRequest


# Create your views here.
class CreateFriendshipForm(forms.Form):
    userID = forms.CharField(max_length=20,required=True)
    


@api_view(['POST'])
def create(request):
    user =  yyGetUserFromRequest(request)
    if user == None:
        return HttpResponse(status.HTTP_401_UNAUTHORIZED)
    
    createFriendshipForm = CreateFriendshipForm(request.POST)
    
    if createFriendshipForm.is_valid():
        
        #TODO:
        return None
        
    else:
        return HttpResponse("format Error",status=status.HTTP_400_BAD_REQUEST)