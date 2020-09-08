#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: manage.py
@time: 2020/9/8 11:36
@desc:
'''
from django.shortcuts import render


def dashboard(request, project_id):
	return render(request, 'dashboard.html')


def issues(request, project_id):
	return render(request, 'issues.html')


def statistics(request, project_id):
	return render(request, 'statistics.html')


def file(request, project_id):
	return render(request, 'file.html')




def setting(request, project_id):
	return render(request, 'setting.html')
