from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from yyStaffManager import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'YouYongProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^postStaff/$', views.postStaff, name='postStaff'),
    url(r'^staffList/$', views.staffList, name='staffList'),
    url(r'^staffDetail/$', views.staffDetail, name='staffDetail'),
    url(r'^staffEdit/$', views.staffEdit, name='staffEdit'),
    url(r'^staffDel/$', views.staffDel, name='staffDel'),
    
    #url(r'^postTimeLine/$',views.postTimeLine, name='postTimeLine'),
    
    
    
    
    #url(r'^logon/$',views.logon),
    #url(r'^logout/$',views.logout),
    #url(r'^update_icon_image/$',views.update_icon_image)
)

urlpatterns = format_suffix_patterns(urlpatterns)