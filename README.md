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

修改origin推送链接`git remote set-url origin https://gitee.com/YanYeek/Tracer.git`

#### 4.2测试获取代码

https://gitee.com/YanYeek/SaaS.git

```
进入自己想要放置代码的目录
git clone https://gitee.com/YanYeek/SaaS.git
# 将当前环境的模块信息保存
pip freeze > requirements.txt
# 根据依赖信息安装模块
pip install -r requirements.txt
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

	- disabled属性

		```
		$("#btnSms").prop("disabled", ture); 添加disabled属性，不可操作。
		$("#btnSms").prop("disabled", false); 移除disabled属性，可操作。
		```

	- 定时器

		```javascript
		var obj = setInterval(function(){
			console.log(123);
		}, 1000)
		
		clearInterval(obj);
		```

		```javascript
		var time = 60;
		var obj = setInterval(function(){
			time = time - 1;
			if(time < 1){
		     	clearInterval(obj);	            
		     }
		}, 1000)
		```

		

		







## 内容总结

- 视图 view.py -> views目录

- 模板，根目录templates -> 个人那句app注册顺序去每个app的templates中载入

- 静态文件，static同上载入规则

- 项目中多个app且想要各自模板、静态文件隔离，建议通过app名称再进行嵌套即可。

- 路由分发

	- include
	- namespace

- 母版

	```
	title
	css
	content
	js
	```

- bootstrap导航条、去除圆角、container

- ModelForm生成HTML标签，自动ID`id_字段名`

- 发送Ajax请求

	```js
	$.ajax({
	    url:'/index/',
	    type:'GET',
	    data:{},
	    dataType:"JSON",
	    sucess: function(res){
	        console.log(res)
	    }
	})
	```

- Form & ModelForm可以进行表单校验

	```
	form = sendSmsForm(data=request.POST) # QueryDict
	form = sendSmsForm(data=request.GET) # QueryDict
	```

- From & ModelForm 中如果想要用视图函数中的值（request）

	```python
	class SendSmsForm(forms.Form):
		phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])
	
		# 重写初始化函数来获取试图函数中的传值
		def __init__(self, request, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.request = request
	```

- 短信
- redis（django-redis）
- 倒计时



## 今日作业

- 点击注册按钮
- 短信登录
- Django实现图片验证码（可选）





# day04



## 内容回顾

- 项目规则

	- 创建项目：静态、视图、路由

- Ajax

	```javascript
	$.ajax({
		url:'...',
	    type: "GET",
	    data: {},
	    dataType: "JSON",
	    success: function(res){
	        
	    }
	})
	
	$.ajax({
	    url: "{% url 'register' %}",
	    type: "POST",
	    data: $('#regForm').serialize(),
	    dataType: "JSON",
	    success: function (res) {
	        console.log(res);
	    }
	})
	```

- ModelForm/Form 中想要使用视图中的数据，例如：request

	```
	重写ModelForm/Form的__init__方法，把想要的数据传递，再继承原init方法。
	```

- django-redis



## 今日概要

- 点击注册
- 用户登录
	- 短信验证码登录
	- 手机or邮箱 / 密码登录
- 项目管理（创建&星标）





## 今日详细

### 1. 点击注册

#### 1.1 点击收集数据&Ajax

```javascript
function bindClickSubmit() {
    $('#btnSubmit').click(function () {
        // 收集表单中的数据（找到每一个字段）
        // 包含所以字段的数据 + csrf token

        // 数据Ajax发送到后台
        $.ajax({
            url: "{% url 'register' %}",
            type: "POST",
            data: $('#regForm').serialize(),
            dataType: "JSON",
            success: function (res) {
                console.log(res);
            }
        })
    })
}
```





#### 1.2 数据校验（每个字段）

test

**!字典用get方法取值提高健壮性，[‘key’]方式获取不到或报错**

```python
class RegisterModelForm(forms.ModelForm):
	password = forms.CharField(label='密码',
	                           min_length=8,
	                           max_length=64,
	                           error_messages={
		                           'min_length': "密码长度不能少于8个字符",
		                           'max_length': "密码长度不能多于64个字符",
	                           },
	                           widget=forms.PasswordInput(),
	                           )

	confirm_password = forms.CharField(label='重复密码', widget=forms.PasswordInput(
	))
	phone = forms.CharField(label='手机号',
	                        validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ],
	                        widget=forms.TextInput(),
	                        )

	code = forms.CharField(label='验证码',
	                       widget=forms.TextInput())

	class Meta:
		model = models.UserInfo
		# 钩子函数校验顺序与下方列表一致，字段定义顺序也要统一，否则校验时cleaned_data获取不到值。
		fields = ['username', 'email', 'password', 'confirm_password', 'phone', 'code']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'
			field.widget.attrs['placeholder'] = '请输入%s' % (field.label,)

	def clean_username(self):
		username = self.cleaned_data.get('username')
		exists = models.UserInfo.objects.filter(username=username).exists()
		if exists:
			raise ValidationError('用户名已存在')
		return username

	def clean_email(self):
		email = self.cleaned_data.get('email')
		exists = models.UserInfo.objects.filter(username=email).exists()
		if exists:
			raise ValidationError('邮箱已存在')
		return email

	def clean_password(self):
		pwd = self.cleaned_data.get('password')
		# 加密 & 返回
		return encrypt.md5(pwd)

	def clean_confirm_password(self):
		pwd = self.cleaned_data.get('password')
		confirm_pwd = encrypt.md5(self.cleaned_data.get('confirm_password'))
		if pwd != confirm_pwd:
			raise ValidationError('两次密码不一致')
		return confirm_pwd

	def clean_phone(self):
		phone = self.cleaned_data.get('phone')
		exists = models.UserInfo.objects.filter(phone=phone).exists()
		if exists:
			raise ValidationError('手机号已注册')
		return phone

	def clean_code(self):
		code = self.cleaned_data.get('code')
		phone = self.cleaned_data.get('phone')
		conn = get_redis_connection()
		redis_code = conn.get(str(phone))
		if not redis_code:
			raise ValidationError('验证码失效或未发生，请重新发送')

		redis_str_code = redis_code.decode('utf-8')
		if code.strip() != redis_str_code:
			raise ValidationError('验证码错误，请重新输入')

		return code
```



#### 1.3 写入数据库

```python
def register(request):
	"""
	注册页面
	:param requests:
	:return:
	"""
	if request.method == "GET":
		form = RegisterModelForm()
		return render(request, 'register.html', {'form': form})
	form = RegisterModelForm(data=request.POST)
	if form.is_valid():
		# 验证通过，写入数据库（密码要是密文）
		# instance = models.UserInfo.objects.create(**form.cleaned_data) # 此方法包含无用数据段，需要手动剔除。
		form.save()  # 此方法可自动剔除无用数据。此函数可返回刚刚创建数据一个对象instance
		return JsonResponse({'status': True, 'data': '/login/'})

	return JsonResponse({'status': False, 'error': form.errors})
```





### 2. 短信登录

#### 2.1 展示页面

![image-20200905193217427](https://raw.githubusercontent.com/YanYeek/FigureBed/master/images/image-20200905193217427.png)



#### 2.2 点击发送短信

![image-20200905193236448](https://raw.githubusercontent.com/YanYeek/FigureBed/master/images/image-20200905193236448.png)



#### 2.3 点击登录



### 3. 用户名/密码登录



#### 3.1 Python生成图片+写文字

https://www.cnblogs.com/wupeiqi/articles/5812291.html

```py
pip install pillow
```



#### 3.2 Session & Cookie

`django默认session超时时间为2周，但可以修改。`

![image-20200905201313639](https://raw.githubusercontent.com/YanYeek/FigureBed/master/images/image-20200905201313639.png)

#### 3.3 页面展示



#### 3.4登录

## 总结（一期项目结束）

- 项目代码
- 思维导图





# day05

## 今日概要

- django写离线脚本
- 探讨业务
- 设计表结构
- 参考表结构【任务】
	- 查看项目列表
	- 创建项目
	- 星标项目



## 今日详细

### 1.django离线脚本

```
django框架
离线，非web运行时。
脚本，一个或几个py文件。
```

再某个py文件中对django项目做一些处理。

#### 示例1：使用离线脚本在用户表插入数据

```python
#!/usr/bin/env python
# encoding: utf-8
'''
@author: YanYeek
@file: init_user.py
@time: 2020/9/5 22:34
@desc:
'''
import django
import os
import sys

