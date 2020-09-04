#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: urls.py
@time: 2020/9/4 13:21
@desc:
'''
from django.conf.urls import url
from app01 import views

urlpatterns = [
	url(r'^send/sms/', views.send_sms),
	url(r'^register', views.register),
]
