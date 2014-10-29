# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
import spiderqueue as squeue
import spiderhttp as shttp
import dboperate.dbprocess as dbp
import networkx as nx
import matplotlib.pyplot as plt
import re
import os

class WhutSpider(object):
	"""docstring for WhutSpider"""
	def __init__(self,starturl):
		# self.starturl = starturl
		self.DBP = dbp.MySqlBase()
		self.SH = shttp.SpiderHttp()
		self.todo_queue = squeue.Queue()
		self.todo_queue.enqueue(starturl)
		self.DG = nx.DiGraph()

		filefloder = r'../data/'
		filename = filefloder + 'whutgraph.yaml'
		# self.DG=nx.read_yaml('whutgraph.gml')
		if os.path.exists(filename):
			self.DG=nx.read_yaml(filename)
		self.visited_set = set(self.DBP.getOriginalUrllist())
		print('visited_set',self.visited_set)
		self.wideSpider()
		
	def urlFilter(self, urllist):
		urlFilterList = []
		pattern = re.compile(r'http://.*whut.edu.cn.*',re.M)
		for url in urllist:
			match = pattern.match(url)
			if match:
				urlFilterList.append(url)
			else:
				pass
		return urlFilterList

	def wideSpider(self):
		count = 0
		# print('data', count)
		# while (self.todo_queue.isempty() == False):
		while (self.todo_queue.isempty() == False and count <6):
			# print('count', count)
			count = count +1
			superurl = self.todo_queue.dequeue()
			urllist = self.SH.getUrlList(superurl)
			urlFilterList = self.urlFilter(urllist)
			for urlstr in urlFilterList:
				self.todo_queue.enqueue(urlstr)		
			# print('superurl ', superurl)
			if superurl in self.visited_set:
				# print('in')
				continue
			else:
				self.SH.downloadPage(superurl)
				self.visited_set.add(superurl)
				if superurl in self.DG:
					nodeValue = self.DG.in_degree(superurl,weight='weight')
				else:
					nodeValue = 1
				# urllist = self.SH.getUrlList(superurl)
				# urlFilterList = self.urlFilter(urllist)
				urlnums = len(urlFilterList)
				if urlnums == 0:
					# print('length')
					continue
				urlEdgeWeight = nodeValue/(urlnums+1)
				for urlstr in urlFilterList:
					self.DG.add_weighted_edges_from([(superurl,urlstr,urlEdgeWeight)])
					# self.todo_queue.enqueue(urlstr)
			

	def saveUrlGraph(self):
		filefloder = r'../data/'
		filename = filefloder + 'whutgraph.yaml'
		nx.write_yaml(self.DG,filename)
		nx.draw(self.DG)
		plt.savefig("whutnetwork.png")

