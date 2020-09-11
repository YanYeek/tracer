#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: file.py
@time: 2020/9/11 1:35
@desc:
'''
from django import forms

from web import models
from web.forms.bootstrap import BootStrapForm


class FolderModelForm(BootStrapForm, forms.ModelForm):
	class Meta:
		model = models.FileRepository
		fields = ['name', ]