base_dir = os.path.dirname((os.path.dirname(os.path.abspath(__file__))))
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saas.settings")
django.setup()  # os.environ.['DJANGO_SETTINGS_MODULE']

from web import models

# 往数据库添加数据：连接数据库、操作、关闭连接
models.UserInfo.objects.create(username='Yan', email='yan@qq.com', phone='13111111111', password='11111111')

```

#### 示例2：数据库录入全国省市县



#### 示例3：朋友圈项目敏感字、词语



#### 示例4：SaaS免费版：1G、5项目、10人。





### 2.探讨业务

#### 2.1 价格策略

| ID   |  分类  |    标题    | 价格/年 | 项目个数 | 项目成员 | 项目空间 | 单文件 | 创建时间 |
| ---- | :----: | :--------: | :-----: | :------: | :------: | :------: | :----: | :------: |
| 1    | 免费版 | 个人免费版 |    0    |    3     |    2     |   20M    |   5M   |          |
| 2    | 收费版 |    VIP     |   199   |    20    |   100    |   50G    |  500M  |          |
| 3    | 企业版 |    SVIP    |   299   |    50    |   200    |   100G   |   1G   |          |
| 4    |  其他  |            |         |          |          |          |        |          |

注意：新用户注册拥有免费版的额度。



#### 2.2 用户

| ID   | 用户名  | 手机号         | 密码  |      |
| ---- | ------- | -------------- | ----- | ---- |
| 1    | YanYeek | 18888888888888 | sdf   |      |
| 2    | 阿尔法  | 18888888888888 | ssg   |      |
| 3    | 北塔    | 18888888888888 | sdfsd |      |



#### 2.3 交易

| ID   | 状态          | 用户 | 价格策略 | 实际支付 | 开始      | 结束      | 数量（年） | 订单号       |
| ---- | ------------- | ---- | -------- | -------- | --------- | --------- | ---------- | ------------ |
| 1    | 已支付        | 1    | 1        | 0        | 2020-9-6  | null      | 0          | asefasfga321 |
| 2    | 已支付        | 1    | 1        | 0        | 2020-9-6  | null      | 0          | asefasfga323 |
| 3    | 已支付        | 1    | 1        | 0        | 2020-9-6  | null      | 0          | asefasfga323 |
| 4    | 已支付        | 2    | 2        | 199      | 2020-9-10 | 2021-9-10 | 1          | asefasfga324 |
| 5    | 未支付/已支付 | 3    | 3        | 299*2    | 2020-5-18 | 2020-5-18 | 2          | asefasfga325 |

`request.tracer = 交易对象`



#### 2.4 创建存储

基于腾讯对象存储COS存储数据



#### 2.5 项目

| ID   | 项目名称 | 描述 | 颜色  | 星标  | 参与人数 | 创建者 | 已使用空间 |      |      |
| ---- | -------- | ---- | ----- | ----- | -------- | ------ | ---------- | ---- | ---- |
| 1    | CRM      | …    | #dddd | ture  | 5        | 3      | 5M         |      |      |
| 2    | 路飞学城 | …    | #uuu7 | false | 10       | 3      | 1G         |      |      |
| 3    | SaaS     | …    | #uu97 | false | 20       | 3      | 2G         |      |      |



#### 2.6 项目参与者

| ID   | 项目 | 用户 | 星标  | 邀请者 | 角色 |      |      |      |      |
| ---- | ---- | ---- | ----- | ------ | ---- | ---- | ---- | ---- | ---- |
| 1    | 1    | 1    | true  |        |      |      |      |      |      |
| 2    | 1    | 2    | false |        |      |      |      |      |      |
|      |      |      |       |        |      |      |      |      |      |





### 3.任务

#### 3.1 创建相应表结构



#### 3.2 离线脚本创建价格策略【免费版】

|  分类  |    标题    | 价格/年 | 项目个数 | 项目成员 | 项目空间 | 单文件 | 创建时间 |
| :----: | :--------: | :-----: | :------: | :------: | :------: | :----: | :------: |
| 免费版 | 个人免费版 |    0    |    3     |    2     |   20M    |   5M   |          |



#### 3.3 用户注册【改】

- 之前：操作成功只是新建用户
- 现在：
	- 新建用户
	- 新建交易激励【免费版】

```python

```





#### 3.4 添加项目



#### 3.5 展示项目

- 星标
- 我创建的
- 我参与的



#### 3.6 星标项目



# day06



## 今日概要

- 表结构
- 离线脚本
- 以后注册
- 添加项目
- 展示项目
- 星标项目





## 今日详细

### 1.表结构

### 2.离线脚本

```python
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
```



### 3.用户注册【改】

- 以前：创建用户
- 现在：用户 & 交易记录



### 4.添加项目

#### 4.1 项目列表母版 + 样式

- 后台：登录成功才可以访问
- 官网：无论是否登录都可以访问 
- 通过中间件+白名单 对后台管理的权限 进行处理
- 当前用户所拥有的价格策略【额度】



#### 4.2 添加

任务：选择颜色 查看项目列表 星标

```
modelForm-select -> radio
颜色覆盖
```





# day07

## 今日概要

- 展示项目
- 星标项目
- 添加项目：颜色选择
- 项目切换 & 项目管理菜单处置
- wiki管理



## 今日详细

### 1.展示项目

#### 1.1 数据

![image-20200907174240035](https://raw.githubusercontent.com/YanYeek/FigureBed/master/images/image-20200907174240035.png)

```
1. 从数据库中获取两部分数据
	我创建的所有项目：已星标、未星标
	我参与的所有项目：已星标、未星标
2. 提前已星标
	循环 = 循环[我创建的所有项目] + [我参与的所有项目] 吧已星标的数据提取
	
得到三个列表：星标、创建、参与
```

#### 1.2 样式

```html
<style>
        .project {
            margin-top: 10px;
        }

        .panel-body {
            padding: 0;
            display: flex;
            flex-direction: row;
            justify-content: left;
            align-items: flex-start;
            flex-wrap: wrap;
        }

        .panel-body > .item {
            border-radius: 6px;
            width: 228px;
            border: 1px solid #dddddd;
            margin: 20px 10px;

        }

        .panel-body > .item:hover {
            border: 1px solid #f0ad4e;
        }

        .panel-body > .item > .title {
            height: 104px;
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            font-size: 15px;
            text-decoration: none;
        }

        .panel-body > .item > .info {
            padding: 10px 10px;

            display: flex;
            justify-content: space-between;

            border-bottom-left-radius: 6px;
            border-bottom-right-radius: 6px;
            color: #8c8c8c;

        }

        .panel-body > .item > .info a {
            text-decoration: none;
        }

        .panel-body > .item > .info .fa-star {
            font-size: 18px;
        }

        .color-radio label {
            margin-left: 0;
            padding-left: 0;
        }

        .color-radio input[type="radio"] {
            display: none;
        }

        .color-radio input[type="radio"] + .cycle {
            display: inline-block;
            height: 25px;
            width: 25px;
            border-radius: 50%;
            border: 2px solid #dddddd;
        }

        .color-radio input[type="radio"]:checked + .cycle {
            border: 2px solid black;
        }
    </style>
```



### 2.星标项目（去除星标）



#### 2.1 星标

```
我创建的项目：projectstar = True
我参与的项目：projectUser的star = True
```



#### 2.2 移除星标

```
我创建的项目：projectstar = False
我参与的项目：projectUser的star = False
```





### 3.选择颜色

#### 3.1 部分样式应用BootStrap

```python
class BootStrapForm(object):
	bootstrap_class_exclude = []

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for name, field in self.fields.items():
			if name in self.bootstrap_class_exclude:
				continue
			field.widget.attrs['class'] = 'form-control'
			field.widget.attrs['placeholder'] = '请输入%s' % (field.label,)
```

```python
class ProjectModelForm(BootStrapForm, forms.ModelForm):
	# desc = forms.CharField(widget=forms.Textarea)
	bootstrap_class_exclude = ['color']
    class Meta:
        model = models.Project
        fields = ['name', 'color', 'desc']
        widgets = {
            'desc': forms.Textarea,
            'color': ColorRadioSelect(attrs={"class": "color-radio"}),
        }
