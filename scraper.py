import sys
import requests
#from requests_oauthlib import OAuth1
import xml.etree.ElementTree as xtree
import random

# tag parsing helper function
def tag_parser(tags):
	tlen = len(tags)
	newtags = []
	t = 0
	while t < tlen:
		tt = tags[t]
		if t > 0 and t < tlen-1 and tt == "|":
			cc = random.choice((-1,1))
			tt = tags[t+cc]
			if cc == -1: t+=1
			if random.choice((0, 1)) == 0: newtags[-1] = tt
		else: newtags.append(tt)
		t+=1

	return {}.fromkeys(newtags).keys()

# scraper classes

class Scraper:
	def scrape(self, tags):
		raise NotImplementedError("scrape should scrape from the website and return a dict with 'tag':'info' key:value pairs")
	def random(self):
		raise NotImplementedError("random should pick a random picture ideally using an ID number (should be faster than linker with zero args) and return a string ")
	def link(self, id):	
		raise NotImplementedError("link should use the <id> parameter and return link with that ID")
	

class GelbooruScraper(Scraper):
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
		

# pixiv's interface is SHIT! also all the tags are in nipponese.
# i will implement this if i get enough demand for it and some example syntaxes (translating the tags would be a bad idea i m o)
# pixiv random might be possible though
class PixivScraper(Scraper):
	def __init__(self, username, password):
		pass
		'''
		# login
		auth_url = "https://oauth.secure.pixiv.net/auth/token"
        auth_data = OAuth1('bYGKuGVw91e0NMfPGp44euvGt59s','HP3RmkgAmEGro0gn1x9ioawQE8WMfvLXDz3ZqxpK', username, password)
		requests.get(auth_url, auth=auth_data)
		'''
		
	def scrape(self, tags):
		pass
		
	def random(self, tags):
		pass
		
	def link(self, id):
		pass