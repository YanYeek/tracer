# 项目概述：Bug追踪&任务管理追踪

> # **SaaS**——软件即服务(Software as a Service)



![image-20200830162127236](https://raw.githubusercontent.com/YanYeek/FigureBed/master/images/image-20200830162127236.png)

------

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

### 特别注意：企业做项目开发 必须使用环境隔离

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

# day03 用户认证

## 内容回顾&补充

- 虚拟环境 virtualenv（为每个环境创建独立虚拟环境）

- requirements.txt（pip freeze > requirements.txt）

- local_settings.py 

- .gitignore

- 腾讯云短信/阿里云短信 （阅读文档，文档不清晰：谷歌、必应、搜狗都比百度强）

	- API，提供URL，去访问这些URL并根据提示传参数。（所有第三方工具都有）

		```python
		requests.get("http://www.xx.com/sdf/sdf", json={.....})
		```

	- SDK，模块；下载安装模块，基于模块完成功能。

	```python
	sms.py
		def func():
			return requests.get("http://www.xx.com/sdf/sdf", json={.....})
	```

	```
	pip install sms
	```

	```python
	sms.func()
	```

- Redis,帮助我们在内存中存储数据的软件（基于内存的数据库）

	- 第一步：在A主机安装redis&配置&启动

	- 第二步：连接redis

		- 方式一：利用redis提供的客户端。

		- 方式二：利用相关模块。

			- 安装模块

				```python
				pip isstall redis
				```

			- 使用模块(不推荐)

				```python
				import redis
				
				conn = redis,Redis(host='127.0.0.1', port=6379, password='foobared', encoding='uft-8')
				
				conn.set('13111111111', 9999, ex=10)
				value = conn.get('13111111111')
				print(value)
				```

			- 使用模块（推荐连接池）

				```python
				import redis
				# 创建redis连接池（默认连接池最大连接数 2**31=2147483648）
				pool = redis.ConnectionPool(host='10.211.55.28', port=6379, password='foobared', encoding='utf-8', max_connections=1000)
				# 去连接池中获取一个连接
				conn = redis.Redis(connection_pool=pool)
				# 设置键值：15131255089="9999" 且超时时间为10秒（值写入到redis时会自动转字符串）
				conn.set('name', "武沛齐", ex=10)
				# 根据键获取值：如果存在获取值（获取到的是字节类型）；不存在则返回None
				value = conn.get('name')
				print(value)
				```

- django-redis, 在django中”方便“的使用redis。

  ```
  不方便：redis模块+连接池
  方便：django-redis
  ```

  - 安装: ` django-redis`

  	```
  	pip install django-reids
  	```

  - 使用

  	```python
  	# 配置文件 settings.py (建议loacl_settings.py)
  	CACHES = {
  	    "default": {
  	        "BACKEND": "django_redis.cache.RedisCache",
  	        "LOCATION": "redis://10.211.55.28:6379", # 安装redis的主机的 IP 和 端口
  	        "OPTIONS": {
  	            "CLIENT_CLASS": "django_redis.client.DefaultClient",
  	            "CONNECTION_POOL_KWARGS": {
  	                "max_connections": 1000,
  	                "encoding": 'utf-8'
  	            },
  	            "PASSWORD": "foobared" # redis密码
  	        }
  	    }
  	}
  	```

  	```python
  	from django.shortcuts import HttpResponse
  	from django_redis import get_redis_connection
  	def index(request):
  	    # 去连接池中获取一个连接
  	    conn = get_redis_connection("default")
  	    conn.set('nickname', "YanYeek", ex=10)
  	    value = conn.get('nickname')
  	    print(value)
  	    return HttpResponse("OK")
  	```

  	

  	

## 今日概要

- 注册
- 短信验证码登录
- 用户名密码登录



## 今日详细

### 1.实现注册



#### 1.1 展示注册页面



##### 1.1.1 创建web的应用

- django渲染template顺序为先根目录下，次之是按app注册顺序下的模板文件夹，当遇到不同app的同名时渲染顺序会出错，所以在各app的templates目录下再创建同app名的子级文件夹嵌套来避免冲突；如公共模板就放在根目录文件夹下。static静态文件目录也同理。

![image-20200904124544228](https://raw.githubusercontent.com/YanYeek/FigureBed/master/images/image-20200904124544228.png)

##### 1.1.2 下载静态文件

1. https://blog.jquery.com/2019/05/01/jquery-3-4-1-triggering-focus-events-in-ie-and-finding-root-elements-in-ios-10/
2. https://v3.bootcss.com/getting-started/#download
3. https://fontawesome.dashgame.com/

##### 1.1.3 母版准备

![image-20200904131838890](https://raw.githubusercontent.com/YanYeek/FigureBed/master/images/image-20200904131838890.png)





##### 1.1.4 URL准备

![image-20200904142346822](https://raw.githubusercontent.com/YanYeek/FigureBed/master/images/image-20200904142346822.png)



![image-20200904142409649](https://raw.githubusercontent.com/YanYeek/FigureBed/master/images/image-20200904142409649.png)

commit：路由处理

##### 1.1.5注册页面显示

- 母版中导航
- 注册页面样式
- ModelForm放到指定目录forms



#### 1.2 点击获取验证码

![image-20200904143143877](https://raw.githubusercontent.com/YanYeek/FigureBed/master/images/image-20200904143143877.png)

##### 1.2.1 按钮绑定点击事件



##### 1.2.2 获取手机号



##### 1.2.3 发送ajax



##### 1.2.4 手机号校验

- 不能为空
- 格式正确
- 没有注册过



##### 1.2.5 验证通过

- 发送短信
- 将短信保存到redis中（60s）





##### 1.2.6 成功失败处理

- 失败，错误信息
- 成功，倒计时



#### 1.3 点击注册











