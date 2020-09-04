#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: account.py
@time: 2020/9/4 12:36
@desc:用户相关功能：注册、短信、登录、注销
'''
from django.shortcuts import render, HttpResponse

def register(requests):
	return render(requests, 'register.html')