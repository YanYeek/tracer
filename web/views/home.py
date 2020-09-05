#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: home.py
@time: 2020/9/5 21:29
@desc:
'''
from django.shortcuts import render


def index(request):
	return render(request, 'index.html')
