#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: cos_bucket_demo.py
@time: 2020/9/10 14:43
@desc:
'''
# !/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: cos_upload_demo.py
@time: 2020/9/9 16:16
@desc:
'''
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from django.conf import settings

secret_id = settings.TENCENT_SECRET_ID  # 替换为用户的 secretId
secret_key = settings.TENCENT_SECRET_KEY  # 替换为用户的 secretKey

region = 'ap-chengdu'  # 替换为用户的 Region

config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
client = CosS3Client(config)

response = client.create_bucket(
	Bucket='picture-1302428193',
	ACL="public-read"  # private / public-read /public-read-write
)
