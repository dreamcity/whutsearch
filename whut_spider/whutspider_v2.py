import spiderqueue as squeue
import spiderhttp as shttp
import dbprocess as dbp
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
		# self.DG=nx.read_yaml('whutgraph.gml')
		if os.path.exists('whutgraph.yaml'):
			self.DG=nx.read_yaml('whutgraph.yaml')
		self.visited_set = set(self.DBP.getShortUrlList())
		# print('visited_set',self.visited_set)
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
		# while (self.todo_queue.isempty() == False):
		while (self.todo_queue.isempty() == False and count <1):
			superurl = self.todo_queue.dequeue()
			if superurl in self.visited_set:
				continue
			else:
				self.visited_set.add(superurl)
				urllist = self.SH.getUrlList(superurl)
				urlFilterList = self.urlFilter(urllist)
				urlnums = len(urlFilterList)
				if urlnums == 0:
					continue
				if superurl in self.DG:
					nodeValue = self.DG.in_degree(superurl)
				else:
					nodeValue = 1
				urlEdgeWeight = nodeValue/(urlnums+1)

				for urlstr in urlFilterList:
					self.DG.add_weighted_edges_from([(superurl,urlstr,urlEdgeWeight)])
					self.todo_queue.enqueue(urlstr)
				count = count +1

	def saveUrlGraph(self):
		nx.write_yaml(self.DG,"whutgraph.yaml")
		nx.draw(self.DG)
		plt.savefig("whutnetwork.png")

