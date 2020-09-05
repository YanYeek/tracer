#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: urls.py
@time: 2020/9/4 13:22
@desc:
'''
from django.conf.urls import url
from web.views import account
from web.views import home

urlpatterns = [
	url(r'^register/$', account.register, name='register'),
	url(r'^login/sms/$', account.login_sms, name='login_sms'),
	url(r'^login/$', account.login, name='login'),
	url(r'^logout/$', account.logout, name='logout'),
	url(r'^image/code/$', account.image_code, name='image_code'),

	url(r'^send/sms/$', account.send_sms, name='send_sms'),


	url(r'^index/$', home.index, name='index'),
]
