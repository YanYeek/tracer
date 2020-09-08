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
from web.forms.wiki import WikiModelForm
from web import models


def wiki(request, project_id):
	"""Wiki首页展示"""
	wiki_id = request.GET.get('wiki_id')
	if not wiki_id or not wiki_id.isdecimal():
		return render(request, 'wiki.html')
	if wiki_id:
		print("文章详细页面")
		wiki_object = models.Wiki.objects.filter(id=wiki_id, project_id=project_id).first()
	else:
		print("文章首页")

	return render(request, 'wiki.html', {'wiki_object': wiki_object})


def wiki_add(request, project_id):
	"""Wiki添加"""
	if request.method == "GET":
		form = WikiModelForm(request)
		return render(request, 'wiki_add.html', {'form': form})
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
	return render(request, 'wiki_add.html', {'form': form})


def wiki_catalog(request, project_id):
	"""Wiki目录"""
	# 获取当前项目的所有目录：data = Queryset类型
	# data = models.Wiki.objects.filter(project=request.tracer.project).values_list('id', 'title', 'parent_id')
	data = models.Wiki.objects.filter(project=request.tracer.project).values('id', 'title', 'parent_id').order_by(
		'depth',
		'id')
	# data = models.Wiki.objects.filter(project=request.tracer.project).values('id', 'title', 'parent_id')

	return JsonResponse({"status": True, "data": list(data)})


def wiki_detail(request, project_id):
	"""
	查看文章详细页面
		/detail?wiki_id=1
		/detail?wiki_id=2
		/detail?wiki_id=3
	"""
	return HttpResponse("查看文章详细")
