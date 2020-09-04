#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: account.py
@time: 2020/9/4 14:03
@desc:
'''
import random
from utils.tencent.sms import send_sms_single
from django_redis import get_redis_connection

from django import forms
from web import models
from django.conf import settings

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class RegisterModelForm(forms.ModelForm):
	phone = forms.EmailField(label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ],
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
			field.widget.attrs['placeholder'] = '请输入%s' % field.label


class SendSmsForm(forms.Form):
	phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])

	# 重写初始化函数来获取试图函数中的传值
	def __init__(self, request, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.request = request

	def clean_phone(self):
		"""手机号校验的钩子函数"""
		phone = self.cleaned_data['phone']

		# 判断短信模板是否有问题
		tpl = self.request.GET.get('tpl')
		template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
		if not template_id:
			# self.add_error('phone', '短信模板错误')
			raise ValidationError('模板错误')

		# 校验数据库中是否已有手机号
		exists = models.UserInfo.objects.filter(phone=phone).exists()
		if exists:
			raise ValidationError('手机号已存在')

		code = random.randrange(1000, 9999)
		# 发短信
		sms = send_sms_single(phone, template_id, [code, ])
		if sms['result'] != 0:
			raise ValidationError('短信发送失败，{}'.format(sms['errmsg']))

		# 验证码写入redis（django-redis）
		conn = get_redis_connection()
		conn.set(phone, code, ex=60)

		return phone
