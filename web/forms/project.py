#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: project.py
@time: 2020/9/7 15:38
@desc:
'''

from django import forms
from django.core.exceptions import ValidationError
from web.forms.bootstrap import BootStrapForm
from web import models
from web.forms.widgets import ColorRadioSelect


class ProjectModelForm(BootStrapForm, forms.ModelForm):
	# desc = forms.CharField(widget=forms.Textarea)
	bootstrap_class_exclude = ['color']

	class Meta:
		model = models.Project
		fields = ['name', 'color', 'desc']
		widgets = {
			'desc': forms.Textarea,
			'color': ColorRadioSelect(attrs={"class": "color-radio"}),
		}

	# 重写初始化函数来获取试图函数中的传值
	def __init__(self, request, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.request = request

	def clean_name(self):
		"""项目校验"""
		name = self.cleaned_data.get('name')
		# 1. 当前用户是否已创建过此项目

		# 1.1 十一日是否已创建过此项目。
		exists = models.Project.objects.filter(name=name, creator=self.request.tracer.user).exists()
		if exists:
			raise ValidationError('项目名已存在')
		# 2. 当前用户是否还有额度创建此项目
		# 此用户最大创建项目额度
		max_project_num = self.request.tracer.price_policy.project_num

		# 现在当前项目已创建项目数？
		count = models.Project.objects.filter(creator=self.request.tracer.user).count()

		if count >= max_project_num:
			raise ValidationError('项目个数超限，去购买套餐！')
		return name
