from django.shortcuts import render,HttpResponse

# Create your views here.
import random
from utils.tencent.sms import send_sms_single


def send_sms(requests):
	"""
	发送短信
	:param requests:
	:return:
	"""
	code = random.randrange(1000,9999)
	res = send_sms_single("18108817986", 635855, [code,])
	print(res)
	return HttpResponse('成功')
