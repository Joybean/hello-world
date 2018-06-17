#!/usr/bin/env python

import os, sys
import difflib
import json

def indexMoules(course, folder):
	subFolders = os.listdir(folder)
	iModule = 0
	for module in course['modules']:
		iModule += 1
		maxRatio = -1
		for subFolder in subFolders:
			if os.path.isdir(os.path.join(folder, subFolder)):
				ratio = difflib.SequenceMatcher(None, module['title'], os.path.basename(subFolder)).ratio()
				print(ratio)
				if maxRatio < ratio:
					maxRatio = ratio
					matchedFolder = subFolder
		indexClips(module['clips'], os.path.join(folder, matchedFolder))
		if os.path.exists(os.path.join(folder, matchedFolder)):
			os.rename(os.path.join(folder, matchedFolder), '%s/%d-%s' % (folder, iModule, os.path.basename(matchedFolder)))

def indexClips(clips, folder):
	files = os.listdir(folder)
	iClip = 0
	for clip in clips:
		iClip += 1
		maxRatio = -1
		for file in files:
			if os.path.isfile(os.path.join(folder, file)):
				ratio = difflib.SequenceMatcher(None, clip['title'], os.path.basename(file)).ratio()
				if maxRatio < ratio:
					maxRatio = ratio
					matchedFile = file
		if os.path.exists(os.path.join(folder, matchedFile)):
			os.rename(os.path.join(folder, matchedFile), '%s/%d-%s' % (folder, iClip, os.path.basename(matchedFile)))

def getCourseContent(response):
	if 'content' in response and 'text' in response['content']:
		course = json.loads(response['content']['text']) 
		if 'data' in course and 'rpc' in course['data'] and 'bootstrapPlayer' in course['data']['rpc'] \
			and 'course' in course['data']['rpc']['bootstrapPlayer'] and 'modules' in course['data']['rpc']['bootstrapPlayer']['course']:
			return course['data']['rpc']['bootstrapPlayer']['course']

if __name__ == '__main__':
	folder = sys.argv[1]
	files = os.listdir(folder)
	for file in files:
		if file.endswith('.har'):
			print("scan file: " + os.path.join(folder, file))
			har = json.loads(open(os.path.join(folder, file)).read())
			for entry in har['log']['entries']:
				if entry['request']['url'] == 'https://app.pluralsight.com/player/api/graphql' \
					and entry['request']['method'] == 'POST':
					course = getCourseContent(entry['response'])
					if course:
						indexMoules(course, folder)
						exit()