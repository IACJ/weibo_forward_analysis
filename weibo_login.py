#coding:utf-8
import urllib
import urllib2
import re
import json
import cookielib
import random
import time
import Image
import post_encode
import get_weibo
class WeiboLogin:
	"""docstring for WeiboLogin"""
	#初始化
	def __init__(self, user_name, user_password):
		self.user_name = user_name
		self.user_password = user_password
 		su = post_encode.encrypt_user_name(user_name)
		# ?entry=weibo
		# &callback=sinaSSOController.preloginCallBack
		# &su=MTg1MzU0Nzc5MDE%3D
		# &rsakt=mod
		# &checkpin=1
		# &client=ssologin.js(v1.4.18)
		# &_=1448083786752
		curr_time = str(int(time.time()))
		self.pre_login_url = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&checkpin=1&callback=sinaSSOController.preloginCallBack&rsakt=mod&client=ssologin.js(v1.4.18)" + "&su=" + su +"&_=" + curr_time
		self.login_url = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.11)"
		self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0'}
	#cookie非常重要
	def enableCookies(self):
            		#获取一个保存cookies的对象
	            cookie= cookielib.CookieJar()
	            #将一个保存cookies对象和一个HTTP的cookie的处理器绑定
	            cookie_support = urllib2.HTTPCookieProcessor(cookie)
	            #创建一个opener,设置一个handler用于处理http的url打开
	            opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
	            #安装opener，此后调用urlopen()时会使用安装过的opener对象
	            urllib2.install_opener(opener)
	#此函数获取服务器返回的必要的登录数据
	def get_server_data(self):
		server_data = urllib2.urlopen(self.pre_login_url).read()
		#匹配返回的server_data
		p = re.compile('\((.*)\)')
		get_data = p.search(server_data).group(1)
		print p.search(server_data).group(1)		
		get_json = json.loads(get_data)
		server_time = get_json['servertime']
		nonce = get_json['nonce']
		pubkey = get_json['pubkey']
		rsakv = get_json['rsakv']
		pcid = get_json['pcid']
		show_pin = 0
		show_pin = get_json['showpin']
		# print show_pin
		# try:
		# 	show_pin = get_json['showpin']
		# except:
		# 	print "无验证码"
		return (server_time, nonce, pubkey, rsakv, show_pin, pcid)
	#此函数获取验证码
	def get_pin(self, pcid):
		pin_code_url = "http://login.sina.com.cn/cgi/pin.php"
		#产生随机数
		#pcid = "xd-01ee4d114e1c59964396d92937c2de294e20"
		url_random = str(int(random.random() * 100000000))
		pin_code_url = pin_code_url + "?r=" + url_random + "&s=0" + "&p=" + pcid
		pin_code = urllib2.urlopen(pin_code_url).read()
		f = open("/home/ruansongsong/work/code", "wb")
		f.write(pin_code)
		f.close()
		#显示验证码图片
		image = Image.open("/home/ruansongsong/work/code")
		image.show()
		#输入验证码
		input_code = raw_input()
		return input_code		        		
	#返回登陆成功的url
	def get_location_replace(self, get_html):
		p = re.compile('location\.replace\([\'"](.*?)[\'"]\)')
		get_login_url = p.search(get_html).group(1)
		return get_login_url
	#此函数执行登录
	def login(self):
		#调用cookie函数
		self.enableCookies()
		#调用get_server_data函数
		(server_time, nonce, pubkey, rsakv, show_pin, pcid) = self.get_server_data()
		if (show_pin):
			get_input_code = self.get_pin(pcid)
			#调用pos_encode函数
			post_data = post_encode.post_encode(self.user_name, self.user_password, server_time, nonce, pubkey, rsakv, get_input_code)
		else:
			post_data = post_encode.post_encode(self.user_name, self.user_password, server_time, nonce, pubkey, rsakv)
		#向服务器发送请求
		req = urllib2.Request(self.login_url, post_data, self.headers)
		get_html = urllib2.urlopen(req).read()
		#调用get_location_url获取返回的地址
		try:
			get_login_url = self.get_location_replace(get_html)
			print "登陆成功后的地址："
			print get_login_url
			urllib2.urlopen(get_login_url)
			
		except:
			print "登录失败"
			return False
		return True