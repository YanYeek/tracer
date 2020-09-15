#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: issues.py
@time: 2020/9/14 21:47
@desc:
'''
from django.shortcuts import render
from django.http import JsonResponse

from web.forms.issues import IssuesModalForm
from utils.pagination import Pagination
from web import models


def issues(request, project_id):
	if request.method == "GET":
		# 分页获取数据
		queryset = models.Issues.objects.filter(project_id=project_id)

		page_object = Pagination(
			current_page=request.GET.get('page'),
			all_count=queryset.count(),
			base_url=request.path_info,
			query_params=request.GET,
			per_page=1,
		)
		issues_object_list = queryset[page_object.start:page_object.end]

		form = IssuesModalForm(request)
		context = {
			'form': form,
			'issues_object_list': issues_object_list,
			'page_html': page_object.page_html()
		}
		return render(request, 'issues.html', context=context)

	print(request.POST)
	form = IssuesModalForm(request, data=request.POST)
	if form.is_valid():
		form.instance.project = request.tracer.project
		form.instance.creator = request.tracer.user
		form.save()
		return JsonResponse({'status': True})

	return JsonResponse({'status': False, 'error': form.errors})


def issues_detail(request, project_id, issues_id):
	""" 编辑问题 """
	issues_object = models.Issues.objects.filter(id=issues_id, project_id=project_id).first()
	form = IssuesModalForm(request, instance=issues_object)
	return render(request, 'issues_detail.html', {'form': form})
