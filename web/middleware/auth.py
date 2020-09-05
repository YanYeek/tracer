#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: auth.py
@time: 2020/9/5 21:55
@desc:
'''
from django.utils.deprecation import MiddlewareMixin
from web import models


class AuthMiddleware(MiddlewareMixin):
	def process_request(self, request):
		"""
		如果用户已登录，则再request中赋值
		:param request:
		:return:
		"""
		user_id = request.session.get('user_id', 0)
		user_object = models.UserInfo.objects.filter(id=user_id).first()
		request.tracer = user_object
