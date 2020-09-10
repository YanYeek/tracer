#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: cos.py
@time: 2020/9/9 20:25
@desc:
'''
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from django.conf import settings
import sys


def create_bucket(bucket, region='ap-chengdu'):
	"""
	创建桶
	:param bucket：桶名称
	:param region: 区域
	:return:
	"""
	config = CosConfig(Region=region, SecretId=settings.TENCENT_SECRET_ID, SecretKey=settings.TENCENT_SECRET_KEY)
	# 2. 获取客户端对象
	client = CosS3Client(config)
	# 参照下文的描述。或者参照 Demo 程序，详见 https://github.com/tencentyun/cos-python-sdk-v5/blob/master/qcloud_cos/demo.py

	client.create_bucket(
		Bucket=bucket,
		ACL="public-read"  # private / public-read /public-read-write
	)


def upload_file(bucket, region, file_object, key):
	"""
	上传图片到cos桶
	:param bucket:桶名称
	:param region: 区域
	:param file_object:图片对象
	:param key: 图片名字
	:return:
	"""
	config = CosConfig(Region=region, SecretId=settings.TENCENT_SECRET_ID, SecretKey=settings.TENCENT_SECRET_KEY)
	client = CosS3Client(config)
	response = client.upload_file_from_buffer(
		Bucket=bucket,
		Key=key,  # 上传到桶之后的名字
		Body=file_object  # 文件对象
	)
	# https://picture-1302428193.cos.ap-chengdu.myqcloud.com/elephant.jpg
	return "https://{}.cos.{}.myqcloud.com/{}".format(bucket, region, key)
