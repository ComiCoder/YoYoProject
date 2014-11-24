from django.conf.urls import patterns, include, url
from django.contrib import admin

from yyMongoImgManager import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'YouYongProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^getImg/$', views.getImage, name='getImg'),
    
    
    
    
    #url(r'^logon/$',views.logon),
    #url(r'^logout/$',views.logout),
    #url(r'^update_icon_image/$',views.update_icon_image)
)