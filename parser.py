#!/usr/bin/python
import report

# method for extracting necessary imformation (distro, version, URL) from mib-report
def extractItems(s):
	res = []
	
	words = s.split()
	
	# find packages from distros
	for i in range(len(words)):
		if (isURL(words[i]) 
			and isVersion(words[i - 1]) 
			and isDistro(words[i - 2])):
			
			res.append(report.Item(words[i - 2], words[i - 1], words[i]))	
	
	return res

def isURL(s):
	return 'http://' in s and s.endswith('src.rpm')

def isVersion(v):
	import re
	return re.search('\d', v) is not None

def isDistro(d):
	return d[-1] == ':'

# method for getting current rosa version
def getRosaVersion(items):
	for item in items:
		if 'rosa' in item.distro.lower():
			return item.version
	return None

# method for changing substrings in file
def replaceInFile(f, oldV, newV):
	content = f.readlines()
	f.seek(0)
	for line in content:
		f.write(line.replace(oldV, newV))
	f.close()
	
