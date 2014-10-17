import whutspider_v2 as ws 
starturl = r'http://i.whut.edu.cn/'
wsp = ws.WhutSpider(starturl)
wsp.wideSpider()
wsp.saveUrlGraph()