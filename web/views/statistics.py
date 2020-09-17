#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: statistics.py
@time: 2020/9/8 11:36
@desc:
'''
from django.shortcuts import render






def statistics(request, project_id):
	""" 统计页面 """

	return render(request, 'statistics.html')
