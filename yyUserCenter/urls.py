from django.conf.urls import patterns, include, url
from django.contrib import admin

from yyUserCenter import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'YouYongProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^weibo_login/$', views.weibo_login, name='weibo_login'),
    url(r'^weibo_login_callback/$', views.weibo_callback, name='weibo_login_callback'),
    
    url(r'^register/$',views.register, name="register"), 
    url(r'^login/$',views.login, name="login"),
    url(r'^logout/$',views.logout, name='logout'),
    
    url(r'^update/$',views.logout, name='update'),
    url(r'^updateIcon/$',views.updateIcon, name='updateIcon'),
    url(r'^resetPwd/$',views.logout, name='resetPwd'),
    url(r'^bindWithPhone/$',views.bindWithPhone, name='bindWithPhone'),
    
    url(r'^view/$',views.logout, name='view'),
    
    
    
    
    #url(r'^logon/$',views.logon),
    #url(r'^logout/$',views.logout),
    #url(r'^update_icon_image/$',views.update_icon_image)
)

urlpatterns = format_suffix_patterns(urlpatterns)