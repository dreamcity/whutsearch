# -*- coding: utf-8 -*-
import sys
sys.path.append('./netspider')
sys.path.append('./dboperate')
sys.path.append('./fileoperate')
sys.path.append('./usersearch')

import netspider.whutspider as ws
import fileoperate.fileprocess as fpro
import usersearch.searchrank as sr

# starturl = r'http://i.whut.edu.cn/'
# wsp = ws.WhutSpider(starturl)
# wsp.saveUrlGraph()
# fp = fpro.FileProcess()

inputstr = '武汉理工大学'
srank = sr.SearchPage(inputstr)
print('srank', srank.topnfile)

# 'pbq8b 6vyv6 25t52'
# srank.topnfile
# print('shorturl', fp.tinyurllist)
# print('filelist', fp.txtfilelist)
# print('fileworddict', fp.fileworddict)
# print('wordset', fp.wordset)
# print('wordfiledict', fp.wordfiledict)
