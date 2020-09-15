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
from web import models


def issues(request, project_id):
	if request.method == "GET":
		form = IssuesModalForm(request)
		issues_object_list = models.Issues.objects.filter(project_id=project_id)
		return render(request, 'issues.html', {'form': form, 'issues_object_list': issues_object_list})
	print(request.POST)
	form = IssuesModalForm(request, data=request.POST)
	if form.is_valid():
		form.instance.project = request.tracer.project
		form.instance.creator = request.tracer.user
		form.save()
		return JsonResponse({'status': True})

	return JsonResponse({'status': False, 'error': form.errors})
