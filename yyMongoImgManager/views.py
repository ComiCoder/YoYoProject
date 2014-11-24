from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from yyMongoImgManager.models import YYImgInfo
from django.http.response import HttpResponse


# Create your views here.
def getImage(request):
    
    imgID = request.GET.get('imageID')
    
    try:
        imageInfo = YYImgInfo.objects.get(pk=imgID)
        return HttpResponse(imageInfo.img.read(),content_type='image/jpeg')
    except:
        raise
    