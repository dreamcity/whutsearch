# -*- coding: utf-8 -*-
import sys
sys.path.append('./netspider')
sys.path.append('./dboperate')
sys.path.append('./fileoperate')

import netspider.whutspider as ws
import fileoperate.fileprocess

starturl = r'http://i.whut.edu.cn/'
wsp = ws.WhutSpider(starturl)
# wsp.saveUrlGraph()