#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: bootstrap.py
@time: 2020/9/7 15:40
@desc:
'''


class BootStrapForm(object):
	bootstrap_class_exclude = []

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for name, field in self.fields.items():
			if name in self.bootstrap_class_exclude:
				continue
			field.widget.attrs['class'] = 'form-control'
			field.widget.attrs['placeholder'] = '请输入%s' % (field.label,)
