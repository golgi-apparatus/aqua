from tag_parser import tag_parser
import sys
import requests
import xml.etree.ElementTree as xtree
import random
import pixiv

class GelbooruScraper:
	MAXGEL = 3000000
	def __init__(self):
		print "init gelbooru..."
		gel_home = "http://gelbooru.com/index.php?page=dapi&s=post&q=index"
		xmlstr = requests.get(gel_home).text
		root = xtree.fromstring(xmlstr)
		self.MAXGEL = int(root.attrib["count"])
		print self.MAXGEL
		
	def scrape(self, tags):
		tags = tag_parser(tags)
		
		sys.stdout.write("wow webscrape time ::: %s..." % tags)
		link = "http://gelbooru.com/index.php?page=dapi&s=post&q=index&pid=%s&tags=" % (self.MAXGEL/10 + 1)
		for t in tags:
			link+=(t+"+")

		xmlstr = requests.get(link).text
		root = xtree.fromstring(xmlstr)
		total = int(root.attrib["count"])
		if total < 1: return {}
		start = random.randint(0, total/100)
		link+="&pid=%i" %(start)
		xmlstr = requests.get(link).text
		root = xtree.fromstring(xmlstr)
		
		cc = random.choice(root).attrib
		cc["total_resluts"] = total
		return cc
		
	def random(self, tags):
		api_link = "http://gelbooru.com/index.php?page=dapi&s=post&q=index&id=%s" %(random.randint(0, self.MAXGEL))
		xmlstr = requests.get(api_link).text
		root = xtree.fromstring(xmlstr)
		gay = []
		for child in root:
			gay.append(dict((attribute, value) for attribute, value in child.items()))
			
		if not gay: 
			return {}
		
		c = random.choice(gay)
		c["total_resluts"] = self.MAXGEL
		return c
		
			
	def link(self, id):
		return "http://gelbooru.com/index.php?page=post&s=view&id=%s" % id 
		
