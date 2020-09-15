#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: issues.py
@time: 2020/9/15 12:44
@desc:
'''
from django.template import Library
from web import models
from django.shortcuts import reverse

register = Library()


@register.simple_tag
def string_just(num):
	if num < 100:
		f_num = f"{str(num).rjust(3, '0')}"
		return f'#{f_num}'
	return num
