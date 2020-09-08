#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: auth.py
@time: 2020/9/5 21:55
@desc:
'''
import datetime

from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from web import models
from django.conf import settings


class Tracer(object):
	def __init__(self):
		self.user = None
		self.price_policy = None
		self.project = None


class AuthMiddleware(MiddlewareMixin):
	def process_request(self, request):
		"""
		如果用户已登录，则再request中赋值
		:param request:
		:return:
		"""
		request.tracer = Tracer()

		user_id = request.session.get('user_id', 0)
		user_object = models.UserInfo.objects.filter(id=user_id).first()
		request.tracer.user = user_object

		# url 白名单
		"""
		1. 获取当前用户访问的URL
		2. 检查URL是否在白名单，如果有就可以继续向后访问，如果不在则判断是否已登录
		"""
		if request.path_info in settings.WHITE_REGEX_LIST:
			return
		# 检查用户是否登录，已登录继续往后走；未登录则返回登录页面。
		if not request.tracer.user:
			return redirect('login')

		# 登录成功后 访问后台管理时：获取当前用户所拥有的额度
		# 方式一：免费额度在交易记录中存储
		# 获取当前用户ID值最大（最近的交易记录）
		_object = models.Transaction.objects.filter(user=user_object, status=2).order_by('-id').first()

		# 判断是否过期
		current_datetime = datetime.datetime.now()
		if _object.end_datetime and _object.end_datetime < current_datetime:
			# 过期
			# _object = models.Transaction.objects.filter(user=user_object, status=2).order_by('-id').first()
			_object = models.Transaction.objects.filter(user=user_object, status=2, price_policy=1).order_by(
				'-id').first()
		request.tracer.price_policy = _object.price_policy

	# 方式二：免费额度存储在配置文件中
	# 获取当前用户ID值最大（最近的交易记录）
	# _object = models.Transaction.objects.filter(user=user_object, status=2).order_by('-id').first()
	# if not _object:
	# 	# 没有购买
	# 	request.price_policy = models.PricePolicy.objects.filter(category=1, title='个人免费版').first()
	# else:
	# 	# 付费版
	# 	# 判断是否过期
	# 	current_datetime = datetime.datetime.now()
	# 	if _object.end_datetime and _object.end_datetime < current_datetime:
	# 		request.price_policy = models.PricePolicy.objects.filter(category=1, title='个人免费版').first()
	# 	else:
	# 		request.price_policy = _object.price_policy

	def process_view(self, request, view, args, kwargs):
		# 判断URL是否以manage开头？ 如果是则判断项目ID是否由我创建 or 参与
		if not request.path_info.startswith('/manage/'):
			return
		# project_id 是我创建的 or 我参与的？
		project_id = kwargs.get('project_id')

		project_object = models.Project.objects.filter(creator=request.tracer.user, id=project_id, ).first()
		if project_object:
			# 是我创建的项目的话，我就让他通过。
			request.tracer.project = project_object
			return
		# 是否我参与的项目
		project_user_object = models.ProjectUser.objects.filter(user=request.tracer.user, id=project_id, ).first()
		if project_user_object:
			# 是我参与的项目
			request.tracer.project = project_user_object.project
			return

		return redirect('project_list')
