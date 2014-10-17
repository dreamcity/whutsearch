# -*- coding: utf-8 -*-
import urllib.request as request
from http.client import IncompleteRead
from urllib.error import HTTPError , URLError
import socket  
import time  
import chardet
import re
import os
import hashlib
import short_url
import dbprocess

class SpiderHttp(object):
	"""docstring for SpiderHttp"""
	def __init__(self):
		# self.url = url
		self.codedetect = ''
		# self.urlList= []
		self.dbp = dbprocess.MySqlBase()
		self.dbp.createDB()
		
	def downloadPage(self,suprurl):
		if os.path.exists('whuthtmldata'):
			pass
		else:
			os.mkdir('whuthtmldata')
		newurlid = self.dbp.getMaxUrlID() + 1
		tinyurl = short_url.encode_url(newurlid)
		self.dbp.updateUrltable(newurlid,suprurl,tinyurl)
		storepath = './whuthtmldata/'+tinyurl + '.html'
		request.urlretrieve(suprurl,storepath)

	def getUrlPage(self, url):
		timeout = 10 
		socket.setdefaulttimeout(timeout)
		sleep_download_time = 1
		time.sleep(sleep_download_time)
		user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
		headers = { 'User-Agent' : user_agent }
		urlreq = request.Request(url, headers = headers)
		urlResponse = request.urlopen(urlreq)
		urlPage = urlResponse.read()
		self.codedetect = chardet.detect(urlPage)['encoding']
		if self.codedetect:
			urlPage =urlPage.decode(self.codedetect,'ignore')		
		urlResponse.close()
		self.downloadPage(url)
		return urlPage

	def getUrlList(self,suprurl):
		urlList = []
		try:
			urlPage = self.getUrlPage(suprurl)
		except HTTPError :
			return urlList
		except URLError :
			return urlList
		except socket.timeout :
			return urlList
		except IncompleteRead :
			return urlList
		except ConnectionAbortedError :
			return urlList
		urlPage = self.getUrlPage(suprurl)
		if self.codedetect != 'utf-8' and self.codedetect != 'gbk' and self.codedetect !='GB2312':
			pass
		else:
			urlPage = urlPage.replace(u'\u30fb', u'')
			pattern = re.compile(r'<a href="h.*?"|<a href="./.*?"',re.M)
			urlstrList = pattern.findall(urlPage)
			for urlstr in urlstrList:
				url = urlstr[9: -1]
				if (url[0] == r'.'):
					url = suprurl + url[1:]
				urlList.append(url)
		return urlList
					
# url = r'http://i.whut.edu.cn/'
# SH = SpiderHttp()
# urllist = SH.getUrlList(url)
# print(urllist)

