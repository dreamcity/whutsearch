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

	def createDB(self):
		cnx = connector.connect(user= self.user, password = self.pwd, host = self.host)
		cur = cnx.cursor()
		sqlorder = "CREATE DATABASE IF NOT EXISTS %s" %self.basename
		cur.execute(sqlorder)
		sqlorder = "USE %s" %self.basename
		cur.execute(sqlorder)
		sqlorder = "CREATE TABLE IF NOT EXISTS %s (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,originalurl VARCHAR(200),shorturl VARCHAR(10))" %self.urltable
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

	def updateUrltable(self,urlid,orignalurl,shorturl):
		cnx = connector.connect(user= self.user, password = self.pwd, host = self.host)
		cur = cnx.cursor()
		sqlorder = "USE %s" %self.basename
		cur.execute(sqlorder)
		sqlorder = "INSERT INTO %s VALUES(%d,'%s','%s')" %(self.urltable, urlid, orignalurl,shorturl)
		cur.execute(sqlorder)					
		cur.close()
		cnx.commit()
		cnx.close()

	def getShortUrlList(self):
		shortUrllist = []
		cnx = connector.connect(user= self.user, password = self.pwd, host = self.host)
		cur = cnx.cursor()
		sqlorder = "USE %s" %self.basename
		cur.execute(sqlorder)
		sqlorder = "select  %s from %s " %('shorturl',self.urltable)
		cur.execute(sqlorder)
		records = cur.fetchall()
		cur.close()
		cnx.commit()
		cnx.close()
		for row in records:
		    for r in row:
		        shortUrllist.append(r)
		return shortUrllist

# basename = 'whutsearch'
# urltable = 'urltable'
# db = MySqlBase()
# db.createDB()
# filenamelist = db.getFilenameList()
# print(filenamelist)
# fiel = list(filenamelist)
# print(fiel)
# maxid = db.getMaxUrlID()
# urlid = maxid +1
# db.updateUrltable(urlid,'http://i.whut.edu.cn//xyxw/zhxy/201409/t20140928_120522.shtml','6vyv6')
# print('maxid', maxid)
