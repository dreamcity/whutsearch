import sys
sys.path.append("..")
import dboperate.dbprocess as dboper
import textextract as tex
import os
import glob
import chardet
import jieba
import jieba.analyse
from optparse import OptionParser

class FileProcess(object):
	"""docstring for FileProcess"""
	def __init__(self):
		self.dbp = dboper.MySqlBase()
		self.tinyurllist = []
		self.txtfilelist = []
		self.fileworddict = {}
		self.wordset = {''}
		self.wordfiledict = {}
		self.topK = 200
		jieba.analyse.set_stop_words("./fileoperate/stopdict.txt")

		self.run()

	def getTinyurlList(self):
		self.tinyurllist = self.dbp.getNVisShortUrllist()	
		self.dbp.updateVisitedFlag(self.tinyurllist)
		# return tinyurllist

	def getFilelist(self):
		htmlfilefloder = r'../data/whuthtmldata/'
		if os.path.exists(htmlfilefloder):
			pass
		else:
			os.mkdir(htmlfilefloder)
		txtfilefloder = r'../data/whuttxtdata/'
		if os.path.exists(txtfilefloder):
			pass
		else:
			os.mkdir(txtfilefloder)
		# tinyurllist = self.getTinyurlList()
		for tinyurl in self.tinyurllist:
			htmlfilename = htmlfilefloder + tinyurl + '.html'
			htmlpage = open(htmlfilename,'rb').read()
			codingchar=chardet.detect(htmlpage)['encoding']
			filePage = htmlpage.decode(codingchar,'ignore')
			extractText = tex.TextExtract(filePage)
			
			txtfilename = txtfilefloder + tinyurl + '.txt'
			fileObject = open(txtfilename, 'w', encoding='utf-8')
			fileObject.write(extractText.title)
			fileObject.close()
			fileObject = open(txtfilename, 'a+', encoding='utf-8')
			fileObject.write(extractText.content)
			fileObject.close()
			
			self.txtfilelist.append(txtfilename)
		# return 
	
	def getWordlist(self,filename):
		htmlpage = open(filename,'rb').read()
		codingchar=chardet.detect(htmlpage)['encoding']
		filePage = htmlpage.decode(codingchar,'ignore')
		topK = 200
		# filePage = open(filename,'r', encoding='utf-8').read()
		tags = jieba.analyse.extract_tags(filePage, topK=topK)
		wordlist = list(tags)
		return wordlist

	def getFileWordDict(self):
		for filename in self.txtfilelist:
			tinyurlstr = self.tinyurllist[self.txtfilelist.index(filename)]
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
		# tinyurllist = []
		for word in wordlist:
			# tinyurllist = {''}
			self.wordfiledict[word] = ''
			for tinyurl in self.tinyurllist:
				filewordlist = self.fileworddict[tinyurl]
				if word in filewordlist:
					self.wordfiledict[word] = self.wordfiledict[word] + tinyurl + '|' 
					# self.wordfiledict[word].add(tinyurl) 
		self.dbp.updateWFtable(self.wordfiledict)

	def run(self):
		self.getTinyurlList()
		self.getFilelist()	
		self.getFileWordDict()
		self.getWordSet()
		self.getWordFileDict()
		