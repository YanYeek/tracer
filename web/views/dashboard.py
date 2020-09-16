#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: dashboard.py
@time: 2020/9/16 17:17
@desc:
'''
from django.shortcuts import render


def dashboard(request):
	return render(request, 'dashboard.html')
