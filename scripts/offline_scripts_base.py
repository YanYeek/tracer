#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: offline_scripts_base.py
@time: 2020/9/7 1:41
@desc:
'''
import django
import os
import sys

base_dir = os.path.dirname((os.path.dirname(os.path.abspath(__file__))))
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saas.settings")
django.setup()  # os.environ.['DJANGO_SETTINGS_MODULE']
