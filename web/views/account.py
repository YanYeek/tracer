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
from web.forms.account import RegisterModelForm, SendSmsForm


def register(request):
	"""
	注册页面
	:param requests:
	:return:
	"""
	form = RegisterModelForm()
	return render(request, 'register.html', {'form': form})


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
