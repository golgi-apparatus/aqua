import urllib2
import linkshort

class Scraper:
	def scrape(self, tags):
		raise NotImplementedError("scrape should scrape from the website and return a dict with 'tag':'info' key:value pairs")
	def random(self):
		raise NotImplementedError("random should pick a random picture ideally using an ID number (should be faster than linker with zero args) and return a string ")

class GelbooruScraper(Scraper):
	def __init__(self):
		pass
		
	def scrape(self, tags):
		tags = tag_parser(tags)
		
		sys.stdout.write("wow webscrape time ::: %s..." % tags)
		link = "http://gelbooru.com/index.php?page=dapi&s=post&q=index&pid=%s&tags=" % (self.MAXGEL/10 + 1)
		for t in tags:
			link+=(t+"+")

		xmlstr = urllib2.urlopen(link).read().encode("ascii","ignore")
		root = xtree.fromstring(xmlstr)
		total = int(root.attrib["count"])
		if total < 1: return {}
		start = randint(0, total/100)
		link+="&pid=%i" %(start)
		xmlstr = urllib2.urlopen(link).read().encode("ascii","ignore")
		root = xtree.fromstring(xmlstr)
		
		cc = choice(root).attrib
		cc["total_resluts"] = total
		return cc
		
	def random(self):
		api_link = "http://gelbooru.com/index.php?page=dapi&s=post&q=index&id=%s" %(randint(0, self.MAXGEL))
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
		
		
		
class PixivScraper(Scraper):
	def __init__(self):
		pass