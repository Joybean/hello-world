#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import urllib.request  
import re
from pathlib import Path

def parsePage(url):
	while True:
		try:
			page = urllib.request.urlopen(url, timeout=3)
			content = page.read().decode(encoding='utf-8',errors='strict')
			break;
		except:
			print('request page %s timeout, try again' % url )
	patterns = {
		'name' : 'data-last_month="">(.*?)</a>',
		'rate' :'(\d+.\d+)\D+</span>%<br/>预期年化收益',
		'project' : '<li class="transfer-index-thire-left-text-right">\s+(.+)\s+</li>',
		'priceUnit' : '<span class="transfer-index-thire-left-text-color1">(\d+.\d+)</span>',
		'lockPeriod' : '<span class="transfer-index-thire-left-text-color1">(\d+)</span>',
		'dueDate' : '<span style="line-height:30px;">(.*?)</span><br/>销售截止时间'
	}
	results = {}
	for pattern in patterns.items():
		regex = re.compile(pattern[1])
		results[pattern[0]] = regex.findall(content, re.S)
	return results

def printResults(results):
	for i in range(len(results['name'])):
		for (key, value) in results.items():
			print(key + " : " + value[i])

def outputToCsv(results, file):
	for i in range(len(results['name'])):
		line = []
		for (key, value) in results.items():
			line.append(value[i])
		file.write(','.join(line) + '\n')
	file.flush()

def getTotalPage(url): 
	page = urllib.request.urlopen(url)
	content = page.read().decode(encoding='utf-8',errors='strict')
	totalPagePattern = '<a class="end" href=".*?">(\d+)</a>'
	regex = re.compile(totalPagePattern)
	result = regex.findall(content)
	return int(result[0])

#支持断点续传
def getStartPage():
	filename = 'GetData.start'
	path = Path(filename)
	if path.exists():		
		with open(filename, 'r') as file:
			line = file.readline()
			if line:
				return int(line) + 1
	return 0
#支持断点续传
def saveStartPage(pageId):
	with open('GetData.start', 'w+') as file:
		file.write(str(pageId))

startPage = getStartPage()
totalPage = getTotalPage('http://www.solarbao.com/licai/catid0')

print("totalPages: %d" % totalPage)
catId = 0
totalResults = {}
totalResults[catId] = {}
#支持断点续传
with open('GetData.csv', 'a') as file : 
	file.write('name,rate,project,price,lockPeriod,dueDate\n')
	for pageId in range(startPage, totalPage):
		url = 'http://www.solarbao.com/licai/catid%d/p%d.html' % (catId, pageId+1)
		totalResults[catId][pageId] = parsePage(url)
		outputToCsv(totalResults[catId][pageId], file)
		print('crawl page: %s records:%d' % (url, len(totalResults[catId][pageId]['name'])))
		saveStartPage(pageId)