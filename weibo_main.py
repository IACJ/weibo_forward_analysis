#coding:utf-8
import urllib2
import post_encode
import time
import os
from weibo_login import WeiboLogin
import get_weibo
if __name__ == '__main__':
	#Login = WeiboLogin('17089368196', 'tttt5555')
	Login = WeiboLogin('用户名', '密码')
	if Login.login() == True:
		print "登录成功"
	rnd = long((time.time())*1000)
	#可以根据page来循环以便达到爬取多页的目的
	init_url = "http://weibo.com/aj/v6/mblog/info/big?ajwvr=6&id=3917356680052180&max_id=3917762218921722"
	url = init_url + "&page=1&_rnd=" + str(rnd)
	html = urllib2.urlopen(url)
	#调用解析html内容的函数
	forward_html = urllib2.urlopen("http://weibo.com/1336593085/D7hwE0dzC?type=repost#_rnd1449550776472").read()
	#print forward_html
	origin_uid = get_weibo.get_origin_weibo(forward_html)
	(uid, origin_uid2_no, uid2_no, time_no, time_no2, total_forward, total_page, current_page) = get_weibo.get_forward(html, forward_html)
	#循环抓取多页
	print total_page
	uid = []
	origin_uid2 = []
	uid2 = []
	forward_time =[]
	forward_time2 = []
	count = 0
	for i in range(1,total_page):
		rnd = long((time.time())*1000)
		#可以根据page来循环以便达到爬取多页的目的
		url = init_url + "&page=" + str(i) + "&__rnd=" + str(rnd)
		html = urllib2.urlopen(url)
		(uid_temp, origin_uid2_temp, uid2_temp, time_temp, time_temp2, total_forward, total_page, current_page) = get_weibo.get_forward(html , forward_html)
		print "current page"
		print current_page
		#mid += mid_temp
		uid += uid_temp
		count  += len(uid_temp)
		origin_uid2 += origin_uid2_temp
		uid2 += uid2_temp
		forward_time += time_temp
		forward_time2 += time_temp2
	print len(uid)
	with open("data.csv", "w") as data:
		for i in range(0, len(uid)):
			print>>data, "%s,%s,'%s'" %(origin_uid, uid[i], forward_time[i])
	print total_forward
	with open("data.csv", "a") as data:
		for i in range(0, len(origin_uid2)):
			print >>data, "%s,%s,'%s'" %(origin_uid2[i], uid2[i], forward_time2[i])
	for i in range(0, len(origin_uid2)):
		print origin_uid2[i] + "->" +uid2[i]