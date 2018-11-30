# coding: utf-8
from django.conf.urls import url

from . import views

app_name = 'user'

urlpatterns = (
    url(r'^inspector_request/$', views.inspector_request_async,
        name='inspector_request'),
)
