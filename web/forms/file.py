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
from qcloud_cos.cos_exception import CosServiceError

from web import models
from web.forms.bootstrap import BootStrapForm
from utils.tencent.cos import check_file


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


class FileModelForm(forms.ModelForm):
	""""""

	class Meta:
		model = models.FileRepository
		exclude = ['project', 'file_type', 'update_user']

	def __init__(self, request, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.request = request
		self.etag = request.POST.get('etag')

	def clean_file_path(self):
		return f"https://{self.cleaned_data.get('file_path')}"

	def clean(self):
		key = self.cleaned_data.get('key')
		etag = self.etag
		size = self.cleaned_data.get('file_size')
		if not key or etag:
			return self.cleaned_data

		# 向cos校验文件是否合法
		# SDK的功能
		try:
			result = check_file(
				bucket=self.request.tracer.project.bucket,
				region=self.request.tracer.project.region,
				key=key,
			)
		except CosServiceError as e:
			self.add_error(key, '文件不存在')
			return self.cleaned_data

		cos_eTag = result.get('Etag')
		if etag != cos_eTag:
			self.add_error('etag', 'ETag错误')

		cos_length = result.get('Content-Length')
		if int(cos_length) != size:
			self.add_error('size', '文件大小错误')

		return self.cleaned_data
