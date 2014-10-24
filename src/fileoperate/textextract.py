# -*- coding=utf-8 -*-

import re

re_title = re.compile(r'<title>(.*?)</title>', re.I|re.U|re.S)
re_body = re.compile(r'<body[^>]*>.*</body>', re.I|re.U|re.S)
re_doc_type = re.compile(r'<!DOCTYPE.*?>', re.I|re.U|re.S)
re_comment = re.compile(r'<!--.*?-->', re.I|re.U|re.S)
re_js = re.compile(r'<script.[^>]*>.*?</script>', re.I|re.U|re.S)
re_css = re.compile(r'<style[^>]*>.*?</style>', re.I|re.U|re.S)
re_special = re.compile(r'&.{2,8};|&#.{2,8};', re.I|re.U|re.S)
re_other = re.compile(r'<[^>]*>', re.I|re.U|re.S)

BLOCK_HEIGHT = 3
THRESHOLD = 90

class TextExtract(object):
	"""docstring for TextExtract"""
	def __init__(self, new_html, join=True):
		self.html = new_html
		self.join = join
		self.text_start = 0
		self.text_end = 0
		self.text_body = ''
		self.block_len = []
		self.title = ''
		self.content = ''

		self.extract()

	def extract(self):
		self.getExtractTitle()
		self.getExtractBody()
		self.removeTags()
		self.getExtractText()

	def getExtractTitle(self):
		m = re_title.search(self.html)
		if m:
			self.title = m.group(1)

	def getExtractBody(self):
		m = re_body.search(self.html)
		if m:
			self.text_body = m.group()

	def removeTags(self):
		self.text_body = re_doc_type.sub('', self.text_body)
		self.text_body = re_comment.sub('', self.text_body)
		self.text_body = re_js.sub('', self.text_body)
		self.text_body = re_css.sub('', self.text_body)
		self.text_body = re_special.sub('', self.text_body)
		self.text_body = re_other.sub('', self.text_body)

	def getExtractText(self):
		# print('getExtractText')
		lines = self.text_body.split('\n')
		# print('lines', lines)
		line_len = len(lines)
		for index in range(0, line_len):
			lines[index] = re.sub(r'\s+', ' ', lines[index]).strip()
			# print('data', lines[index])
		for index in range(1, line_len-1):
			if len(lines[index]) > 0 and len(lines[index]) < 30 and 0 == len(lines[index-1]) and 0 == len(lines[index+1]):
				lines[index] = ''
		for index in range(0, len(lines)-BLOCK_HEIGHT):
			line_len = 0
			for shift in range(0, BLOCK_HEIGHT):
				line_len += len(lines[index+shift])
			self.block_len.append(line_len)
 
		self.text_start = self.getTextStart(0)
		self.text_end = 0
		if (0 == self.text_start):
		 	# self.content = 'nothing can find'
		 	self.content = ''
		else:
			# print('self.join',self.join)
			if self.join:
			 	line_lens = len(lines)
			 	while self.text_end < line_lens:
			 		self.text_end = self.getTextEnd(self.text_start)
			 		self.content += self.get_text(lines)
			 		self.text_start = self.getTextStart(self.text_end)
			 		if  0 == self.text_start:
			 			break
			 		self.text_end = self.text_start
			else:
				 self.text_end = self.getTextEnd(self.text_start)
				 self.content += self.get_text(lines)

	def getTextStart(self,index):
		blk_len = len(self.block_len)
		for i in range(index, blk_len-1):
			if self.block_len[i] > THRESHOLD and self.block_len[i+1] > 0:
				return i
		return 0

	def getTextEnd(self, index):
		blk_len = len(self.block_len)
		for index in range(index, blk_len-1):
			if 0== self.block_len[index] and 0== self.block_len[index+1]:
				return index
		return blk_len-1

	def get_text(self, lines):
		strtmp = ''
		# print('text_start',self.text_start)
		# print('text_end',self.text_end)
		for index in range(self.text_start, self.text_end):
			strtmp += lines[index]+'\n'
		return strtmp


# filename = '1234.html'
# file_object = open(filename,'r', encoding='utf-8')
# filePage = file_object.read()
# file_object.close()
# text_extract = TextExtract(filePage)

# file_object = open('datainfo8.txt', 'w', encoding='utf-8')
# file_object.write(text_extract.title)
# file_object.close()
# file_object = open('datainfo.txt', 'w+', encoding='utf-8')
# file_object.write(text_extract.content)
# file_object.close()