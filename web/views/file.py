#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: file.py
@time: 2020/9/10 23:03
@desc:
'''
from django.shortcuts import render
from django.http import JsonResponse

from web.forms.file import FolderModelForm
from web import models


# http://127.0.0.1:8000/manage/6/file/
# http://127.0.0.1:8000/manage/6/file/?folder=9
def file(request, project_id):
	""" 文件列表 & 添加文件夹 """
	if request.method == "GET":
		form = FolderModelForm()
		return render(request, 'file.html', {'form': form})

	parent_object = None
	folder_id = request.GET.get('folder', "")
	if folder_id.isdecimal():
		parent_object = models.FileRepository.objects.filter(id=int(folder_id), file_type=2,
		                                                     project=request.tracer.project).first()
	# 添加文件夹
	form = FolderModelForm(request.POST)
	if form.is_valid():
		form.instance.project = request.tracer.project
		form.instance.file_type = 2
		form.instance.update_user = request.tracer.user
		form.instance.parent = parent_object
		form.save()
		return JsonResponse({'status': True})

	return JsonResponse({'status': False, 'error': form.errors})
