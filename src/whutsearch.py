# -*- coding: utf-8 -*-
import sys
sys.path.append('./netspider')
sys.path.append('./dboperate')
sys.path.append('./fileoperate')

import netspider.whutspider as ws
import fileoperate.fileprocess as fpro

starturl = r'http://i.whut.edu.cn/'

wsp = ws.WhutSpider(starturl)
wsp.saveUrlGraph()
fp = fpro.FileProcess()

# print('shorturl', fp.tinyurllist)
# print('filelist', fp.txtfilelist)
# print('fileworddict', fp.fileworddict)
# print('wordset', fp.wordset)
print('wordfiledict', fp.wordfiledict)
