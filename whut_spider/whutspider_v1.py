import spiderqueue as squeue
import spiderhttp as shttp
import networkx as nx
import matplotlib.pyplot as plt
import re

def urlFilter(urllist):
	urlFilterList = []
	pattern = re.compile(r'http://.*whut.edu.cn.*',re.M)
	for url in urllist:
		match = pattern.match(url)
		if match:
			urlFilterList.append(url)
		else:
			pass
	return urlFilterList

DG = nx.DiGraph()

visited_set = set()
todo_queue = squeue.Queue()

print(todo_queue.isempty())
starturl = r'http://i.whut.edu.cn/'
todo_queue.enqueue(starturl)
print(todo_queue.isempty())

SH = shttp.SpiderHttp()
count = 0
while (todo_queue.isempty() == False and count <3):
	superurl = todo_queue.dequeue()
	if superurl in visited_set:
		continue
	else:
		visited_set.add(superurl)
		urllist = SH.getUrlList(superurl)
		urlFilterList = urlFilter(urllist)
		urlnums = len(urlFilterList)
		if urlnums == 0:
			continue
		if superurl in DG:
			nodeValue = DG.in_degree(superurl)
		else:
			nodeValue = 1
		urlEdgeWeight = nodeValue/(urlnums+1)

		for urlstr in urlFilterList:
			DG.add_weighted_edges_from([(superurl,urlstr,urlEdgeWeight)])
			todo_queue.enqueue(urlstr)
		count = count +1

print(DG.neighbors(starturl))

nx.write_gml(DG,"whutgraph.gml")

nx.draw(DG)
plt.savefig("network.png")
plt.show()
# print(todo_queue.length())
# while (todo_queue.isempty() == False):
# 	url = todo_queue.dequeue()
# 	print(url)

