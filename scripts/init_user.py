#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: init_user.py
@time: 2020/9/5 22:34
@desc:
'''
import django
import os
import sys

base_dir = os.path.dirname((os.path.dirname(os.path.abspath(__file__))))
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saas.settings")
django.setup()  # os.environ.['DJANGO_SETTINGS_MODULE']

from web import models

# 往数据库添加数据：连接数据库、操作、关闭连接
models.UserInfo.objects.create(username='Yan', email='yan@qq.com', phone='13111111111', password='11111111')
