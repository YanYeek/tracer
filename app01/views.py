from django.shortcuts import render, HttpResponse
from django import forms
from app01 import models

# Create your views here.
import random
from utils.tencent.sms import send_sms_single
from django.conf import settings
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


def send_sms(requests):
	"""
	发送短信
	:param requests:
	:return:
	"""
	tpl = requests.GET.get('tpl')
	template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
	if not template_id:
		return HttpResponse('模板不存在')
	code = random.randrange(1000, 9999)
	res = send_sms_single("18108817986", template_id, [code, ])
	if res['result'] == 0:
		return HttpResponse('成功')
	else:
		return HttpResponse(res['errmsg'])


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
			field.widget.attrs['placeholder'] = '请输入%s' % field.label


def register(requests):
	form = RegisterModelForm
	return render(requests, 'web/../web/templates/register.html', {'form': form})
