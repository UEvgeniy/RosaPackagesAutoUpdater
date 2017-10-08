#!/usr/bin/python

# class is a wrapper for items in mib-report
# each item containes distro, version and URL
class Item:
	def __init__(self, distro, version, url):
		self.distro = distro
		self.version = version
		self.url = url
		
	def __str__(self):
		return "[distro: " + self.distro + ", version: "+ self.version + ", URL: " + self.url +"]"
	
	# self < other
	def __lt__(self, other):
		if isinstance(other, Item):
			return self.version < other.version
		return False
	
	# self > other
	def __gt__(self, other):
		if isinstance(other, Item):
			return self.version > other.version
		return False	
	
	
	
	
	
	
	
	
	
	