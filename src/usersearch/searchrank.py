import sys
sys.path.append("..")
import dboperate.dbprocess as dboper
import jieba
import networkx as nx
import os

# import jieba.analyse

class SearchPage(object):
	"""docstring for SearchPage"""
	def __init__(self, userstr):
		super(SearchPage, self).__init__()
		self.userstr = userstr
		self.segwordlist = []
		self.filesetlist = []
		self.fileweightdict = {}
		self.topnfile = []
		self.dbp = dboper.MySqlBase()
		self.DG = nx.DiGraph()
		self.loadNGdata()
		self.run()

	def getSegwordList(self):
		segword = jieba.cut_for_search(self.userstr)
		segwordstr =  '|'.join(segword)
		self.segwordlist = segwordstr.split('|')

	def getFilesetList(self):
		filesetstr = ''
		for word in self.segwordlist:
			# result = 'select filename from db' 
			result = self.dbp.getFilestrfWF(word) 
			filesetstr = filesetstr + result
		self.filesetlist = filesetstr.split('|')[0:-1]
	
	def loadNGdata(self):
		filefloder = r'../data/'
		filename = filefloder + 'whutgraph.yaml'
		# filename = 'whutgraph.yaml'
		try:
			self.DG = nx.DiGraph()
			self.DG = nx.read_yaml(filename)
		except Exception:
			print('Error, the graph data isnot exist!!!')
			exit()

	def getNodesValue(self,tinyurl):
		value = 0
		nodename = self.dbp.getOriUrlFSUrl(tinyurl)
		# print('nodename', nodename)
		value = self.DG.in_degree(nodename,weight='weight')
		# print('value', value)	
		return value

	def getFileWeightDict(self):
		for filename in self.filesetlist:
			# print('filename', filename)
			# print('graph0:', self.fileweightdict)
			if filename in self.fileweightdict.keys():
				# print('graph11:', self.fileweightdict)
				self.fileweightdict[filename][0] += 1
				self.fileweightdict[filename][1] *= 2
				# print('graph1:', self.fileweightdict)
			else:
				value = self.getNodesValue(filename)
				# print('values', value)
				# value = "ng.innodedegree(filename)"
				self.fileweightdict[filename] = []
				self.fileweightdict[filename].append(1)
				self.fileweightdict[filename].append(value)

	def getTopNfile(self,n=3):
		filelist = []
		filewdict = self.fileweightdict
		resultdict = sorted(filewdict.items(),key= lambda filewdict:filewdict[1],reverse=True)
		# print('resultdict0', resultdict)
		for item in resultdict:
			filename = item[0]
			filelist.append(filename)
		self.topnfile = filelist[0:n]

	def run(self):
		self.getSegwordList()
		self.getFilesetList()
		self.getFileWeightDict()
		self.getTopNfile()

# inputstr = '武汉理工大学'

# sr = SearchPage(inputstr)
# print('self.segwordlist', sr.segwordlist)
# print('self.filesetlist', sr.filesetlist)
# print('srank', sr.topnfile)
# nodes = sr.DG.nodes()[0:20]

# print('nodes', nodes)

# value = sr.getNodesValue('867nv')
# print('value', value)

# sr.getFileWeightDict()
# print('value', sr.fileweightdict)