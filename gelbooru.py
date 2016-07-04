from tag_parser import tag_parser
import sys
import urllib2
import xml.etree.ElementTree as xtree
import random

def scrape(tags):
	tags = tag_parser(tags)
	
	sys.stdout.write("wow webscrape time ::: %s..." % tags)
	link = "http://gelbooru.com/index.php?page=dapi&s=post&q=index&pid=%s&tags=" % (self.MAXGEL/10 + 1)
	for t in tags:
		link+=(t+"+")

	xmlstr = urllib2.urlopen(link).read().encode("ascii","ignore")
	root = xtree.fromstring(xmlstr)
	total = int(root.attrib["count"])
	if total < 1: return {}
	start = random.randint(0, total/100)
	link+="&pid=%i" %(start)
	xmlstr = urllib2.urlopen(link).read().encode("ascii","ignore")
	root = xtree.fromstring(xmlstr)
	
	cc = choice(root).attrib
	cc["total_resluts"] = total
	return cc
	
def random(tags):
	api_link = "http://gelbooru.com/index.php?page=dapi&s=post&q=index&id=%s" %(random.randint(0, self.MAXGEL))
	xmlstr = urllib2.urlopen(api_link).read().encode("ascii","ignore")
	root = xtree.fromstring(xmlstr)
	gay = []
	for child in root:
		gay.append(dict((attribute, value) for attribute, value in child.items()))
		
	if not gay: 
		return {}
	
	c = choice(gay)
	c["total_resluts"] = self.MAXGEL
	return c
	
		
def link(id):
	return "http://gelbooru.com/index.php?page=post&s=view&id=%s" % id 