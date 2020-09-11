#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: wiki.py
@time: 2020/9/8 16:46
@desc:
'''
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from django.conf import settings

from utils.encrypt import uid
from utils.tencent.cos import upload_file
from web.forms.wiki import WikiModelForm
from web import models


def wiki(request, project_id):
	"""Wiki首页展示"""
	wiki_id = request.GET.get('wiki_id')
	if not wiki_id or not wiki_id.isdecimal():
		return render(request, 'wiki.html')
	if wiki_id:
		wiki_object = models.Wiki.objects.filter(id=wiki_id, project_id=project_id).first()
		return render(request, 'wiki.html', {'wiki_object': wiki_object})

	return render(request, 'wiki.html')


def wiki_add(request, project_id):
	"""Wiki添加"""
	if request.method == "GET":
		form = WikiModelForm(request)
		return render(request, 'wiki_form.html', {'form': form})
	form = WikiModelForm(request, data=request.POST)
	if form.is_valid():
		# 判断用户是否选择父文章，如选择就在父文章的深度上加1。
		if form.instance.parent:
			form.instance.depth = form.instance.parent.depth + 1
		else:
			form.instance.depth = 1
		form.instance.project = request.tracer.project
		form.save()
		url = reverse('wiki', kwargs={'project_id': project_id})
		return redirect(url)
	return render(request, 'wiki_form.html', {'form': form})


def wiki_catalog(request, project_id):
	"""Wiki目录"""
	# 获取当前项目的所有目录：data = Queryset类型
	# data = models.Wiki.objects.filter(project=request.tracer.project).values_list('id', 'title', 'parent_id')
	data = models.Wiki.objects.filter(project=request.tracer.project).values('id', 'title', 'parent_id').order_by(
		'depth',
		'id')
	# data = models.Wiki.objects.filter(project=request.tracer.project).values('id', 'title', 'parent_id')

	return JsonResponse({"status": True, "data": list(data)})


# def wiki_detail(request, project_id):
# 	"""
# 	查看文章详细页面
# 		/detail?wiki_id=1
# 		/detail?wiki_id=2
# 		/detail?wiki_id=3
# 	"""
# 	return HttpResponse("查看文章详细")


def wiki_delete(request, project_id, wiki_id):
	"""删除wiki"""
	models.Wiki.objects.filter(project_id=project_id, id=wiki_id).delete()
	url = reverse('wiki', kwargs={'project_id': project_id})
	return redirect(url)


def wiki_edit(request, project_id, wiki_id):
	"""编辑Wiki"""
	wiki_object = models.Wiki.objects.filter(project_id=project_id, id=wiki_id).first()
	if not wiki_object:
		url = reverse('wiki', kwargs={'project_id': project_id})
		return redirect(url)

	if request.method == "GET":
		form = WikiModelForm(request, instance=wiki_object)
		return render(request, 'wiki_form.html', {'form': form})
	form = WikiModelForm(request, data=request.POST, instance=wiki_object)
	if form.is_valid():
		# 判断用户是否选择父文章，如选择就在父文章的深度上加1。
		if form.instance.parent:
			form.instance.depth = form.instance.parent.depth + 1
		else:
			form.instance.depth = 1
		form.instance.project = request.tracer.project
		form.save()
		url = reverse('wiki', kwargs={'project_id': project_id})
		preview_url = f"{url}?wiki_id={wiki_id}"
		return redirect(preview_url)

	return render(request, 'wiki_form.html', {'form': form})


@csrf_exempt
def wiki_upload(request, project_id):
	"""markdown插件上传图片"""
	# 1. 接收到图片对象
	result = {
		'success': 0,
		'message': None,
		'url': None,
	}
	image_object = request.FILES.get("editormd-image-file")
	if not image_object:
		result['message'] = "文件不存在"
		return JsonResponse(result)

	ext = image_object.name.rsplit('.')[-1]
	key = "{}.{}".format(uid(request.tracer.user.phone), ext)
	# 2. 文件对象上传到当前项目的桶中
	image_url = upload_file(
		request.tracer.project.bucket,
		request.tracer.project.region,
		image_object,
		key,
	)
	result['success'] = 1
	result['url'] = image_url
	return JsonResponse(result)
