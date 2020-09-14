#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: issues.py
@time: 2020/9/14 21:47
@desc:
'''
from django.shortcuts import render

from web.forms.issues import IssuesModalForm


def issues(request, project_id):
	if request.method == "GET":
		form = IssuesModalForm()
		return render(request, 'issues.html', {'form': form})
