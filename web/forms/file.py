#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: file.py
@time: 2020/9/11 1:35
@desc:
'''
from django import forms
from django.core.exceptions import ValidationError

from web import models
from web.forms.bootstrap import BootStrapForm


class FolderModelForm(BootStrapForm, forms.ModelForm):
	class Meta:
		model = models.FileRepository
		fields = ['name', ]

	def __init__(self, request, parent_object, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.request = request
		self.parent_object = parent_object

	def clean_name(self):
		name = self.cleaned_data.get('name')
		# 数据库判断 当前目录下 此文件夹是否已存在
		queryset = models.FileRepository.objects.filter(file_type=2, name=name, project=self.request.tracer.project)
		if self.parent_object:
			exists = queryset.filter(parent=self.parent_object).exists()

		else:
			exists = queryset.filter(parent__isnull=True).exists()
		if exists:
			raise ValidationError('文件夹已存在')
		return name
