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
from utils import encrypt
from django_redis import get_redis_connection

from django import forms
from web import models
from django.conf import settings

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from web.forms.bootstrap import BootStrapForm


class RegisterModelForm(BootStrapForm, forms.ModelForm):
	password = forms.CharField(label='密码',
	                           min_length=8,
	                           max_length=64,
	                           error_messages={
		                           'min_length': "密码长度不能少于8个字符",
		                           'max_length': "密码长度不能多于64个字符",
	                           },
	                           widget=forms.PasswordInput(),
	                           )

	confirm_password = forms.CharField(label='重复密码', widget=forms.PasswordInput(
	))
	phone = forms.CharField(label='手机号',
	                        validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ],
	                        widget=forms.TextInput(),
	                        )

	code = forms.CharField(label='验证码',
	                       widget=forms.TextInput())

	class Meta:
		model = models.UserInfo
		# 钩子函数校验顺序与下方列表一致，字段定义顺序也要统一，否则校验时cleaned_data获取不到值。
		fields = ['username', 'email', 'password', 'confirm_password', 'phone', 'code']

	def clean_username(self):
		username = self.cleaned_data.get('username')
		exists = models.UserInfo.objects.filter(username=username).exists()
		if exists:
			raise ValidationError('用户名已存在')
		return username

	def clean_email(self):
		email = self.cleaned_data.get('email')
		exists = models.UserInfo.objects.filter(username=email).exists()
		if exists:
			raise ValidationError('邮箱已存在')
		return email

	def clean_password(self):
		pwd = self.cleaned_data.get('password')
		# 加密 & 返回
		return encrypt.md5(pwd)

	def clean_confirm_password(self):
		pwd = self.cleaned_data.get('password')
		confirm_pwd = encrypt.md5(self.cleaned_data.get('confirm_password'))
		if pwd != confirm_pwd:
			raise ValidationError('两次密码不一致')
		return confirm_pwd

	def clean_phone(self):
		phone = self.cleaned_data.get('phone')
		exists = models.UserInfo.objects.filter(phone=phone).exists()
		if exists:
			raise ValidationError('手机号已注册')
		return phone

	def clean_code(self):
		code = self.cleaned_data.get('code')
		phone = self.cleaned_data.get('phone')
		conn = get_redis_connection()
		redis_code = conn.get(str(phone))
		if not redis_code:
			raise ValidationError('验证码失效或未发生，请重新发送')

		redis_str_code = redis_code.decode('utf-8')
		if code.strip() != redis_str_code:
			raise ValidationError('验证码错误，请重新输入')

		return code


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

		exists = models.UserInfo.objects.filter(phone=phone).exists()

		if tpl == "login":
			if not exists:
				raise ValidationError('手机号不存在,请注册。')

		else:
			# 校验数据库中是否已有手机号
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


class LoginSMSForm(BootStrapForm, forms.Form):
	phone = forms.CharField(label='手机号',
	                        validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ],
	                        widget=forms.TextInput(),
	                        )

	code = forms.CharField(label='验证码', widget=forms.TextInput())

	def clean_phone(self):
		phone = self.cleaned_data.get('phone')
		user_object = models.UserInfo.objects.filter(phone=phone).first()
		if not user_object:
			raise ValidationError('手机号不存在')

		return user_object

	def clean_code(self):
		code = self.cleaned_data.get('code')
		user_object = self.cleaned_data.get('phone')

		# 手机号不存在，则无需校验。
		if not user_object:
			return code

		conn = get_redis_connection()
		redis_code = conn.get(user_object.phone)
		if not redis_code:
			raise ValidationError('验证码失效或未发生，请重新发送')

		redis_str_code = redis_code.decode('utf-8')

		if code.strip() != redis_str_code:
			raise ValidationError('验证码错误，请重新输入')

		return code


class LoginForm(BootStrapForm, forms.Form):
	username = forms.CharField(label="邮箱或手机号")
	password = forms.CharField(label="密码", widget=forms.PasswordInput(render_value=True))
	code = forms.CharField(label="图片验证码")

	def __init__(self, request, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.request = request

	def clean_password(self):
		pwd = self.cleaned_data.get('password')
		# 加密 & 返回
		return encrypt.md5(pwd)

	def clean_code(self):
		"""钩子 图片验证码是否正确"""
		# 读取用户输入的验证码
		code = self.cleaned_data.get('code')
		# 去session获取自己的验证码
		session_code = self.request.session.get('image_code')

		if not session_code:
			raise ValidationError('验证码已过期，请重新获取！')

		if code.strip().upper() != session_code.upper():
			raise ValidationError('验证码输入错误！')

		return code