```

#### 3.2 定制ModelForm的插件

```python
class ProjectModelForm(BootStrapForm, forms.ModelForm):

	class Meta:
		model = models.Project
		fields = "__all__"
		widgets = {
			'desc': forms.Textarea,
			'color': ColorRadioSelect(attrs={"class": "color-radio"}),
		}
```

```python
from django.forms import RadioSelect


class ColorRadioSelect(RadioSelect):
	# template_name = 'django/forms/widgets/radio.html'
	# option_template_name = 'django/forms/widgets/radio_option.html'

	template_name = 'widgets/color_radio/radio.html'
	option_template_name = 'widgets/color_radio/radio_option.html'
```

```html
{% with id=widget.attrs.id %}
    <div{% if id %} id="{{ id }}"{% endif %}{% if widget.attrs.class %} class="{{ widget.attrs.class }}"{% endif %}>
        {% for group, options, index in widget.optgroups %}
            {% for option in options %}
                <label {% if option.attrs.id %} for="{{ option.attrs.id }}"{% endif %} >
                    {% include option.template_name with widget=option %}
                </label>
            {% endfor %}
        {% endfor %}
    </div>
{% endwith %}
```

```html
{% include "django/forms/widgets/input.html" %}
<span class="cycle" style="background-color:{{ option.label }}"></span>
```



#### 3.3 项目选择颜色

3.1、3.2知识点的应用 + 前端样式的编写



### 4.切换菜单

```
1. 数据库获取
	我创建的：
	我参与的：
2. 循环显示

3. 当前页面需要显示/其他页面也需要显示 [inclusion_tag]
```



### 5.项目管理

![image-20200908112449731](https://raw.githubusercontent.com/YanYeek/FigureBed/master/images/image-20200908112449731.png)





```
/manage/项目ID/dashboared
/manage/项目ID/issues
/manage/项目ID/statistics
/manage/项目ID/file
/manage/项目ID/wiki
/manage/项目ID/setting
```



#### 5.1 进入项目展示菜单



```
- 进入项目
- 展示菜单
```

##### 5.1.1 是否进入项目【中间件】

判断URL是否以manage开头？

project-id 是我创建的 or 我参与的？



##### 5.1.2 显示菜单

依赖：是否已经进入项目？

```html
判断：是否已经进入项目？
<ul class="nav navbar-nav">
    <li><a href="#">概览</a></li>
    <li><a href="#">wiki</a></li>
    <li><a href="#">配置</a></li>
</ul>
```

##### 5.1.3 修复bug

bootstrap样式ul与li嵌套关系错误

##### 5.1.4 默认选择菜单

![image-20200908162114488](https://raw.githubusercontent.com/YanYeek/FigureBed/master/images/image-20200908162114488.png)





## 总结

1. 项目实现思路
2. 星标/取消星标
3. inclusion_tag实现项目切换
4. 3项目菜单
	- 中间件 process_view
	- 默认选中：inclusion_tag
	- 路由分发
		- include(“xxx.url”)
		- include([“xxx.url”, “sdf”, “afaf”])
5. 颜色选择：源码 + 扩展【实现】……



## 作业

<img src="https://raw.githubusercontent.com/YanYeek/FigureBed/master/images/image-20200908141934319.png" alt="image-20200908141934319" style="zoom:50%;" />





# day08 Wiki



## 今日概要

- 表结构设计
- 快速开发
- 应用markdown组件
- 腾讯COS做上传





## 今日详细

### 1.表结构设计

![image-20200908160947851](https://raw.githubusercontent.com/YanYeek/FigureBed/master/images/image-20200908160947851.png)







| ID   | 标题   | 内容           | 项目ID | 父ID | depth |
| ---- | ------ | -------------- | ------ | ---- | ----- |
| 1    | test   | 山豆根发射点发 | 1      | null | 1     |
| 2    | 张家界 | 事故发生规划   | 1      | null | 1     |
| 3    | fh     | 儿童火热拖后腿 | 1      | 1    | 2     |

父ID字段使用自关联，划分归属层级



### 2.快速开发

#### 2.1 wiki首页展示

- 首页：已完成

- 多级目录思路：

	```
	1级：
		找到当前项目的所有文章的name
		页面循环展示
	多级：
		去数据库获取每一级的数据
	```

	```
	模板渲染：
		- 数据库获取数据要有层级的划分
		讲数据构造
		[
			{
				id:1,
				title:'lol',
				children: {
					id:xxx,
					name:'xxxx'
				}
			}
		]
	缺点：
		- 写代码费劲
		- 效率低
	```

	```python
	后端 + 前端完成Ajax+ID选择器
		- 前端：打开页面之后。发送ajax请求获取所有的文档标题信息。
		- 后台：获取所有的文章信息
			queryset = model.wiki.objects.filter(project_id=2).values_list('id','title', 'parent_id')
			[
				{'id':1,'title':'为人体','parent_id': None},
				{'id':2,'title':'温热','parent_id': None},
				{'id':3,'title':'是的','parent_id': None},
				{'id':4,'title':'不是','parent_id': 3},
			]
	        直接返回给前端的ajax
	    - ajax的回调函数succsee中获取到res.data , 并循环
	    	$.wach(res.data,funcion(index,item){
	            if(item.parent_id){
	                
	            }else{
	                
	            }
	        })
	<ul>
		<li id-"1">万元
	    	<ul>
	        	<li id-"1">张浩</li>
	        </ul>
	    </li>
	</ul>
	        
	```

多级目录存在两个问题：

- 父目录要提前出现：排序 + 字段（depth）

- 点击目录查看文章详细

	



#### 2.2 添加文章

- 目前已经完成
- BUG：已修复S

#### 



# day09

## 今日概要

- wiki删除
- wiki编辑
- markdown编辑器
	- 添加、编辑
	- 预览页面

- markdown上传图片



## 今日详细

### 1.Wiki删除

### 2.Wiki编辑

### 3.markdown编辑器

- 富文本编辑器，ckeditor。
- markdown，mdeditor。

项目中想要应用markdown编辑器

- 添加和编辑的页面中 textarea 输入框->转换未markdown编辑器

	```html
	1. textarea 输入框通过div包裹设置id以便于查找
		<div id="editor">{{ field }}</div>
	2. 应用js和css
	    <link rel="stylesheet" href="{% static 'plugin/editor-md/css/editormd.min.css' %}">
	    <script src="{% static 'plugin/editor-md/editormd.min.js' %}"></script>
	3. 初始化
	    <script>
	        $(function () {
	                initEditorMd();
	            })
	        function initEditorMd() {
	                editormd('editor', {
	                    placeholder: "请输入内容",
	                    height: 500,
	                    path: "{% static 'plugin/editor-md/lib/' %}",
	                });
	            }
	    </script>
	4. 全屏样式
	    .editormd-fullscreen{
	                z-index: 1001;
	            }
	```

	[](https://www.mdeditor.com/)

	[](https://www.github.com/pandao/editor.md)

	[](https://pandao.github.io/editor.md/)

- 预览页面按照markdown格式显示

	```html
	1. 内容区域
	    <div id="previewMarkdown">
	        <textarea>{{ wiki_object.content }}</textarea>
	    </div>
	1. 引入css和js
		<link rel="stylesheet" href="{% static 'plugin/editor-md/css/editormd.preview.min.css' %}">
	
		<script src="{% static 'plugin/editor-md/editormd.min.js' %}"></script>
	    <script src="{% static 'plugin/editor-md/lib/marked.min.js' %}"></script>
	    <script src="{% static 'plugin/editor-md/lib/prettify.min.js' %}"></script>
	    <script src="{% static 'plugin/editor-md/lib/raphael.min.js' %}"></script>
	    <script src="{% static 'plugin/editor-md/lib/underscore.min.js' %}"></script>
	    <script src="{% static 'plugin/editor-md/lib/sequence-diagram.min.js' %}"></script>
	    <script src="{% static 'plugin/editor-md/lib/flowchart.min.js' %}"></script>
	    <script src="{% static 'plugin/editor-md/lib/jquery.flowchart.min.js' %}"></script>
	3. 初始化
	     <script>
	        $(function () {
	                initPreviewMd();
	            })
	        function initPreviewMd() {
	                editormd.markdownToHTML('previewMarkdown', {
	                    htmlDecode: "style,script,iframe",
	                });
	            }
	     </script>
	```

	

总结：编辑器实现markdown编辑和预览。

差：markdown组件进行上传图片功能



### 4.腾讯对象存储

![image-20200909152041004](C:\Users\YanYeek\AppData\Roaming\Typora\typora-user-images\image-20200909152041004.png)



#### 4.1 开通腾讯对象服务



#### 4.2 后台创建存储桶

<img src="https://raw.githubusercontent.com/YanYeek/FigureBed/master/images/image-20200909153031565.png" alt="image-20200909153031565" style="zoom: 67%;" />



#### 4.3 python实现上传文件

1. 安装

```
pip install -U cos-python-sdk-v5
```

2. 初始化

	```python
	# -*- coding=utf-8
	# appid 已在配置中移除,请在参数 Bucket 中带上 appid。Bucket 由 BucketName-APPID 组成
	# 1. 设置用户配置, 包括 secretId，secretKey 以及 Region
	from qcloud_cos import CosConfig
	from qcloud_cos import CosS3Client
	import sys
	import logging
	
	logging.basicConfig(level=logging.INFO, stream=sys.stdout)
	
	secret_id = 'COS_SECRETID'      # 替换为用户的 secretId
	secret_key = 'COS_SECRETKEY'      # 替换为用户的 secretKey
	region = 'ap-chengdu'     # 替换为用户的 Region
	
	token = None                # 使用临时密钥需要传入 Token，默认为空，可不填
	scheme = 'https'            # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
	config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
	# 2. 获取客户端对象
	client = CosS3Client(config)
	# 参照下文的描述。或者参照 Demo 程序，详见 https://github.com/tencentyun/cos-python-sdk-v5/blob/master/qcloud_cos/demo.py
	```

	

	```python
	# 创建存储桶
	response = client.create_bucket(
	    Bucket='examplebucket-1250000000'
	)
	```

	

	

	```python
	#### 高级上传接口（推荐）
	# 根据文件大小自动选择简单上传或分块上传，分块上传具备断点续传功能。
	response = client.upload_file(
	    Bucket='picture-1302428193',
	    LocalFilePath='local.txt',
	    Key='picture.jpg',
	    PartSize=1,
	    MAXThread=10,
	    EnableMD5=False
	)
	print(response['ETag'])
	```

	

	

	示例代码

	```python
	from scripts import offline_scripts_base
	from qcloud_cos import CosConfig
	from qcloud_cos import CosS3Client
	from django.conf import settings
	import sys
	
	secret_id = settings.TENCENT_SECRET_ID  # 替换为用户的 secretId
	secret_key = settings.TENCENT_SECRET_KEY  # 替换为用户的 secretKey
	region = 'ap-chengdu'  # 替换为用户的 Region
	
	config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
	# 2. 获取客户端对象
	client = CosS3Client(config)
	# 参照下文的描述。或者参照 Demo 程序，详见 https://github.com/tencentyun/cos-python-sdk-v5/blob/master/qcloud_cos/demo.py
	
	response = client.upload_file(
		Bucket='picture-1302428193',
		LocalFilePath='picture.jpg',  # 本地文件路径
		Key='elephant.jpg',  # 上传到桶之后的名字
	)
	print(response['ETag'])
	```

	

### 5.项目中集成COS

希望我们的项目在用到的图片可以放在COS中，防止我们的服务处理图片时压力过大。

#### 5.1　创建项目时同时创建一个桶

```python
	if form.is_valid():
		# 1. 为项目创建一个桶
		name = form.cleaned_data.get('name')
		bucket = "{}-{}-{}-1302428193".format(name, request.tracer.user.phone, str(int(time.time())))
		region = "ap-chengdu"
		create_bucket(bucket=bucket, region=region)

		# 把桶和区域写入数据库

		# 验证通过: 项目名、颜色、描述 + creator谁创建的项目
		form.instance.bucket = bucket
		form.instance.region = region
		form.instance.creator = request.tracer.user
		# 创建项目
		form.save()
		return JsonResponse({'status': True})
