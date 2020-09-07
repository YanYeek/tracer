#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: project.py
@time: 2020/9/7 2:00
@desc:
'''
from django.shortcuts import render
from django.http import JsonResponse
from web.forms.project import ProjectModelForm


def project_list(request):
	"""项目列表"""
	if request.method == "GET":
		form = ProjectModelForm(request)

		return render(request, 'project_list.html', {'form': form})

	form = ProjectModelForm(request, data=request.POST)
	if form.is_valid():
		# 验证通过: 项目名、颜色、描述 + creator谁创建的项目
		form.instance.creator = request.tracer.user
		# 创建项目
		form.save()
		return JsonResponse({'status': True})

	# 验证不通过 返回错误信息
	return JsonResponse({'status': False, 'error': form.errors})
