# -*- coding: utf-8 -*-
# urltable
# id  超链接的索引值
# originalurl   完整的的超链接 
# shorturl  根据id得到的md5编码，也是存储在本地的文件名
# visitedflag  默认为null，为文件预处理的标记
# 			 完成倒排序索引值，之后置为true

from mysql import connector

class MySqlBase(object):
	"""docstring for MySqlBase"""
	def __init__(self):
		super(MySqlBase, self).__init__()
		self.user = 'dreamcity'
		self.pwd = '304031870'
		self.host = 'localhost'
		self.basename = 'whutsearch'
		self.urltable = 'urltable'
		self.wftable = 'wordfiletable'
		self.createDB()
	
	def createDB(self):
		cnx = connector.connect(user= self.user, password = self.pwd, host = self.host)
		cur = cnx.cursor()
		sqlorder = "CREATE DATABASE IF NOT EXISTS %s" %self.basename
		cur.execute(sqlorder)
		sqlorder = "USE %s" %self.basename
		cur.execute(sqlorder)
		sqlorder = "CREATE TABLE IF NOT EXISTS %s (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,originalurl VARCHAR(200),shorturl VARCHAR(10),visitedflag boolean DEFAULT NULL)" %self.urltable
		cur.execute(sqlorder)
		sqlorder = "CREATE TABLE IF NOT EXISTS %s (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,wordname VARCHAR(30),filestr mediumtext)" %self.wftable
		cur.execute(sqlorder)
		cur.close()
		cnx.commit()
		cnx.close() 

	def getMaxUrlID(self):
		maxid = 0
		cnx = connector.connect(user= self.user, password = self.pwd, host = self.host)
		cur = cnx.cursor()
		sqlorder = "USE %s" %self.basename
		cur.execute(sqlorder)
		sqlorder = "select id from %s where id =( select MAX(id) from %s)" %(self.urltable,self.urltable)
		cur.execute(sqlorder)
		records = cur.fetchall()
		cur.close()
		cnx.commit()
		cnx.close()
		if records:
			maxid = records[0][0]
		# for row in records:
		# 	if row:
		# 		maxid = row[0]
		return maxid

	def insertUrltable(self,urlid,originalurl,shorturl):
		cnx = connector.connect(user= self.user, password = self.pwd, host = self.host)
		cur = cnx.cursor()
		sqlorder = "USE %s" %self.basename 
		cur.execute(sqlorder)
		sqlorder = "INSERT INTO %s VALUES(%d,'%s','%s',False)" %(self.urltable, urlid, originalurl,shorturl)
		cur.execute(sqlorder)					
		cur.close()
		cnx.commit()
		cnx.close()

	def updateVisitedFlag(self,visitedlist):
		cnx = connector.connect(user= self.user, password = self.pwd, host = self.host)
		cur = cnx.cursor()
		sqlorder = "USE %s" %self.basename 
		cur.execute(sqlorder)
		# visitedlist = list(visitedset) 
		for visitedenum in visitedlist:
			sqlorder = "update urltable set visitedflag = True where shorturl = '%s'" %(visitedenum)
			cur.execute(sqlorder)					
		cur.close()
		cnx.commit()
		cnx.close()

	def getOriUrlFSUrl(self,tinyurl):
		oriUrl = ''
		cnx = connector.connect(user= self.user, password = self.pwd, host = self.host)
		cur = cnx.cursor()
		sqlorder = "USE %s" %self.basename 
		cur.execute(sqlorder)
		sqlorder = "select originalurl from %s where shorturl = '%s'" %(self.urltable,tinyurl)
		cur.execute(sqlorder)
		records = cur.fetchall()
		cur.close()
		cnx.commit()
		cnx.close()
		if records:
			oriUrl = records[0][0]
		return oriUrl
	
	def getOriginalUrllist(self):
		originalUrllist = []
		cnx = connector.connect(user= self.user, password = self.pwd, host = self.host)
		cur = cnx.cursor()
		sqlorder = "USE %s" %self.basename
		cur.execute(sqlorder) 
		sqlorder = "select  %s from %s " %('originalurl',self.urltable)
		cur.execute(sqlorder)
		records = cur.fetchall()
		cur.close()
		cnx.commit()
		cnx.close()
		for row in records:
		    if row:
		    	originalUrllist.append(row[0])
		    # print('row', row)
		    # for r in row:
		        # originalUrllist.append(r)
		return originalUrllist

	def getNVisShortUrllist(self):
		nvisitedUrllist = []
		cnx = connector.connect(user= self.user, password = self.pwd, host = self.host)
		cur = cnx.cursor()
		sqlorder = "USE %s" %self.basename 
		cur.execute(sqlorder) 
		sqlorder = "select  %s from %s where visitedflag = False" %('shorturl',self.urltable)
		cur.execute(sqlorder)
		records = cur.fetchall()
		cur.close()
		cnx.commit()
		cnx.close()
		for row in records:
		    for r in row:
		        nvisitedUrllist.append(r)
		return nvisitedUrllist

	def updateWFtable(self,wordfiledict):
		filestr = ''
		cnx = connector.connect(user= self.user, password = self.pwd, host = self.host)
		cur = cnx.cursor()
		sqlorder = "USE %s" %self.basename 
		cur.execute(sqlorder)

		for wordname in wordfiledict.keys():
			filesetstr = wordfiledict[wordname]
			sqlorder = "select filestr from %s where wordname = '%s'" %(self.wftable,wordname)
			cur.execute(sqlorder)
			records = cur.fetchall()
			for row in records:
			    for r in row:
			        filestr = r
			if filestr:
				newfilesetstr = filestr + filesetstr
				sqlorder = "update %s set filestr = '%s' where wordname = '%s'" %(self.wftable,newfilesetstr,wordname)			
				cur.execute(sqlorder)
				# print('filestr', filestr)
			else:
				sqlorder = "INSERT INTO %s VALUES(0,'%s','%s')" %(self.wftable, wordname, filesetstr)
				# print('not exists')
				cur.execute(sqlorder)
		cur.close()
		cnx.commit()
		cnx.close()

	def getFilestrfWF(self,word):
		filestr = ''
		cnx = connector.connect(user= self.user, password = self.pwd, host = self.host)
		cur = cnx.cursor()
		sqlorder = "USE %s" %self.basename 
		cur.execute(sqlorder)
		sqlorder = "select filestr from %s where wordname = '%s'" %(self.wftable,word)
		cur.execute(sqlorder)
		records = cur.fetchall()
		cur.close()
		cnx.commit()
		cnx.close()
		if records:
			filestr = records[0][0]
		return filestr
# basename = 'whutsearch'
# urltable = 'urltable'
# db = MySqlBase()
# visitedlist = db.getVisitedUrlList()
# print('visitedlist: ', visitedlist)
# # db.insertUrltable(4,'originalurl','shorturl')
# maxid = db.getMaxUrlID()
# print("maixid: ", maxid)
# filestr = db.getFilestrfWF('应用')
# print('filestr', filestr)

# oriurl = db.getOriUrlFSUrl(filestr[0:-1])
# print('originalurl', oriurl)

# oriurllist = db.getOriginalUrllist()
# print('oriurllist', oriurllist)
# shorturl = db.getShortUrlList()
# print('shorturl: ', shorturl)
# visitedset = {'shorturl'}
# db.updateVisitedFlag(visitedset)

