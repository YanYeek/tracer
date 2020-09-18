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
	# exists = models.PricePolicy.objects.filter(category=1, title='个人免费版', ).exists()
	models.PricePolicy.objects.create(
		category=2,
		title='VIP',
		price=100,
		project_num=50,
		project_member=10,
		project_space=10,
		project_size=500,
	)
	models.PricePolicy.objects.create(
		category=2,
		title='SVIP',
		price=200,
		project_num=150,
		project_member=110,
		project_space=110,
		project_size=1024,
	)
	models.PricePolicy.objects.create(
		category=2,
		title='SSVIP',
		price=500,
		project_num=550,
		project_member=510,
		project_space=510,
		project_size=2048,
	)


if __name__ == '__main__':
	run()
