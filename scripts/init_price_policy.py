#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: init_price_policy.py
@time: 2020/9/7 1:32
@desc:
'''
import offline_scripts_base

from web import models


def run():
	exists = models.PricePolicy.objects.filter(category=1, title='个人免费版', ).exists()
	if not exists:
		models.PricePolicy.objects.create(
			category=1,
			title='个人免费版',
			price=0,
			project_num=3,
			project_member=2,
			project_space=20,
			project_size=5,
		)


if __name__ == '__main__':
	run()
