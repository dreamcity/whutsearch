import sys
sys.path.append("..")
import dboperate.dbprocess as dboper
import textextract as tex
import os
import jieba
import jieba.analyse
from optparse import OptionParser

class FileProcess(object):
	"""docstring for FileProcess"""
	def __init__(self):
		self.dbp = dboper.MySqlBase()
		self.tinyurllist = []
		self.filelist = []
		self.fileworddict = {}
		self.wordset = {''}
		self.wordfiledict = {}
		self.topK = 200
		jieba.analyse.set_stop_words("stopdict.txt")

	def getTinyurlList(self):
		# 这个地方需要改，最好用联合查询，得到没有处理的tinyurllist
		self.tinyurllist = self.dbp.getShortUrlList()
		# return tinyurllist

	def getFilelist(self):
		if os.path.exists('whuttextdata'):
			pass
		else:
			os.mkdir('whuttextdata')
		# tinyurllist = self.getTinyurlList()
		for tinyurl in self.tinyurllist:
			filename = './whuthtmldata/' + tinyurl + '.html'
			fileObject = open(filename,'r', encoding='utf-8')
			filePage = fileObject.read()
			extractText = tex.TextExtract(filePage)
			fileObject.clost()
			filename = './whuttextdata/' + tinyurl + '.txt'
			fileObject = open('filename', 'w', encoding='utf-8')
			fileObject.write(extractText.title)
			fileObject.close()
			fileObject = open('filename', 'w+', encoding='utf-8')
			fileObject.write(extractText.content)
			fileObject.close()
			self.filelist.append(filename)
		# return 
	
	def getWordlist(self,filename):
		filePage = open(filename,'r', encoding='utf-8').read()
		tags = jieba.analyse.extract_tags(filePage, topK=topK)
		wordlist = list(tags)
		return wordlist

	def getFileWordDict(self):
		for filename in self.filelist:
			tinyurlstr = self.tinyurllist[self.filelist.index(filename)]
			wordlist = self.getWordlist(filename)
			self.fileworddict[tinyurlstr] = wordlist
	
	def getWordSet(self):
		wordlist = []
		mulwordlist = self.fileworddict.values()
		for word in mulwordlist:
			wordlist.extend(word)
		self.wordset = set(wordlist)

	def getWordFileDict(self):
		wordlist = list(self.wordset)
		tinyurllist = []
		for word in wordlist:
			self.wordfiledict[word] = tinyurllist
			for tinyurl in self.tinyurl:
				filewordlist = self.fileworddict[tinyurl]
				if word in filewordlist:
					self.wordfiledict[word].append(tinyurl) 
		