```

```python
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from django.conf import settings
import sys


def create_bucket(bucket, region='ap-chengdu'):
	"""
	创建桶
	:param bucket：桶名称
	:param region: 区域
	:return:
	"""
	config = CosConfig(Region=region, SecretId=settings.TENCENT_SECRET_ID, SecretKey=settings.TENCENT_SECRET_KEY)
	# 2. 获取客户端对象
	client = CosS3Client(config)
	# 参照下文的描述。或者参照 Demo 程序，详见 https://github.com/tencentyun/cos-python-sdk-v5/blob/master/qcloud_cos/demo.py

	client.create_bucket(
		Bucket=bucket,
		ACL="public-read"  # private / public-read /public-read-write
	)
```





#### 5.2　markdown上传图片到cos

- cos上传文件: 本地文件; 接收markdown上传的文件在进行上传。
- markdown上传图片。





# day10 文件管理思路

## 功能介绍：

- 文件夹
- 文件

## 知识点：

- 模态对话框 & Ajax & 后台ModelForm校验
- 目录切换：展示当前文件夹 & 文件
- 删除文件夹：嵌套子文件 & 文件夹删除
- js上传文件到cos（Wiki使用的是python）
- 进度条操作
- 删除文件：
	- 数据库中删除
	- cos中也需要删除
- 下载文件



## 今日概要

- 设计
- 表结构的创建
- 单独知识点



## 今日详细

### 1.功能设计

![image-20200910151626614](https://picture-1302428193.cos.ap-chengdu.myqcloud.com/img/image-20200910151626614.png)

### 2.数据库设计

| ID   | 项目ID | 名称         | 类型 | 大小 | 父目录 | 更新者 | 更新时间 | key  |
| ---- | ------ | ------------ | ---- | ---- | ------ | ------ | -------- | ---- |
| 1    | 9      | 阿尔法色     | 2    | 100  | null   |        |          |      |
| 2    | 9      | 撒旦飞洒     | 2    | null | 1      |        |          |      |
| 3    | 9      | 儿童和肉体和 | 2    | null | 1      |        |          |      |
| 4    | 9      | 12.png       | 1    | 1000 |        |        |          |      |
| 5    | 9      | 13.png       | 1    | 1100 |        |        |          |      |
| 6    | 9      | 14.png       | 1    | 1000 |        |        |          |      |
| 7    |        |              |      |      |        |        |          |      |



```python
class FileRepository(models.Model):
	"""文件库"""
	project = models.ForeignKey(verbose_name='项目', to='Project')
	file_type_choices = (
		(1, '文件'),
		(2, '文件夹'),
	)
	file_type = models.SmallIntegerField(verbose_name='类型', choices=file_type_choices)
	name = models.CharField(verbose_name='文件夹名称', max_length=32, help_text='文件/文件夹名')
	key = models.CharField(verbose_name='文件存储在cos中的key', max_length=128, null=True, blank=True)
	file_size = models.IntegerField(verbose_name='文件大小', null=True, blank=True)
	file_path = models.CharField(verbose_name='文件路径', max_length=255, null=True, blank=True)

	parent = models.ForeignKey(verbose_name='父级目录', to='self', related_name='child', null=True, blank=True)

	update_user = models.ForeignKey(verbose_name='最近更新者', to='UserInfo')
	update_datetime = models.DateTimeField(verbose_name='更新时间', auto_now=True)
```

### 3.知识点

#### 3.1 URL传参 or 不传参

```
url(r'^file/$', manage.file, name='file'),
```

```python
# /file/
# /file/?folder_id=50
def file(request, project_id)
	folder_id = request.GET.get('folder_id')
```

#### 3.2 模态框 + 警告框

![image-20200910185624355](https://picture-1302428193.cos.ap-chengdu.myqcloud.com/img/image-20200910185624355.png)

https://v3.bootcss.com/javascript/#alerts



#### 3.3 获取导航条

![image-20200910185807292](https://picture-1302428193.cos.ap-chengdu.myqcloud.com/img/image-20200910185807292.png)



```python
# /file/
# /file/?folder_id=50
def file(request, project_id)
	folder_id = request.GET.get('folder_id')
    
    url_list = []
    if not folder_id:
        	pass
    else:
        file_object = models.FileRespository.objects.filter(id=folder_id, file_type=2).first()
        row_object = file_object
        while row_object:
            url_list.insert(0, row_object_name)
            row_object = row_object.parent
