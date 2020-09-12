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
		ACL="public-read",  # private / public-read /public-read-write
	)
	# 配置跨域设置
	cors_config = {
		'CORSRule': [
			{
				'AllowedOrigin': '*',
				'AllowedMethod': ['GET', 'PUT', 'HEAD', 'POST', 'DELETE'],
				'AllowedHeader': '*',
				'ExposeHeader': '*',
				'MaxAgeSeconds': 500,
			}
		],
	}
	client.put_bucket_cors(
		Bucket=bucket,
		CORSConfiguration=cors_config,
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


def delete_file(bucket, region, key):
	"""
	删除cos中的文件
	:param bucket:桶名称
	:param region: 区域
	:param key: 图片名字
	:return:
	"""
	config = CosConfig(Region=region, SecretId=settings.TENCENT_SECRET_ID, SecretKey=settings.TENCENT_SECRET_KEY)
	client = CosS3Client(config)
	client.delete_object(
		Bucket=bucket,
		Key=key,  # 上传到桶之后的名字
	)


def delete_file_list(bucket, region, key_list):
	"""
	删除cos中的文件
	:param bucket:桶名称
	:param region: 区域
	:param key: 图片名字
	:return:
	"""
	config = CosConfig(Region=region, SecretId=settings.TENCENT_SECRET_ID, SecretKey=settings.TENCENT_SECRET_KEY)
	client = CosS3Client(config)
	objects = {
		"Quiet": "true",
		"Object": key_list
	}
	client.delete_objects(
		Bucket=bucket,
		Key=objects,  # 上传到桶之后的名字
	)


def credential(bucket, region):
	# 生成一个临时凭证,并给前端返回
	# 1. 安装一个SDK pip isntall -U qcloud-python-sts
	# 2. 写代码
	from sts.sts import Sts
	config = {
		# 临时密钥有效期,单位秒,(30分钟=1800秒)
		'duration_seconds': 1800,
		# 固定密钥 id
		'secret_id': settings.TENCENT_SECRET_ID,
		# 固定密钥 key
		'secret_key': settings.TENCENT_SECRET_KEY,
		# 桶名称
		'bucket': bucket,
		# 桶所在地区
		'region': region,
		# 允许的文件前缀
		'allow_prefix': '*',
		# 密钥权限列表
		'allow_actions': [
			'name/cos:PostObject',
			# '*' # 代表所有权限都可以
		],
	}
	sts = Sts(config)
	result_dict = sts.get_credential()
	return result_dict
