#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: wiki.py
@time: 2020/9/8 17:18
@desc:
'''
from django import forms

from web import models
from web.forms.bootstrap import BootStrapForm


class WikiModelForm(BootStrapForm, forms.ModelForm):
	class Meta:
		model = models.Wiki
		exclude = ['project', 'depth', ]

	def __init__(self, request, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.request = request

		# 找到需要的字段把它绑定的数据重置
		# 数据 = 去数据库中获取当前项目首页的Wiki标题
		total_data_list = [("", "请选择")]
		data_list = models.Wiki.objects.filter(project=request.tracer.project).values_list('id', 'title')
		total_data_list.extend(data_list)
		self.fields['parent'].choices = total_data_list