```



#### 3.4 cos上传文件:python

```python
def upload_file(bucket, region, file_object, key):
	"""
	上传图片到cos桶
	:param bucket:桶名称
	:param region: 区域
	:param file_object:图片对象
	:param key: 图片名字
	:return:
	"""
	config = CosConfig(Region=region, SecretId=settings.TENCENT_SECRET_ID, SecretKey=settings.TENCENT_SECRET_KEY)
	client = CosS3Client(config)
	response = client.upload_file_from_buffer(
		Bucket=bucket,
		Key=key,  # 上传到桶之后的名字
		Body=file_object  # 文件对象
	)
	# https://picture-1302428193.cos.ap-chengdu.myqcloud.com/elephant.jpg
	return "https://{}.cos.{}.myqcloud.com/{}".format(bucket, region, key)
```

详细:python操作cos的API(SDK)

注意:密钥安全



#### 3.5 cos上传文件 :js [建议官方文档]

![image-20200910210301261](https://picture-1302428193.cos.ap-chengdu.myqcloud.com/img/image-20200910210301261.png)



##### 1. 下载js(前端SDK)

地址：https://github.com/tencentyun/cos-js-sdk-v5/tree/master/dist

```html
<script src="./cos-js-sdk-v5.mim.js"></script>script>
```

##### 2. 查看官方文档

​		地址https://cloud.tencent.com/document/product/436/11459

```html
<input id="file-selector" type="file" name="upload_file" multiple>
<script src="dist/cos-js-sdk-v5.min.js"></script>
<script>
var Bucket = 'examplebucket-1250000000';
var Region = 'COS_REGION';     /* 存储桶所在地域，必须字段 */

// 初始化实例
var cos = new COS({
    getAuthorization: function (options, callback) {
        // 异步获取临时密钥
        $.get('http://example.com/server/sts.php', {
            bucket: options.Bucket,
            region: options.Region,
        }, function (data) {
            var credentials = data && data.credentials;
            if (!data || !credentials) return console.error('credentials invalid');
            callback({
                TmpSecretId: credentials.tmpSecretId,
                TmpSecretKey: credentials.tmpSecretKey,
                XCosSecurityToken: credentials.sessionToken,
                // 建议返回服务器时间作为签名的开始时间，避免用户浏览器本地时间偏差过大导致签名错误
                StartTime: data.startTime, // 时间戳，单位秒，如：1580000000
                ExpiredTime: data.expiredTime, // 时间戳，单位秒，如：1580000900
            });
        });
    }
});

// 接下来可以通过 cos 实例调用 COS 请求。
// TODO

</script>
```

格式一（推荐）：后端通过获取临时密钥给到前端，前端计算签名。

```html
<script>
    var COS = require('cos-js-sdk-v5');
    var cos = new COS({
        // 必选参数
        getAuthorization: function (options, callback) {
            // 服务端 JS 和 PHP 例子：https://github.com/tencentyun/cos-js-sdk-v5/blob/master/server/
            // 服务端其他语言参考 COS STS SDK ：https://github.com/tencentyun/qcloud-cos-sts-sdk
            // STS 详细文档指引看：https://cloud.tencent.com/document/product/436/14048
            $.get('http://example.com/server/sts.php', {
                // 可从 options 取需要的参数
            }, function (data) {
                var credentials = data && data.credentials;
                if (!data || !credentials) return console.error('credentials invalid');
                callback({
                    TmpSecretId: credentials.tmpSecretId,
                    TmpSecretKey: credentials.tmpSecretKey,
                    XCosSecurityToken: credentials.sessionToken,
                    // 建议返回服务器时间作为签名的开始时间，避免用户浏览器本地时间偏差过大导致签名错误
                    StartTime: data.startTime, // 时间戳，单位秒，如：1580000000
                    ExpiredTime: data.expiredTime, // 时间戳，单位秒，如：1580000900
                });
            });
        }
	});
</script>
```

##### 3. 跨域问题

![image-20200910211847785](https://picture-1302428193.cos.ap-chengdu.myqcloud.com/img/image-20200910211847785.png)

![image-20200910211828331](https://picture-1302428193.cos.ap-chengdu.myqcloud.com/img/image-20200910211828331.png)

解决:

![image-20200910211935432](https://picture-1302428193.cos.ap-chengdu.myqcloud.com/img/image-20200910211935432.png)



#### 3.6 cos上传文件:临时密钥[推荐]

![image-20200910212208461](https://picture-1302428193.cos.ap-chengdu.myqcloud.com/img/image-20200910212208461.png)



##### 1.路由

```
url(r'^demo2/$', manage.file, name='demo2'),
url(r'^cos/credential/$', manage.cos_credential, name='cos_credential'),
```

##### 2.视图

```python
def demo2(request):
	retrun render(request, 'demo2,html')
    
def cos_credential(request):
    # 生成一个临时凭证,并给前端返回
    # 1. 安装一个SDK pip isntall -U qcloud-python-sts
    # 2. 写代码
    from sts.sts import Sts
    config = {
        # 临时密钥有效期,单位秒,(30分钟=1800秒)
        'duration_seconds': 1800,
        # 固定密钥 id
        'secret_id':'afdaf',
        # 固定密钥 key
        'secret_key': 'wagweg',
        # 桶名称
        'bucket': '',
        # 桶所在地区
        'region': 'ap-chengdu',
        #允许的文件前缀
        'allow_prefix':'*'
        # 密钥权限列表
        'allow_actions': [
            'name/cos:PostObject',
            # '*' # 代表所有权限都可以
        ],
    }
    sts = Sts(config)
    result_dict = sts.get_credential()
	retrun JsonResponse(result_dict)
```

##### 3.html页面

```html
{% load stact %}

<!DOCTYPE html>
<html lang="en">
<head>
    ...
