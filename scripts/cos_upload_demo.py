#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: cos_upload_demo.py
@time: 2020/9/9 16:16
@desc:
'''
from scripts import offline_scripts_base
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from django.conf import settings

secret_id = settings.TENCENT_SECRET_ID  # 替换为用户的 secretId
secret_key = settings.TENCENT_SECRET_KEY  # 替换为用户的 secretKey
region = 'ap-chengdu'  # 替换为用户的 Region

config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
# 2. 获取客户端对象
client = CosS3Client(config)
# 参照下文的描述。或者参照 Demo 程序，详见 https://github.com/tencentyun/cos-python-sdk-v5/blob/master/qcloud_cos/demo.py

response = client.upload_file(
	Bucket='picture-1302428193',
	LocalFilePath='picture.jpg',  # 本地文件路径
	Key='elephant.jpg',  # 上传到桶之后的名字
)
print(response['ETag'])
