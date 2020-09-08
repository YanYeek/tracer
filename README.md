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

![image-20200908141934319](https://raw.githubusercontent.com/YanYeek/FigureBed/master/images/image-20200908141934319.png)



























