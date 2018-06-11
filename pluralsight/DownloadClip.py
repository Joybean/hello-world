#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import sys, os
import re
import json
import requests
from urllib import parse
#import socks
#import socket

#socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1080)
#socket.socket = socks.socksocket

def download(url, headers, saveAs):
	if os.path.exists(saveAs):
		return

	print("download from: " + url)
	required = ['if-range', 'accept', 'accept-encoding', 'accept-language', 'cookie', 'range', 'referer', 'user-agent' ]
	headerDict = {}
	for header in headers:
		if required.count(header['name']) > 0:
			headerDict[header['name']] = header['value']
	req = requests.get(url, headers=headerDict, stream=True)
	
	folder = os.path.dirname(saveAs)
	if not os.path.exists(folder):
		os.makedirs(folder)

	tmp = saveAs + '.tmp'
	with open(tmp, 'wb') as file:
		for chunk in req.iter_content(chunk_size=128 * 1024): 
			if chunk:
				file.write(chunk)
				file.flush()
				print('=' , end='', flush=True)
	os.rename(tmp, saveAs)
	print('\nsaved to: ' + saveAs)

def getModuleAndTitle(entry):
	moduleTitle = ''
	title = ''
	if 'queryString' in entry['request']:
		for queryString in entry['request']['queryString']:
			if queryString['name'] == 'moduleTitle' or queryString['name'] == 's:meta:moduleTitle':
				moduleTitle = parse.unquote(queryString['value']).replace(':', '').replace('/', '').replace(' ', '')
			if queryString['name'] == 'title' or queryString['name'] == 's:meta:title':
				title = parse.unquote(queryString['value']).replace(':', '').replace('/', '').replace(' ', '')
	return moduleTitle, title

def scanHarAndDownload(harFile):
	folder = os.path.dirname(harFile)
	saveAsList = []
	urlList = []
	headersList = []
	with open(harFile) as urls:
		har = json.loads(open(harFile).read())
		saveAs = folder
		for entry in har['log']['entries']:		
			mT, t = getModuleAndTitle(entry)
			saveAs = '%s/%s/%s.mp4' % (folder, mT, t)
			if mT != '' and t != '' and saveAsList.count(saveAs) == 0:
				saveAsList.append(saveAs)

			if re.search('(1280x720.mp4|1024x768.mp4)', entry['request']['url']) != None \
				and urlList.count(entry['request']['url']) == 0:
				urlList.append(entry['request']['url'])
				headersList.append(entry['request']['headers'])

	if len(saveAsList) == len(urlList) == len(headersList):
		count = len(saveAsList)
	else:
		print('len(saveAsList): %d; len(urlList): %d; len(headersList): %d' % (len(saveAsList), len(urlList), len(headersList)))
		return
	print('%d clips are found.')
	for i in range(count):
		download(urlList[i], headersList[i], saveAsList[i])

if __name__ == '__main__':
	scanHarAndDownload(sys.argv[1])