#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: issues.py
@time: 2020/9/14 22:10
@desc:
'''
from django import forms

from web.forms.bootstrap import BootStrapForm
from web import models


class IssuesModalForm(BootStrapForm, forms.ModelForm):
	class Meta:
		model = models.Issues
		exclude = ['project', 'creator', 'create_datetime', 'latest_update_datetime']
		widgets = {
			'assign': forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'}),
			'attention': forms.SelectMultiple(
				attrs={'class': 'selectpicker', 'data-live-search': 'true', 'data-actions-box': 'true'}),
		}