</head>
<body>
	<h1></h1>
    {% block js %}
    <script src="{% static 'js/cos-js-sdk-v5.min.js' %}"></script>
    <script>
        var FOLDER_URL = "{% url 'file' project_id=request.tracer.project.id %}";
        var FILE_DELETE_URL = "{% url 'file_delete' project_id=request.tracer.project.id %}";
        var COS_CREDENTIAL = "{% url 'cos_credential' project_id=request.tracer.project.id %}";
        var FILE_POST = "{% url 'file_post' project_id=request.tracer.project.id %}";
        var CURRENT_FOLDER_ID = "{{ folder_object.id }}";

        $(function () {
            initAddModal();
            bindModelSubmit();
            bindDeleteSubmit();
            bindUploadFile();
        });

        function bindUploadFile() {
            $('#uploadFile').change(function () {
                $('#progressList').empty();

                var fileList = $(this)[0].files;
                // 获取本次要上传的每个文件 名称&大小
                var checkFileList = [];
                $.each(fileList, function (index, fileObject) {
                    checkFileList.push({'name': fileObject.name, 'size': fileObject.size})
                });

                // 把这些数据发送到django后台：Django后台进行容量的校验，如果么有问题则返回临时凭证；否则返回错误信息；
                var cos_credential = new COS({
                    getAuthorization: function (options, callback) {
                        $.post(COS_CREDENTIAL, JSON.stringify(checkFileList), function (res) {
                            if (res.status) {
                                var credentials = res.data && res.data.credentials;
                                callback({
                                    TmpSecretId: credentials.tmpSecretId,
                                    TmpSecretKey: credentials.tmpSecretKey,
                                    XCosSecurityToken: credentials.sessionToken,
                                    StartTime: res.data.startTime,
                                    ExpiredTime: res.data.expiredTime
                                });

                                $('#uploadProgress').removeClass('hide');
                            } else {
                                alert(res.error);
                            }
                        });
                    }
                });

                // 上传文件（上传之前先获取临时凭证
                $.each(fileList, function (index, fileObject) {
                    var fileName = fileObject.name;
                    var fileSize = fileObject.size;
                    var key = (new Date()).getTime() + "_" + fileName;

                    var tr = $('#progressTemplate').find('tr').clone();
                    tr.find('.name').text(fileName);
                    $('#progressList').append(tr);

                    // 上传文件（异步）
                    cos_credential.putObject({
                        Bucket: '{{ request.tracer.project.bucket }}', /* 必须 */
                        Region: '{{ request.tracer.project.region }}', /* 存储桶所在地域，必须字段 */
                        Key: key, /* 必须 */
                        Body: fileObject, // 上传文件对象
                        onProgress: function (progressData) {
                            var percent = progressData.percent * 100 + '%';
                            tr.find('.progress-bar').text(percent);
                            tr.find('.progress-bar').css('width', percent);
                        }
                    }, function (err, data) {
                        if (data && data.statusCode === 200) {
                            // 上传成功，将本次上传的文件提交到后台并写入数据
                            // 当前文件上传成功
                            $.post(FILE_POST, {
                                name: fileName,
                                key: key,
                                file_size: fileSize,
                                parent: CURRENT_FOLDER_ID,
                                etag: data.ETag,
                                file_path: data.Location
                            }, function (res) {
                                // 在数据库中写入成功，将已添加的数据在页面上动态展示。
                                var newTr = $('#rowTpl').find('tr').clone();
                                newTr.find('.name').text(res.data.name);
                                newTr.find('.file_size').text(res.data.file_size);
                                newTr.find('.username').text(res.data.username);
                                newTr.find('.datetime').text(res.data.datetime);
                                newTr.find('.delete').attr('data-fid', res.data.id);
                                $('#rowList').append(newTr);

                                // 自己的进度删除
                                tr.remove();
                            })

                        } else {
                            tr.find('.progress-error').text('上传失败');
                        }
                    });


                })
            });
        }

        function bindDeleteSubmit() {
            $('#btnDelete').click(function () {
                // 获取要删除那行ID
                $.ajax({
                    url: FILE_DELETE_URL,
                    type: "GET",
                    data: {fid: $(this).attr('fid')},
                    success: function (res) {
                        if (res.status) {
                            location.href = location.href;
                        }
                    }
                })
            })
        }

        function initAddModal() {
            $('#addModal').on('show.bs.modal', function (event) {
                var button = $(event.relatedTarget); // Button that triggered the modal
                var recipient = button.data('whatever'); // Extract info from data-* attributes
                var name = button.data('name'); // Extract info from data-* attributes
                var fid = button.data('fid'); // Extract info from data-* attributes
                var modal = $(this);
                modal.find('.modal-title').text(recipient);

                if (fid) {
                    // 编辑
                    modal.find('#id_name').val(name);
                    modal.find('#fid').val(fid);
                } else {
                    // 新建
                    modal.find('.error-msg').empty();
                    $('#form')[0].reset();
                }
            });

            $('#alertModal').on('show.bs.modal', function (event) {
                var button = $(event.relatedTarget); // Button that triggered the modal
                var fid = button.data('fid'); // Extract info from data-* attributes
                $('#btnDelete').attr('fid', fid);

            })
        }

        function bindModelSubmit() {
            $('#btnFormSubmit').click(function () {
                $.ajax({
                    url: location.href,
                    type: "POST",
                    data: $("#form").serialize(),
                    dataType: "JSON",
                    success: function (res) {
                        if (res.status) {
                            location.href = location.href;
                        } else {
                            $.each(res.error, function (key, value) {
                                $("#id_" + key).next().text(value[0]);
                            })
                        }
                    }
                })
            })
        }
    </script>
{% endblock %}
</body>
</html>
```



##### 4.跨域解决

##### 总结:

- python直接上传
- js + 临时凭证(跨域问题)



#### 3.7 cos的功能 & 项目

#####  1.创建项目 & 创建存储桶

```python
def project_list(request):
	"""项目列表"""

	# POST，对话框的ajax添加项目。
	form = ProjectModelForm(request, data=request.POST)
	if form.is_valid():
		# 1. 为项目创建一个桶 & 创建跨域规则
		name = form.cleaned_data.get('name')
		bucket = "{}-{}-1302428193".format(request.tracer.user.phone, str(int(time.time())))
		region = "ap-chengdu"
		create_bucket(bucket=bucket, region=region)

		# 把桶和区域写入数据库

		# 验证通过: 项目名、颜色、描述 + creator谁创建的项目
		form.instance.bucket = bucket
		form.instance.region = region
		form.instance.creator = request.tracer.user
		# 创建项目
		form.save()
		return JsonResponse({'status': True})

	# 验证不通过 返回错误信息
	return JsonResponse({'status': False, 'error': form.errors})
```

```python
def create_bucket(bucket, region='ap-chengdu'):
	"""
	创建桶
	:param bucket：桶名称
	:param region: 区域
	:return:
	"""
	config = CosConfig(Region=region, SecretId=settings.TENCENT_SECRET_ID, SecretKey=settings.TENCENT_SECRET_KEY)
	# 2. 获取客户端对象
	client = CosS3Client(config)
	# 参照下文的描述。或者参照 Demo 程序，详见 https://github.com/tencentyun/cos-python-sdk-v5/blob/master/qcloud_cos/demo.py

	client.create_bucket(
		Bucket=bucket,
		ACL="public-read"  # private / public-read /public-read-write
	)
    
    # 配置跨域设置
    cors_config = {
        'CORSRule': [
            {
                'AllowedOrigin': '*',
                'AllowedMethod': ['GET', 'PUT', 'HEAD', 'POST', 'DELETE'],
                'AllowedHeader': '*',
                'ExposeHeader': '*',
                'MaxAgeSeconds': 500,
            }
        ]
    }
    client.put_bucket_cors(
    	Bucket=bucket,
        CORAConfiguration=cors_config,
    )
```





#### 3.8 markdown上传文件【无改动】



#### 3.9 js上传文件

- 临时凭证：当前项目的 桶&区域 (request.tracer.project)
- js上传文件: 设置当前的 桶&区域





#### 3.10 this

```js
var name='YanYeek'

function func(){
    var name='CC'
    console.log(name) // CC
}

func();
```



```js
var name='YanYeek'

function func(){
    var name='CC'
    console.log(this.name) // YanYeek
}

func(); // this=全局window 相当于window
```

```js
var name='YanYeek'
info = {
    name='Yahoo'
    func:function(){
        console.log(this.name) // Yahoo
        function test(){
            console.log(this.name)
        }
        teat()
    }
}

info.func()
```

总结:每个函数都是一个作用域,在它的内部都会存在this,谁调用的函数,谁就是this

不管嵌套多少次,函数被调用的前面是谁,它的this就是谁。



#### 3.11 闭包

```js
data_list = [11,22,33]
$.each(data_list, function(index,value){
    console.log(value);
})

for(var i ;i++; i < data_list.length){
    console.log(i, data_list[i]);
}
```

```js
data_list = [11,22,33]
for(var i=0 ;i++; i < data_list.length){
    // 循环发送3次ajax请求,由于ajax是异步请求,所有在发送请求时不会等待.
    $.ajax({
        url:"...",
        data:{value:data_list[i]},
        success: function(res){
            // 1分钟之后执行回调函数
        }
    })
}

console.log("YanYeek")
```



```js
data_list = [11,22,33]
for(var i=0 ;i++; i < data_list.length){
    // 循环发送3次ajax请求,由于ajax是异步请求,所有在发送请求时不会等待.
    $.ajax({
        url:"...",
        data:{value:data_list[i]},
        success: function(res){
            // 1分钟之后执行回调函数
            console.log(i) // 全部输出:2
        }
    })
}

console.log(i) // 输出:2
```



```js
data_list = [11,22,33]
for(var i=0 ;i++; i < data_list.length){
    // 循环发送3次ajax请求,由于ajax是异步请求,所有在发送请求时不会等待.
    function xx(data){        
        $.ajax({
            url:"...",
            data:{value:data_list[i]},
            success: function(res){
                // 1分钟之后执行回调函数
                console.log(data) // 全部输出:2
            }
    	})
    }
    xx(i)
}
// 用函数嵌套ajax异步请求,让它同时开了3块不同的空间,i也被data接收变成了三个不同的值,所以实现了回调函数分别打出0,1,2,的效果。

