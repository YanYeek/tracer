#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: access_web.py
@time: 2020/9/14 18:11
@desc:
'''
import requests

res = requests.get(
	'https://18108817986-1599911933-1302428193.cos.ap-chengdu.myqcloud.com/1600078162960_%E5%8D%83%E5%8F%8D%E7%94%B0.jpg')

print(res.content)
