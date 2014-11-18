from django.conf.urls import patterns, include, url
from django.contrib import admin

from yyFriendshipManager import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'YouYongProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^create/$', views.create, name='create'),
    url(r'^destroy/$', views.destroy, name='destroy'),
)