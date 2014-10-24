# -*- coding: utf-8 -*-
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
		for row in records:
		    for r in row:
		        maxid = r
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

	def updateVisitedFlag(self,visitedset):
		cnx = connector.connect(user= self.user, password = self.pwd, host = self.host)
		cur = cnx.cursor()
		sqlorder = "USE %s" %self.basename 
		cur.execute(sqlorder)
		visitedlist = list(visitedset) 
		for visitedenum in visitedlist:
			sqlorder = "update urltable set visitedflag = True where shorturl = %s" %(visitedenum)
			cur.execute(sqlorder)					
		cur.close()
		cnx.commit()
		cnx.close()

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
		    for r in row:
		        originalUrllist.append(r)
		return originalUrllist

	def getVisitedUrllist(self):
		visitedUrllist = []
		cnx = connector.connect(user= self.user, password = self.pwd, host = self.host)
		cur = cnx.cursor()
		sqlorder = "USE %s" %self.basename
		cur.execute(sqlorder) 
		sqlorder = "select  %s from %s where visitedflag = True" %('originalurl',self.urltable)
		cur.execute(sqlorder)
		records = cur.fetchall()
		cur.close()
		cnx.commit()
		cnx.close()
		for row in records:
		    for r in row:
		        visitedUrllist.append(r)
		return visitedUrllist

# basename = 'whutsearch'
# urltable = 'urltable'
# db = MySqlBase()
# visitedlist = db.getVisitedUrlList()
# print('visitedlist: ', visitedlist)
# # db.insertUrltable(4,'originalurl','shorturl')
# maxid = db.getMaxUrlID()
# print("maixid: ", maxid)
# shorturl = db.getShortUrlList()
# print('shorturl: ', shorturl)
# visitedset = {'shorturl'}
# db.updateVisitedFlag(visitedset)
