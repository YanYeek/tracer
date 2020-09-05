#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: account.py
@time: 2020/9/4 12:36
@desc:用户相关功能：注册、短信、登录、注销
'''
from django.shortcuts import render
from django.http import JsonResponse
from web.forms.account import RegisterModelForm, SendSmsForm, LoginSMSForm
# from django.views.decorators.csrf import csrf_exempt # 装饰驶入函数@csrf_exempt
from web import models


def register(request):
	"""
	注册页面
	:param requests:
	:return:
	"""
	if request.method == "GET":
		form = RegisterModelForm()
		return render(request, 'register.html', {'form': form})
	form = RegisterModelForm(data=request.POST)
	if form.is_valid():
		# 验证通过，写入数据库（密码要是密文）
		# instance = models.UserInfo.objects.create(**form.cleaned_data) # 此方法包含无用数据段，需要手动剔除。
		form.save()  # 此方法可自动剔除无用数据。此函数可返回刚刚创建数据一个对象instance
		return JsonResponse({'status': True, 'data': '/login/'})

	return JsonResponse({'status': False, 'error': form.errors})


def send_sms(request):
	"""
	发送短信
	:param requests:
	:return:
	"""
	form = SendSmsForm(request, data=request.GET)
	# 只校验手机号：不能为空、格式是否正确
	if form.is_valid():
		return JsonResponse({'status': True})

	return JsonResponse({'status': False, 'error': form.errors})



def login_sms(request):
	"""
	短信登录
	:param request:
	:return:
	"""
	if request.method == "GET":
		form = LoginSMSForm()
		return render(request, 'login_sms.html', {'form': form})

	form = LoginSMSForm(request.POST)
	if form.is_valid():
		# 用户输入正确，登录成功。
		user_object = form.cleaned_data.get('phone')
		# 用户信息放入session
		request.session['user_id'] = user_object.id
		request.session['user_name'] = user_object.username
		return JsonResponse({'status': True, 'data': "/index/"})

	return JsonResponse({'status': False, 'error': form.errors})
