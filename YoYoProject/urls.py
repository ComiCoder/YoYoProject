from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^userCenter/',include('yyUserCenter.urls')),
    url(r'^staff/',include('yyStaffManager.urls')),
    url(r'^friendship/',include('yyFriendshipManager.urls')),
    url(r'^image/',include('yyMongoImgManager.urls')),
    url(r'^comments/',include('yyCommentCenter.urls')),
    url(r'^tag/',include('yyTagManager.urls')),
    url(r'^cms/',include('yyCRM.urls')),
    
    
    
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
