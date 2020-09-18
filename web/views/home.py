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
		# 找到之前订单:总支付费用、开始结束时间、剩余天数=抵扣的钱
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

"""
def pay(request):
	# 生成订单 & 支付宝支付
	# 方法1 需要对提交的数据再次做校验
	# 方法1 使用redis保存30分钟订单
	conn = get_redis_connection()
	key = f'payment_{request.tracer.user.phone}'
	context_string = conn.get(key)
	if not context_string:
		return redirect('price')
	context = json.loads(context_string.decode('utf-8'))

	# 1. 数据库中生成交易记录（待支付） ——等支付成功后需要更新订单的支付状态与写入可使用时间
	order_id = uid(request.tracer.user.phone)
	total_price = context['total_price']
	models.Transaction.objects.create(
		status=1,
		order=order_id,
		user=request.tracer.user,
		price_policy_id=context['policy_id'],
		count=context['number'],
		price=total_price,
	)
	# 2. 跳转到支付宝
	# - 根据申请的支付信息 + 支付宝文档 => 跳转链接
	# - 生成一个支付的链接
	# 构造字典
	params = {
		'app_id': "2021000116681915",
		'method': "alipay.trade.page.pay",
		'format': "JSON",
		'return_url': "http://127.0.0.1:8000/pay/notify/",
		'notify_url': "http://127.0.0.1:8000/pay/notify/",  # 非必选 但推荐必选设置。
		'charset': "utf-8",
		'sign_type': "RSA2",
		'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
		'version': "1.0",
		'biz_content': json.dumps({
			'out_trade_no': order_id,  # 订单号
			'product_code': "FAST_INSTANT_TRADE_PAY",  # 销售产品码，与支付宝签约的产品码名称。
			'total_amount': total_price,  # 订单总金额，单位为元，精确到小数点后两位，取值范围[0.01, 100000000]。
			'subject': "tracer payment",  # 订单标题
		}, separators=(',', ':'))

	}

	# 获取待签名的字符串
	unsigned_string = "&".join([f"{k}={params[k]}" for k in sorted(params)])
	print(unsigned_string)

	# 签名 SHA256WithRSA(对应sign_type为RSA2)
	from Crypto.PublicKey import RSA
	from Crypto.Signature import PKCS1_v1_5
	from Crypto.Hash import SHA256
	from base64 import decodebytes, encodebytes

	# SHA256WithRSA + 应用私钥 对待签名的字符串进行签名
	private_key = RSA.importKey(open("files/sdk/应用私钥2048.txt").read())
	signer = PKCS1_v1_5.new(private_key)
	signature = signer.sign(SHA256.new(unsigned_string.encode('utf8')))

	# 对签名进行base64 编码 转换为字符串
	sign_string = encodebytes(signature).decode('utf-8').replace('\n', '')

	# 把生成的签名赋值给sign参数，拼接到请求参数中。
	from urllib.parse import quote_plus
	result = "&".join([f"{k}={quote_plus(params[k])}" for k in sorted(params)])
	result = result + "&sign=" + quote_plus(sign_string)

	gateway = "https://openapi.alipaydev.com/gateway.do"
	ali_pay_url = f"{gateway}?{result}"
	# - 跳转到这个链接
	return redirect(ali_pay_url)
"""

def pay(request):
	# 生成订单 & 支付宝支付
	# 方法1 需要对提交的数据再次做校验
	# 方法1 使用redis保存30分钟订单
	conn = get_redis_connection()
	key = f'payment_{request.tracer.user.phone}'
	context_string = conn.get(key)
	if not context_string:
		return redirect('price')
	context = json.loads(context_string.decode('utf-8'))

	# 1. 数据库中生成交易记录（待支付） ——等支付成功后需要更新订单的支付状态与写入可使用时间
	order_id = uid(request.tracer.user.phone)
	total_price = context['total_price']
	models.Transaction.objects.create(
		status=1,
		order=order_id,
		user=request.tracer.user,
		price_policy_id=context['policy_id'],
		count=context['number'],
		price=total_price,
	)
	# 2. 跳转到支付宝
	# - 根据申请的支付信息 + 支付宝文档 => 跳转链接
	# - 生成一个支付的链接
	# 构造字典
	params = {
		'app_id': "2021000116681915",
		'method': "alipay.trade.page.pay",
		'format': "JSON",
		'return_url': "http://127.0.0.1:8000/pay/notify/",
		'notify_url': "http://127.0.0.1:8000/pay/notify/",  # 非必选 但推荐必选设置。
		'charset': "utf-8",
		'sign_type': "RSA2",
		'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
		'version': "1.0",
		'biz_content': json.dumps({
			'out_trade_no': order_id,  # 订单号
			'product_code': "FAST_INSTANT_TRADE_PAY",  # 销售产品码，与支付宝签约的产品码名称。
			'total_amount': total_price,  # 订单总金额，单位为元，精确到小数点后两位，取值范围[0.01, 100000000]。
			'subject': "tracer payment",  # 订单标题
		}, separators=(',', ':'))

	}