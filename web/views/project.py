#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: project.py
@time: 2020/9/7 2:00
@desc:
'''
from django.shortcuts import render


def project_list(request):
	"""项目列表"""
	return render(request, 'project_list.html')
