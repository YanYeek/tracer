#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: dashboard.py
@time: 2020/9/16 20:40
@desc:
'''
from django.template import Library

register = Library()


@register.simple_tag
def use_space(size):
	if size > 1024 * 1024 * 1024:
		return "%.2f GB" % (size / (1024 * 1024 * 1024))
	elif size >= 1024 * 1024:
		return "%.2f MB" % (size / (1024 * 1024))
	elif size >= 1024:
		return "%d KB" % (size / 1024)
	return "%d B" % size
