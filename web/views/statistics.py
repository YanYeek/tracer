#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: statistics.py
@time: 2020/9/8 11:36
@desc:
'''
import collections
from django.shortcuts import render
from django.db.models import Count
from django.http import JsonResponse

from web import models


def statistics(request, project_id):
	""" 统计页面 """

	return render(request, 'statistics.html')


def statistics_priority(request, project_id):
	""" 按优先级生成饼图数据 """
	# 找到所有的问题，根据优先级分组，得到每个优先级问题的数量，构造成字典
	start = request.GET.get('start')
	end = request.GET.get('end')

	# 1 构造字典
	data_dict = collections.OrderedDict()
	for key, text in models.Issues.priority_choices:
		data_dict[key] = {'name': text, 'y': 0}

	# 2 去数据库查询所有分组得到的数据
	result = models.Issues.objects.filter(project_id=project_id, create_datetime__gte=start,
	                                      create_datetime__lt=end).values('priority').annotate(ct=Count('id'))

	# 3 把分组得到的数据更新到字典中
	for item in result:
		data_dict[item['priority']]['y'] = item['ct']

	return JsonResponse({'status': True, 'data': list(data_dict.values())})


def statistics_project_user(request, project_id):
	""" 项目成员某个人被分配的任务数量（问题类型的配比） """
	"""
	info = {
		1:{
			name:"YanYeek",
			status:{
			1:0,
			2:0,
			3:0,
			4:0,
			5:0,
			6:0,
			7:0,
			}
		},
	}
		2:{
			name:"CC",
			status:{
			1:0,
			2:0,
			3:0,
			4:0,
			5:0,
			6:0,
			7:0,
			}
		},
	}
	"""
	start = request.GET.get('start')
	end = request.GET.get('end')
	# 1 找到所有的问题并且需要根据指派的用户分组
	all_user_dict = collections.OrderedDict()
	all_user_dict[request.tracer.project.creator.id] = {
		'name': request.tracer.project.creator.username,
		'status': {item[0]: 0 for item in models.Issues.status_choices}
	}

	all_user_dict[None] = {
		'name': '未指派',
		'status': {item[0]: 0 for item in models.Issues.status_choices}
	}

	# 现已经有了所有的项目成员以及未指派任务
	user_list = models.ProjectUser.objects.filter(project_id=project_id)
	for item in user_list:
		all_user_dict[item.user_id] = {
			'name': item.user.username,
			'status': {item[0]: 0 for item in models.Issues.status_choices}
		}

	# 2 去数据库获取所有修改的数据
	issues = models.Issues.objects.filter(project_id=project_id, create_datetime__gte=start, create_datetime__lt=end)

	for item in issues:
		if not item.assign:
			all_user_dict[None]['status'][item.status] += 1
		else:
			all_user_dict[item.assign_id]['status'][item.status] += 1

	# 3 获取所有的成员
	categories = [data['name'] for data in all_user_dict.values()]

	# 4 构造字典
	"""
	info = {
		1:{name:新建,data:[]}
		2:{name:新建,data:[]}
		3:{name:新建,data:[]}
		4:{name:新建,data:[]}
		5:{name:新建,data:[]}
		6:{name:新建,data:[]}
		7:{name:新建,data:[]}
	}
	"""
	data_result_dict = collections.OrderedDict()
	for item in models.Issues.status_choices:
		data_result_dict[item[0]] = {'name': item[1], 'data': []}

	for key, text in models.Issues.status_choices:
		for row in all_user_dict.values():
			count = row['status'][key]
			data_result_dict[key]['data'].append(count)

	content = {
		'status': True,
		'data': {
			'categories': categories,
			'series': list(data_result_dict.values())
		},
	}
	return JsonResponse(content)
