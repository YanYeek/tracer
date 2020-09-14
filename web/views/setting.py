#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: setting.py
@time: 2020/9/14 19:39
@desc:
'''
from django.shortcuts import render, redirect

from utils.tencent.cos import delete_bucket
from web import models


def setting(request, project_id):
	return render(request, 'setting.html')


def delete(request, project_id):
	"""删除项目"""
	if request.method == "GET":
		return render(request, 'setting_delete.html')

	project_name = request.POST.get('project_name')
	if not project_name or project_name != request.tracer.project.name:
		return render(request, 'setting_delete.html', {'error': "项目名称错误"})

	# 项目名写对 删除（只有创建者跨域删除）
	if request.tracer.user != request.tracer.project.creator:
		return render(request, 'setting_delete.html', {'error': "只有创建者可删除项目"})

	# 1. 删除桶
	#  删除桶中所有文件（找到桶中的所有文件+ 碎片 + 桶）
	delete_bucket(bucket=request.tracer.project.bucket, region=request.tracer.project.region)

	# 2. 删除项目
	models.Project.objects.filter(id=project_id).delete()

	return redirect("project_list")
