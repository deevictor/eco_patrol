# coding: utf-8
from django.conf.urls import url
from django.contrib.auth.views import logout
from django.contrib.auth.views import password_reset


from . import views

app_name = 'user'

urlpatterns = (
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^password_reset/$', password_reset, name='password_reset'),
    url(r'^logout/$', logout, name='logout')
)
