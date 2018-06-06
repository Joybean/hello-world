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
			ratio = difflib.SequenceMatcher(None, module['title'], os.path.basename(subFolder)).ratio()
			if maxRatio < ratio:
				maxRatio = ratio
				matchedFolder = subFolder
		print(matchedFolder)
		indexClips(module['clips'], os.path.join(folder, matchedFolder))
		os.rename(os.path.join(folder, matchedFolder), '%s/%d-%s' % (folder, iModule, os.path.basename(matchedFolder)))

def indexClips(clips, folder):
	files = os.listdir(folder)
	iClip = 0
	for clip in clips:
		iClip += 1
		maxRatio = -1
		for file in files:
			ratio = difflib.SequenceMatcher(None, clip['title'], os.path.basename(file)).ratio()
			if maxRatio < ratio:
				maxRatio = ratio
				matchedFile = file
		print(matchedFile)
		os.rename(os.path.join(folder, matchedFile), '%s/%d-%s' % (folder, iClip, os.path.basename(matchedFile)))

if __name__ == '__main__':	
	course = json.loads(open('/Users/i070599/tmp/Java8_lambda/course_content.json').read())
	indexMoules(course, '/Users/i070599/tmp/Java8_lambda')
