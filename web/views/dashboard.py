#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: dashboard.py
@time: 2020/9/16 17:17
@desc:
'''
import collections
from django.shortcuts import render
from django.db.models import Count

from web import models


def dashboard(request, project_id):
	""" 概览 """

	# 问题数据处理
	status_dict = collections.OrderedDict() # python3.6前默认字典无序
	for key, text in models.Issues.status_choices:
		status_dict[key] = {'text': text, 'count': 0}
	issues_data = models.Issues.objects.filter(project_id=project_id).values('status').annotate(ct=Count('id'))
	for item in issues_data:
		status_dict[item['status']]['count'] = item['ct']
	context = {
		'status_dict': status_dict
	}
	return render(request, 'dashboard.html', context)
