# coding: utf-8
from django.conf.urls import url

from . import views

app_name = 'label'

urlpatterns = (
    url(r'^ajax_form/$', views.ajax_form, name='ajax_form'),
    url(r'^ajax_comment/$', views.ajax_comment, name='ajax_comment'),
    url(r'^labels_json/$', views.labels_json, name='labels_json')
)
