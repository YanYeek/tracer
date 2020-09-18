#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: home.py
@time: 2020/9/5 21:29
@desc:
'''
import datetime
import json

from django.shortcuts import render, redirect
from django_redis import get_redis_connection

from web import models
from utils.encrypt import uid


def index(request):
	return render(request, 'index.html')


def price(request):
	""" 套餐 """
	# 获取套餐
	policy_list = models.PricePolicy.objects.filter(category=2)
	return render(request, 'price.html', {'policy_list': policy_list})


def payment(request, policy_id):
	""" 支付页面 """
	# 1. 价格策略{套餐）policy_id
	policy_object = models.PricePolicy.objects.filter(id=policy_id, category=2).first()
	if not policy_object:
		return redirect('price')
	# 2. 要购买的数量
	number = request.GET.get('number')
	if not number or not number.isdecimal():
		return redirect('price')
	number = int(number)
	if number < 1:
		return redirect('price')

	# 3. 计算原价
	origin_price = number * policy_object.price

	# 4. 之前购买过套餐
	balance = 0
	_object = None
	if request.tracer.price_policy.category == 2:
		# 找到之前订单：总支付费用、开始结束时间、剩余天数=抵扣的钱
		_object = models.Transaction.objects.filter(user=request.tracer.user, status=2).order_by('-id').first()
		#
		total_time_delta = _object.end_datetime - _object.start_datetime
		balance_time_delta = _object.end_datetime - datetime.datetime.now()
		if total_time_delta.days == balance_time_delta.days:
			balance = _object.price / total_time_delta.days * (balance_time_delta.days - 1)
		else:
			balance = _object.price / total_time_delta.days * balance_time_delta.days
	if balance >= origin_price:
		return redirect('price')

	context = {
		'policy_id': policy_id,
		'number': number,
		'origin_price': origin_price,
		'balance': round(balance, 2),
		'total_price': origin_price - round(balance, 2)
	}

	# 存入订单信息，30分钟失效
	conn = get_redis_connection()
	key = f'payment_{request.tracer.user.phone}'
	conn.set(key, json.dumps(context), ex=60 * 30)

	context['policy_object'] = policy_object
	context['transaction'] = _object

	return render(request, 'payment.html', context)


def pay(request):
	""" 生成订单 & 支付宝支付 """
	# 方法1 需要对提交的数据再次做校验
	# 方法1 使用redis保存30分钟订单
	conn = get_redis_connection()
	key = f'payment_{request.tracer.user.phone}'
	context_string = conn.get(key)
	if not context_string:
		return redirect('price')
	context = json.loads(context_string.encode('utf-8'))

	# 1. 数据库中生成交易记录（待支付） ——等支付成功后需要更新订单的支付状态与写入可使用时间
	order_id = uid(request.tracer.user.phone)
	models.Transaction.objects.create(
		status=1,
		order=order_id,
		user=request.tracer.user,
		price_policy_id=context['policy_id'],
		count=context['number'],
		price=context['total_price'],
	)
	# 2. 跳转到支付宝
	# - 生成一个支付的链接
	# - 跳转到这个链接
	url = '支付宝链接'
