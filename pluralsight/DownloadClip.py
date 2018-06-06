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
	print("download from: " + url)
	required = ['if-range', 'accept', 'accept-encoding', 'accept-language', 'cookie', 'range', 'referer', 'user-agent' ]
	headerDict = {}
	for header in headers:
		if required.count(header['name']) > 0:
			headerDict[header['name']] = header['value']
	req = requests.get(url, headers=headerDict, stream=True)
	
	saveAs = saveAs.replace('/', ' ')
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
				moduleTitle = parse.unquote(queryString['value'])
			if queryString['name'] == 'title' or queryString['name'] == 's:meta:title':
				title = parse.unquote(queryString['value'])
	return moduleTitle, title

def scanHarAndDownload(fileName):
	folder = os.path.dirname(fileName)
	with open(fileName) as urls:
		har = json.loads(open(fileName).read())
		saveAs = folder
		for entry in har['log']['entries']:			
			mT, t = getModuleAndTitle(entry)
			if mT != '' and t != '':
				saveAs = '%s/%s/%s.mp4' % (folder, mT, t)
			if os.path.exists(saveAs) and os.stat(saveAs).st_size == 0:
				os.remove(saveAs)
			if  not os.path.exists(saveAs) \
				and re.search('(1280x720.mp4|1024x768.mp4)', entry['request']['url']) != None :
				download(entry['request']['url'], entry['request']['headers'], saveAs)

if __name__ == '__main__':
	scanHarAndDownload(sys.argv[1])