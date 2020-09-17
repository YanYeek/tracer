#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: dashboard.py
@time: 2020/9/16 17:17
@desc:
'''
import time
import collections
import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Count
from django.db.models import Count

from web import models


def dashboard(request, project_id):
	""" 概览 """

	# 问题数据处理
	status_dict = collections.OrderedDict()  # python3.6前默认字典无序
	for key, text in models.Issues.status_choices:
		status_dict[key] = {'text': text, 'count': 0}
	issues_data = models.Issues.objects.filter(project_id=project_id).values('status').annotate(ct=Count('id'))
	for item in issues_data:
		status_dict[item['status']]['count'] = item['ct']

	# 项目成员
	user_list = models.ProjectUser.objects.filter(project_id=project_id).values('user_id', 'user__username')

	# 获取最近的10个任务
	top_ten = models.Issues.objects.filter(project_id=project_id, assign__isnull=False).order_by('-id')[0:10]
	context = {
		'status_dict': status_dict,
		'user_list': user_list,
		'top_ten_object': top_ten,
	}
	return render(request, 'dashboard.html', context)


def issues_chart(request, project_id):
	""" 在概览页面生成highcharts所需要的数据 """
	today = datetime.datetime.now().date()
	data_dict = collections.OrderedDict()
	for i in range(0, 30):
		date = today - datetime.timedelta(days=i)
		data_dict[date.strftime("%Y-%m-%d")] = [time.mktime(date.timetuple()) * 1000, 0]
	""" 生成一个30天每天0问题的初始化字典
		{
			2020-03-31:[1600321987009,0],
			2020-03-31:[1600321987009,0],
			2020-03-31:[1600321987009,0],
			2020-03-31:[1600321987009,0],
		}
	"""
	# 最近30天每天创建的问题数量
	# 去数据库查询最近30天所有数据 & 根据日期每天分组
	"""
	select id,name,email form table
	select id,name,strftime("%Y-%m-%d",create_datetime) as ctime form table
	额外生成一个ctime字段 strftime此为sqlite3时间格式化函数 mysql为 "DATE_FORMAT(web_issues.create_datetime,'%%Y-%%m-%%d')"
	"""
	result = models.Issues.objects.filter(project_id=project_id,
	                                      create_datetime__gte=today - datetime.timedelta(days=30)).extra(
		select={'ctime': "strftime('%%Y-%%m-%%d',web_issues.create_datetime)"}
	).values('ctime').annotate(ct=Count('id'))

	# 查询出的数据结构 <QuerySet [{'ctime': '2020-09-15', 'ct': 4}, {'ctime': '2020-09-17', 'ct': 2}]>
	for item in result:
		data_dict[item['ctime']][1] = item['ct']

	# 返回的30天的数据 data_list = [[1600321987009, 9],[1600321987009, 9],]
	return JsonResponse({'status': True, 'data': list(data_dict.values())})
