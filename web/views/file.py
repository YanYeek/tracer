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
from django.forms import model_to_dict

from web.forms.file import FolderModelForm
from web import models


# http://127.0.0.1:8000/manage/6/file/
# http://127.0.0.1:8000/manage/6/file/?folder=9
def file(request, project_id):
	""" 文件列表 & 添加文件夹 """
	parent_object = None
	folder_id = request.GET.get('folder', "")
	if folder_id.isdecimal():
		parent_object = models.FileRepository.objects.filter(id=int(folder_id), file_type=2,
		                                                     project=request.tracer.project).first()
	# GET 查看页面
	if request.method == "GET":

		breadcrumb_list = []
		parent = parent_object
		while parent:
			# breadcrumb_list.insert(0, {'id': parent.id, 'name': parent.name})
			breadcrumb_list.insert(0, model_to_dict(parent, ['id', 'name']))
			parent = parent.parent

		# 把当前目录所有的文件 & 文件夹获取到即可
		queryset = models.FileRepository.objects.filter(project=request.tracer.project)
		if parent_object:
			# 进入了某一个目录
			file_object_list = queryset.filter(parent=parent_object).order_by('-file_type')
		else:
			# 根目录
			file_object_list = queryset.filter(parent__isnull=True).order_by('-file_type')

		form = FolderModelForm(request, parent_object)
		content = {
			'form': form,
			'file_object_list': file_object_list,
			'breadcrumb_list': breadcrumb_list
		}
		return render(request, 'file.html', content)

	# POST 添加文件夹 & 修改文件夹
	fid = request.POST.get('fid', '')
	edit_object = None
	if fid.isdecimal():
		# 修改
		edit_object = models.FileRepository.objects.filter(id=int(fid), file_type=2,
		                                                   project=request.tracer.project).first()
	if edit_object:
		form = FolderModelForm(request, parent_object, data=request.POST, instance=edit_object)

	else:
		form = FolderModelForm(request, parent_object, data=request.POST)

	if form.is_valid():
		form.instance.project = request.tracer.project
		form.instance.file_type = 2
		form.instance.update_user = request.tracer.user
		form.instance.parent = parent_object
		form.save()
		return JsonResponse({'status': True})

	return JsonResponse({'status': False, 'error': form.errors})
