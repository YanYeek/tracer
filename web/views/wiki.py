#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: wiki.py
@time: 2020/9/8 16:46
@desc:
'''
from django.shortcuts import render, redirect
from django.urls import reverse
from web.forms.wiki import WikiModelForm


def wiki(request, project_id):
	"""Wiki首页展示"""

	return render(request, 'wiki.html')


def wiki_add(request, project_id):
	"""Wiki添加"""
	if request.method == "GET":
		form = WikiModelForm(request)
		return render(request, 'wiki_add.html', {'form': form})
	form = WikiModelForm(request, data=request.POST)
	if form.is_valid():
		form.instance.project = request.tracer.project
		form.save()
		url = reverse('wiki', kwargs={'project_id': project_id})
		return redirect(url)
	return render(request, 'wiki_add.html', {'form': form})