console.log(i) // 输出:2
```

注意事项：如果循环,循环内容发送异步请求，一部任务成功之后，通过闭包来解决。



# day11 文件管理

## 今日概要

- 文件夹管理
- 文件上传
- 思考：限制如何实现？



## 今日详细

### 1.文件夹管理



#### 1.1 创建文件夹

#### 1.2 文件列表 & 进入文件夹

#### 1.3 编辑文件夹

#### 1.4 删除文件夹（DB级联删除 & 删除COS文件）





### 2.文件上传

#### 2.1 上传按钮

#### 2.2 获取临时凭证&上传文件

#### 2.3 右下角展示进度条

#### 2.4 上传文件保存到数据库





# day12 文件上传

## 今日概要

- 获取临时凭证 & 上传文件
- 右下角展示进度条
- 上传文件保存到数据库
- 容量的限制



## 今日详细

### 1.获取临时凭证&上传文件

- 创建项目L添加跨域

- 上传文件前：获取临时凭证

	- 全局：默认超时之后JDK自动再次获取（官方推荐）。

	ps：new了一个cos对象必须调用才会执行里面的方法发请求。

	- 局部：每次上传文件之前，进行临时凭证获取。

- 容量限制：

	- 单文件限制
	- 总容量限制

	注意：容量不合法，错误提示；合法，继续上传

- 继续上传

- 上传成功之后：将当前上传的信息发送至数据库

	- 前端向cos上传文件成功之后
	- 前端向后台发送请求：文件大小/文件名/文件 。。。（后台数据保存到数据库）

	![image-20200914092317021](https://picture-1302428193.cos.ap-chengdu.myqcloud.com/img/image-20200914092317021.png)

- 实时展示添加的文件



扩展：ajax向后台发送消息

```js
前端：
$.ajax({
    data:{name:11. age:22,xx:[11,22,33]}
})

Django后台：
	request.POST
	request.POST.get('name')
	request.POST.get('age')
	request.POST.get('xx')
	多层嵌套的复杂数据django获取不到
```

```js
前端：
$.ajax({
    data: JSON.stringfy({name:11. age:22,xx:[11,22,33]})
})

Django后台：
	request.body
	info = json.loads(request.body.decode('utf-8'))
	info['name']
把数据JSON化才行，接收要用body接收字节后要编码为字符串。
```











# day13

![image-20200914092916282](https://picture-1302428193.cos.ap-chengdu.myqcloud.com/img/image-20200914092916282.png)

![image-20200914092934453](https://picture-1302428193.cos.ap-chengdu.myqcloud.com/img/image-20200914092934453.png)





## 今日概要

- 文件管理：下载
- 项目删除
- 问题管理：
	- 表结构设计
	- 新建问题
	- 问题展示列表
	- 分页处理





## 今日详细

### 1.下载文件

```
浏览器                django
请求					HttpResponse(...)文本;响应头
请求					render(...)		文本;响应头
请求					...       		文件内容;响应头
```

![image-20200914095352219](https://picture-1302428193.cos.ap-chengdu.myqcloud.com/img/image-20200914095352219.png)

```python
def download(request):
    # 打开文件，获取文件的内容
    with open('xxx.xxx', mode ='rb') as f:
        data = f.read()
    response = HttpResponse(data)
    response["Content-Disposition"] = "attachment; filename=xxx.png"
 	return response
```

### 2.删除项目

- 项目删除
- 桶删除
	- 删除所有文件
	- 删除碎片文件
- wiki图片思考
	- 如果要实现文章的图片删除功能就要加更多没必要的逻辑，服务器压力太大。
	- 考虑服务器与开发时间成本不划算。

### 3.问题管理

#### 3.1 设计表结构

![image-20200914212340094](https://picture-1302428193.cos.ap-chengdu.myqcloud.com/img/image-20200914212340094.png)

![image-20200914213544435](https://picture-1302428193.cos.ap-chengdu.myqcloud.com/img/image-20200914213544435.png)

```
- 产品经理：功能 +原型图
- 开发人员：第一步表结构设计
```

| ID   | 标题 | 内容 | 问题类型 | 模块 | 状态CH | 优先级CH | 指派FK | 关注者m2m | 开始时间 | 结束时间 | 模式 | 父问题 |
| ---- | ---- | ---- | -------- | ---- | ------ | -------- | ------ | --------- | -------- | -------- | ---- | ------ |
|      |      |      |          |      |        |          |        |           |          |          |      |        |
|      |      |      |          |      |        |          |        |           |          |          |      |        |
|      |      |      |          |      |        |          |        |           |          |          |      |        |

| ID   | 问题类型 | 项目ID | 颜色 |
| ---- | -------- | ------ | ---- |
| 1    | Bug      |        |      |
| 2    | 功能     |        |      |
| 3    | 任务     |        |      |



| ID   | 模块            | 项目ID |
| ---- | --------------- | ------ |
| 1    | 第一期 用户认证 |        |
| 2    | 第二期 任务管理 |        |
| 3    | 第三期 支付     |        |

#### 3.2 新建问题

##### 3.2.1 模态对话框

- 显示对话框
- 显示用户要填写的数据（表单）

前端插件：

- bootstrap-datepicker

	```
	css
	js
	找到标签处理
	```

- bootstrap-select插件

	```python
	css
	js
	ModelForm中添加属性
	class IssuesModalForm(BootStrapForm, forms.ModelForm):
		class Meta:
			model = models.Issues
			exclude = ['project', 'creator', 'create_datetime', 'latest_update_datetime']
			widgets = {
				'assign': forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'}),
				'attention': forms.SelectMultiple(
					attrs={'class': 'selectpicker', 'data-live-search': 'true', 'data-actions-box': 'true'}),
			}
	class BootStrapForm(object):
		bootstrap_class_exclude = []
	
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			for name, field in self.fields.items():
				if name in self.bootstrap_class_exclude:
					continue
				old_class = field.widget.attrs.get('class', '')
				field.widget.attrs['class'] = f'{old_class} form-control'
				field.widget.attrs['placeholder'] = '请输入%s' % (field.label,)		
	```

	​	

#### 3.3 问题列表



#### 3.4 自定义分页（10年前文件）





# day14

## 今日概要

- 添加问题
- 问题列表 + 分页
- 编辑问题
	- 回复
	- 问题变更



## 今日详细

### 1.添加问题

#### 1.1 数据初始化和合法性

#### 1.2 添加数据（成功之后刷新页面）

#### 1.3 错误提示

`为了避免插入error-msg冲突，把form渲染的内容嵌套一个div，但是bootstrap-select默认会在嵌套一个div，应用了此插件可不用嵌套`

```html
<div class="col-md-8 clearfix">
<div>
{{ form.status }}
</div>
<div class="error-msg"></div>
```

#### 1.4 扩展

```
- bootstrap-select
- 下拉框渲染（自定义插件）
```



### 2.问题列表分页

#### 2.1 问题列表



#### 2.2 分页

```
http://127.0.0.1:8000/manage/10/issues/?page=1
http://127.0.0.1:8000/manage/10/issues/?page=2
- 数据库获取数据
	models.User.object.all(0:10)
	models.User.object.all(10:20)
	...
- 显示页面
	- 点击当前显示的页面选中
	- 显示11个页面（前五个、后五个，根据总页数与当前页，自适应显示，且除page外的其他参数保留不变）

```

了解逻辑，整理出一个class，以后直接用。



### 3.编辑问题

#### 3.1 编辑页面展示



#### 3.2 问题讨论（回复嵌套}

| ID   | 内容 | 类型     | 评论者/修改者 | 自己FK | 问题FK |
| ---- | ---- | -------- | ------------- | ------ | ------ |
|      |      | 回复     |               |        |        |
|      |      | 修改记录 |               |        |        |
|      |      |          |               |        |        |



##### 3.2.1 ajax请求回去所有评论

- 获取评论
- js嵌套展示

##### 3.2.2 评论 & 回复

- 评论
- 回复



# day15

## 今日概要

- 问题跟新 + 操作记录
- 问题列表筛选
- 邀请成员





## 今日详细

### 1.知识点

#### 1.1 反射



```python
print(xxx_object.name)
getattr(xx_object,"name")
示例1：
	request.POST
    getattr(reuqest,"name")
示例2：
	row = models.User.objects.filter(id=1).first()
    row.name
    row.email
    getattr(reuqest,"name")    
```

```python
xxx_object.name = "YanYeek"
setattr(xxx_object,"name","YanYeek")

