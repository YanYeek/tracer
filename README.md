# 项目概述——**SaaS**：软件即服务(Software as a Service)



![image-20200830162127236](https://raw.githubusercontent.com/YanYeek/FigureBed/master/images/image-20200830162127236.png)

> bug追踪&任务管理追踪

## 1. 如何学&如何讲

- 讲
	- 拆解知识点
	- 给大家分配任务：去完成某个功能
	- 讲解
- 学(企业工作)
	- 守规则 (讲课、公司)
	- 主要任务：写代码
	- 实事求是

## 2. 涉及知识点

- 虚拟环境，电脑上创建多个python环境。

	```
	py3:
	    - django 1.11版本 -> crm [维护]
	    - django 2.2 版本 -> 路飞 [新开发]
	虚拟环境：
		自己电脑上都有py3
		- 虚拟1：py3 纯净 django1.11
		- 虚拟2：py3 纯净 django2.0
	```

- local_settings.py本地配置

	```
	开发人员：
		连接数据库需要在django的setting中设置，链接数据库IP：1.1.1.1
	测试人员：
		连接数据库需要在django的setting中设置，链接数据库IP：1.1.1.2
	```

	```python
	# settings.py 开发测试独立配置不共享
	try:
	    from .local_settings import *
	   excepet ImportError:
	    pass
	```

- 腾讯云平台(免费)

	- sms短信，申请服务。
	
	- cos对象存储，腾讯给了云硬盘，项目中上传文件/查看文件/下载文件——都去腾讯云中。
	
		```
		慢，快。
		```
	
- redis

	```
	mysql：
		自己的电脑————        另外的电脑	   		(硬盘文件操作)
		pymysql模块   ->  Mysql软件 -> 行为：cearte table 创建表
										insert into 表插入
	redis：
		自己的电脑————        另外的电脑	   		(内存操作)
		redis模块   ->  		redis软件 -> 行为：set name="YanYeek"
		                                      get name
		                                      超时时间 10秒后过期
	# 注意：1台电脑也可以操作
	```

## 3. 项目开发

- 一期：用户认证（短信验证、图片验证码、django ModelForm）-3天
- 二期：wiki、文件、问题管理 - 5~7天
- 三期：支付、部署（周末linux基础）-2天 

# day01 前戏

## 今日概要

- 虚拟环境（项目环境
- 项目框架：local_settings
- git实战应用
- 通过python & 腾讯sms发送短信

## 今日详细

### 1.虚拟环境 virtualenv

#### 1.1

```
pip install virtualenv
```

#### 1.2

```
virtualenv 环境名字
#注意：创建 [环境名称] 问价夹，放置所有的环境。
```

```
假设：目前电脑 py27 / py36
virtualenv 环境名字 --python="C:\python\python3.6.exe"
virtualenv 环境名字 --python=python2.7
```

```
1. 打开终端
2. 安装：virtualenv
	pip install virtualenv
3. 终端关闭，在重新打开
4. 通过命令进入指定目录
	win：
		>>>D:
		>>>cd envs
	mac:
		...
5. 创建虚拟环境
	virtualenv saas
```

#### 1.3 激活、退出虚拟环境

```
win：
	>>> cd Scripts 进入虚拟环境 Scripts目录
	>>> activate.exe 激活虚拟环境
```

#### 补充

- py3.7+django1.11.7创建项目报错

	![image-20200830181323928](https://raw.githubusercontent.com/YanYeek/FigureBed/master/images/image-20200830181323928.png)



解决思路：安装django1.11.28

```python
pip install django==1.11.28
```

#### 1.4在虚拟环境中安装模块

注意：激活虚拟环境再执行pip install django==1.11.28

### 2.搭建项目环境（django+虚拟环境）

### 警醒：企业做项目开发 必须使用环境隔离

### 3.本地配置

local_settings.py

#### 3.1 在settings中导入

```python
try:
    from .local_settings import *
except ImportError:
    pass
```

#### 3.2创建自己的local_settings.py文件

```python
#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: local_settings.py
@time: 2020/8/30 19:00
@desc:
'''
LANGUAGE_CODE = 'zh-hans'

SMS = 666
```

给别人代码时，切记不给local_settings.py本地配置文件

### 4.给别人代码

#### 4.1创建一个远程仓库

- 让git忽略文件 .gitignore

```
# pycharm
.idea/
.DS_Store

__pycache__/
*.py[cod]
*$py.class

# Django stuff:
local_settings.py
*.sqlite3


# database migrations
*/migrations/*.py
!*/migrations/__init__.py
```

- git管理项目

```
(saas) C:\Users\YanYeek\Documents\SC\saas>git commit -m "第一次提交"
[master (root-commit) fa81a6b] 第一次提交
 6 files changed, 204 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 manage.py
 create mode 100644 saas/__init__.py
 create mode 100644 saas/settings.py
 create mode 100644 saas/urls.py
 create mode 100644 saas/wsgi.py
```

#### 4.2将本地项目推送到远程仓库

```bash
(saas) C:\Users\YanYeek\Documents\SC\saas>$ git remote add origin https://gitee.com/YanYeek/SaaS.git

(saas) C:\Users\YanYeek\Documents\SC\saas>$ git push -u origin master
Enumerating objects: 9, done.
Counting objects: 100% (9/9), done.
Delta compression using up to 4 threads
Compressing objects: 100% (8/8), done.
Writing objects: 100% (9/9), 2.87 KiB | 1.43 MiB/s, done.
Total 9 (delta 0), reused 0 (delta 0), pack-reused 0
remote: Powered by GITEE.COM [GNK-5.0]
To https://gitee.com/YanYeek/SaaS.git
 * [new branch]      master -> master
Branch 'master' set up to track remote branch 'master' from 'origin'.

#You can override any checks that git does by using "force push". Use this command in terminal
$ git push -f origin master
```

#### 4.2测试获取代码

https://gitee.com/YanYeek/SaaS.git

```
进入自己想要放置代码的目录
git clone https://gitee.com/YanYeek/SaaS.git
```

## 今天作业

- 虚拟环境
- 创建django项目
- git 仓库
- 写文档
	- 知识点
	- git地址



# day02

## 内容回顾：

1. local_settings的作用？

  - 满足本地不同需求的配置

    	 - 开发
    	 - 测试
      	 - 运维

2. .gitignore的作用？

- git软件，本地进行版本管理。
	- git init
	- git add
	- git commit
	- git push

- 码云/GitHub/gitlab，代码托管。

3. 虚拟环境的作用？

~~~
项目之间环境隔离。
开发：本地环境
线上：多环境隔离
~~~

~~~
# 将当前环境的模块信息保存
pip freeze > requirements.txt
# 根据依赖信息安装模块
pip install -r requirements.txt
~~~

## 今日概要：

- 腾讯发送短信
- Django的ModelForm组件
- redis
- 注册逻辑设计
- 开发
- 讲解

## 今日详细：

### 1.腾讯发短信

- 注册
- 登录

[注册腾讯云 & 开通云短信](https://www.pythonav.com/wiki/detail/10/81/)



### 2.Django的ModelForm

- 自动生成表单
- 做表单验证

### 3.下一步思路

- 点击获取验证码
	- 获取手机号
	- 向后台发送ajax
		- 手机
		- tpl=register
	- 向手机发送验证码（ajax/sms/redis）
	- 验证码失效处理 60s

### 4.redis基本操作

#### 4.1 安装redis

- Windows

- Linux

#### 4.2 python操作redis的模块

- redis的直接连接

[安装操作文档](https://www.pythonav.com/wiki/detail/10/82/)

## 作业

- ModelForm页面
- register页面写ajax，手机号和模板字符串tpl csrf问题
- 校验
- sms + redis
- 进阶
	- 倒计时效果
	- 注册按钮：字段验证+手机号验证码
	- py操作redis：使用django-redis模块

















