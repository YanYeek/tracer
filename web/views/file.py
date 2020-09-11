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
from utils.tencent.cos import delete_file
from utils.tencent.cos import delete_file_list
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


# http://127.0.0.1:8000/manage/6/file/delete?fid=9
def file_delete(request, project_id):
	""" 删除文件 """
	fid = request.GET.get('fid')
	# 删除了文件 or 文件夹 （级联删除）
	delete_object = models.FileRepository.objects.filter(id=fid, project=request.tracer.project).first()

	if delete_object.file_type == 1:
		# 删除文件（数据库文件删除、cos存储文件删除、项目空间容量还回去 单位：默认字节）
		# 删除文件，将容量返还当前项目
		request.tracer.project.use_space -= delete_object.file_size
		request.tracer.project.use_space.save()

		# cos中删除文件
		delete_file(bucket=request.tracer.project.bucket, region=request.tracer.project.bucket.region,
		            key=delete_object.key)
		# 数据库中删除当前文件
		delete_object.delete()
		return JsonResponse({'status': True})

	# 删除文件夹（找到文件夹下的所有文件->数据库文件删除、cos存储文件删除、项目空间容量还回去）
	# delete_object.
	# 找到文件夹下面的所有文件和文件夹
	total_size = 0
	key_list = []
	folder_list = [delete_object, ]
	for folder in folder_list:
		child_list = models.FileRepository.objects.filter(project=request.tracer.project, parent=folder).order_by(
			'-file_type')
		for child in child_list:
			if child.file_type == 2:
				# 文件夹
				folder_list.append(child)
			else:
				# 文件大小汇总
				total_size += child.file_size
				# 删除文件
				key_list.append({"Key": child.key})

	# models.FileRepository.objects.filter(parent=delete_object)  # 文件 删除；文件夹 继续往里查找
	# 批量删除文件 cos
	delete_file_list(bucket=request.tracer.project.bucket, region=request.tracer.project.bucket.region,
	                 key_list=key_list)
	# 归还容量
	if total_size:
		request.tracer.project.use_space -= total_size
		request.tracer.project.use_space.save()
	delete_object.delete()
	return JsonResponse({'status': True})