示例1：
	row = models.User.objects.filter(id=1).first()
    row.email = "aeff@wef.com"
    setattr(row,"email","aeff@wef.com")
    row.save()
```

需求：我通过ajax发送一个数据{“v1”: ”email”, “v2”: ”aeff@wef.com”,}，{“v1”: ”name”, “v2”: ”YanYeek”,}，{“v1”: ”age”, “v2”: ”18”,}， 获取到这个字典后，对数据库中的用户表进行一次更新操作。

后端代码不用更改

```python
def index(request):
    data_dict = json.loads(request.body.decode('utf-8'))
    user_object = models.User.objects.filter(id=1).first()
    setattr(user_object,data_dict["v1"],data_dict["v2"])
    user_object.save()
    
    return JsonResponse({"status": Ture})
```



#### 1.2 orm字段

需求：前端发送json{‘key’,: ‘email’}, 后端结束到数据之后，去ORM类User中校验是否允许为空。

```python
class UserInfo(models.Model):
	username = models.CharField(verbose_name='用户名', max_length=32, db_index=True)  # 创建索引，加快查询速度
	email = models.EmailField(verbose_name='邮箱', max_length=32)
	phone = models.CharField(verbose_name='手机号', max_length=32)
	password = models.CharField(verbose_name='密码', max_length=32)

def index(request):
    data_dict = json,loads(request,body.decode('utf-8'))
    data_dict["key"] # "email"
	models.UserInfo._meta.get_field("email")
    field_object.verbose_name # 邮箱；密码
    field_object.null # True；False
```



#### 1.3 可迭代对象

如果一个对象中存在`__iter__` 方法，且它返回一个迭代器。那么我们将根据类创建的对象，为可迭代对象。

时可迭代对象支持for循环

```python
class Foo:
    pass
obj1 = Foo()
obj2 = Foo()
```

```python
class Bar:
    def __iter__(self):
        yield 1
        yield 2
        yield 3
        
obj3 = Bar()
obj4 = Bar()
for item in obj3:
    print(item) # 1 2 3
```

示例：

```python
class Bar:
    def __iter__(self):
		yield 1
		yield 2
        yield 3

def index(request):
    obj = Bar()
    return render(request, 'index.html', {'data_list':obj})
```



```html
<html>
    ...
    <ul>
        {% for data in data_list %}
        	<li>{{ data }}</li>
        {% endfor %}
    </ul>
</html>
```



### 2.问题的更新

#### 2.1 给点的的标签绑定事件



#### 2.2 出发事件发送ajax



#### 2.3 后台接收数据并做跟新



#### 2.4 生成更新记录返回前端







# day16

## 今日概要

- 筛选
	- choices
	- fk
	- select2
- 邀请成员
- 概览

注意：提前准备支付宝沙箱环境



## 今日详细

### 1.筛选

#### 1.2 FK

#### 1.3 select2



### 2.邀请

#### 2.1 表结构设计

| ID   | 有效期 | 数量 | 使用数量 | 创建者 | 邀请码 | 项目 |      |
| ---- | ------ | ---- | -------- | ------ | ------ | ---- | ---- |
| 1    | 2      | 2    | 1        | 1      |        |      |      |
|      |        |      |          |        |        |      |      |
|      |        |      |          |        |        |      |      |

```python
class ProjectInvite(models.Model):
	""" 项目邀请码 """

	project = models.ForeignKey(verbose_name='项目', to='Project')
	code = models.CharField(verbose_name='邀请码', max_length=64, unique=True)
	count = models.PositiveIntegerField(verbose_name='限制数量', null=True, blank=True, help_text="空代表无数量限制")
	use_count = models.PositiveIntegerField(verbose_name='已邀请数量', default=0)
	period_choices = (
		(30, '30分钟'),
		(60, '一小时'),
		(300, '5小时'),
		(1440, '34小时'),
	)
	period = models.IntegerField(verbose_name='有效期', choices=period_choices, default=1440)
	create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
	creator = models.ForeignKey(verbose_name='创建者', to='UserInfo', related_name='create_invite')
```



#### 2.2 开发

##### 2.2.1 对话框

##### 2.2.2 生成邀请码

##### 2.2.3 访问





### 3.概览

![image-20200916172048754](https://picture-1302428193.cos.ap-chengdu.myqcloud.com/img/image-20200916172048754.png)

#### 3.1 详细



#### 3.2问题



#### 3.3 成员



#### 3.4 动态



#### 3.5 问题趋势







# day17

## 今日详细

### 1.django时区

```python
# UTC 格林威治标准时间
# Asia/Shanghai 东八区中国北京时间，快标准时间8小时整
TIME_ZONE = 'Asia/Shanghai'
# 为True时写入数据库时间为 UTC，False时写入数据库时间为TIME_ZONE所设置时间
USE_TZ = True
```



### 2.bug

```python
# 最多允许的成员(当前项目创建者的限制）
	max_transaction = models.Transaction.objects.filter(user=invite_object.project.creator).order_by('-id').first()
	# 如果已经过期 使用免费额度
	if max_transaction.pricePolicy.category == 1:
		max_member = max_transaction.price_project.project_member
	else:
		if max_transaction.end_datetime < current_datetime:
			# 如果已经过期 使用也免费额度
			free_object = models.PricePolicy.objects.filter(category=1).first()
			max_member = free_object.project_member
		else:
			# 如果没有过期，使用套餐额度
			max_member = max_transaction.price_project.project_member
```

### 3.画图

在网页上画图：HighCharts/Echarts

#### 3.1 下载文件 

https://www.highcharts.com.cn/download

#### 3.2 应用

```
<script src="http://cdn.highcharts.com.cn/highcharts/8.2.0/highcharts.js"></script>
```

```html
<div id="i1"></div>
```

```js
var chart = Highcharts.chart('container', {
		title: {
				text: '2010 ~ 2016 年太阳能行业就业人员发展情况'
		},
		subtitle: {
				text: '数据来源：thesolarfoundation.com'
		},
		yAxis: {
				title: {
						text: '就业人数'
				}
		},
		legend: {
				layout: 'vertical',
				align: 'right',
				verticalAlign: 'middle'
		},
		plotOptions: {
				series: {
						label: {
								connectorAllowed: false
						},
						pointStart: 2010
				}
		},
		series: [{
				name: '安装，实施人员',
				data: [43934, 52503, 57177, 69658, 97031, 119931, 137133, 154175]
		}, {
				name: '工人',
				data: [24916, 24064, 29742, 29851, 32490, 30282, 38121, 40434]
		}, {
				name: '销售',
				data: [11744, 17722, 16005, 19771, 20185, 24377, 32147, 39387]
		}, {
				name: '项目开发',
				data: [null, null, 7988, 12169, 15112, 22452, 34400, 34227]
		}, {
				name: '其他',
				data: [12908, 5948, 8105, 11248, 8989, 11816, 18274, 18111]
		}],
		responsive: {
				rules: [{
						condition: {
								maxWidth: 500
						},
						chartOptions: {
								legend: {
										layout: 'horizontal',
										align: 'center',
										verticalAlign: 'bottom'
								}
						}
				}]
		}
});
```

```
data:[
    [时间戳，9]，
    [时间戳，9]，
    [时间戳，9]，
    [时间戳，9]，
    [时间戳，9]，
]
```



#### 3.3 关于中文包

- 提供了js文件就导入文件
- 不提供需要自定义配置



#### 总结：

- 下载并引入

- 应用

	- 引入js
	- 定义div
	- js进行配置

- 以后有需求： demo + api

- 注意事项：series

	- 生成单条图

	```
	series:[{
		data:[1,2,3,4,5,6,7,8,9]
	}]
	```

	

	- 生成多条图

	```
	series:[
	{	
		name: '苹果',
		data:[1,2,3,4,5,6,7,8,9]
	},
	{
		name: '橘子',
		data:[1,2,3,4,5,6,7,8,9]
	},
	{
		name: '香蕉',
		data:[1,2,3,4,5,6,7,8,9]
	},
	{
		name: '啦啦啦',
		data:[1,2,3,4,5,6,7,8,9]
	},
	]
	```



### 4.统计

#### 4.1 daterangepicker插件



#### 4.1 饼图



#### 4.2 柱状图



































