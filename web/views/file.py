#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: file.py
@time: 2020/9/10 23:03
@desc:
'''
from django.shortcuts import render, reverse, HttpResponse
from django.utils.encoding import escape_uri_path
from django.http import JsonResponse
from django.forms import model_to_dict
from django.views.decorators.csrf import csrf_exempt
import json
import requests

from web.forms.file import FolderModelForm
from web.forms.file import FileModelForm
from utils.tencent.cos import delete_file
from utils.tencent.cos import credential
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
			'breadcrumb_list': breadcrumb_list,
			'folder_object': parent_object,
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
		request.tracer.project.use_space += delete_object.file_size
		request.tracer.project.save()

		# cos中删除文件
		delete_file(bucket=request.tracer.project.bucket, region=request.tracer.project.region,
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
	# delete_file_list(bucket=request.tracer.project.bucket, region='cp-chengdu',
	#                  key_list=key_list)
	# 归还容量
	if total_size:
		request.tracer.project.use_space -= total_size
		request.tracer.project.save()
	delete_object.delete()
	return JsonResponse({'status': True})


@csrf_exempt
def cos_credential(request, project_id):
	"""获取cos凭证"""
	per_file_limit = request.tracer.price_policy.project_size * 1024 * 1024
	total_file_limit = request.tracer.price_policy.project_space * 1024 * 1024 * 1024
	total_size = 0
	file_list = json.loads(request.body.decode('utf-8'))
	for item in file_list:
		# 文件的字节大小 item['size'] = B
		# 单文件限制大小 M
		if item['size'] > per_file_limit:
			return JsonResponse({'status': False, 'error': f"单文件超出限制，最大{per_file_limit}M,文件{item['name']},请升级套餐。"})
		total_size += item['size']

	# 总容量限制
	# request.tracer.price_policy.project_space  # 项目运行的空间
	# request.tracer.project.use_space  # 已使用空间
	if request.tracer.project.use_space + total_size > total_file_limit:
		return JsonResponse({'status': False, 'error': "容量超出限制，请升级套餐。"})
	# 获取要上传的每个文件及每个文件大小
	data_dict = credential(bucket=request.tracer.project.bucket, region=request.tracer.project.region)
	return JsonResponse({'status': True, 'data': data_dict})


@csrf_exempt
def file_post(request, project_id):
	""" 已上传成功的文件写入到数据库 """
	"""
	name: fileName,
	key: key,
	fileSize: fileSize,
	parent: CURRENT_FOLDER_ID,
	etag: data.ETag,
	file_path: data.Location,
	"""
	# 根据key再去cos获取文件ETag和"32e46edebc7b1a8f3ae2b07366b34b3a"

	# 把获取到的数据写入数据库即可
	# models.FileRepository.objects.filter()
	form = FileModelForm(request, data=request.POST)
	if form.is_valid():
		# 校验通过写入数据库
		# 通过ModelForm.save存储到数据库中的数据返回的instance对象，无法获取choice的中文。
		# form.instance.file_type = 1
		# form.instance.update_user = request.tracer.user
		# form.save() # 添加成功后获取到新添加的那个对象（instance.id,instance.name，instance。get_file_type_display()）

		data_dict = form.cleaned_data
		# data_dict.pop('etag')
		data_dict.update({'project': request.tracer.project, 'file_type': 1, 'update_user': request.tracer.user})
		instance = models.FileRepository.objects.create(**data_dict)

		# 项目的已使用空间:更新
		request.tracer.project.use_space += data_dict['file_size']
		request.tracer.project.save()
		result = {
			'id': instance.id,
			'name': instance.name,
			'file_size': instance.file_size,
			'username': instance.update_user.username,
			'datetime': instance.update_datetime.strftime('%Y{y}%m{m}%d{d} %H:%M').format(y='年', m='月', d='日'),
			'download_url': reverse('download', kwargs={"project_id": project_id, "file_id": instance.id}),
		}
		return JsonResponse({'status': True, 'data': result})

	return JsonResponse({'status': False, 'data': "文件错误"})


def download(request, project_id, file_id):
	""" 用户点击下载文件 """
	file_object = models.FileRepository.objects.filter(id=file_id, project_id=project_id).first()
	# 文件分块处理（适用于大文件）
	res = requests.get(file_object.file_path)
	data = res.iter_content()
	# 设置content_type='application/octet-stream' 用于提示下载框
	response = HttpResponse(data, content_type='application/octet-stream')

	# 设置响应头：中文文件名转义
	response["Content-Disposition"] = "attachment; filename={}".format(escape_uri_path(file_object.name))
	return response
