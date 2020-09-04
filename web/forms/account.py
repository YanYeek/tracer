#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: account.py
@time: 2020/9/4 14:03
@desc:
'''
from django import forms
from web import models

from django.conf import settings
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class RegisterModelForm(forms.ModelForm):
	phone = forms.EmailField(label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$'), '手机号格式错误'],
	                         widget=forms.TextInput())

	password = forms.CharField(label='密码',
	                           widget=forms.PasswordInput())
	confirm_password = forms.CharField(label='重复密码', widget=forms.PasswordInput(
	))
	code = forms.CharField(label='验证码',
	                       widget=forms.TextInput())

	class Meta:
		model = models.UserInfo
		fields = ['username', 'email', 'password', 'confirm_password', 'phone', 'code']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'
			field.widget.attrs['placeholder'] = f'请输入{field.label}'
