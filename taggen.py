#!/usr/bin/env python
# encoding=utf8  
import re, requests

## returns the string between two keywords in s 
def finder(s, beg, end, fromloc=0): 
	bloc = s.find(beg, fromloc)+len(beg)
	eloc = s.find(end,bloc)
	return (s[bloc:eloc], eloc) 
	
## split() but returns an iterator instead of a list
def isplit(string):
    return (x.group(0) for x in re.finditer(r"[A-Za-z']+", string))
			f.write("%s %s\n" % (k, v))

def generate_taglist(filewrite=False, fn="gelbooru_tags.txt"):
	if filewrite:
		with open(fn, 'w') as f: 
			f.write("")
	url = "http://gelbooru.com/index.php?page=tags&s=list&sort=desc&order_by=index_count"
	utext = requests.get(url).text
	maxpid = int(finder(utext, 'alt="next">&rsaquo;</a><a href="?page=tags&amp;s=list&amp;pid=','"')[0])
	print maxpid
	tags = {}
	for p in xrange(maxpid/50):
		print p*50
		url = 'http://gelbooru.com/index.php?page=tags&s=list&sort=desc&order_by=index_count&pid=%i' % (p*50)
		utext = requests.get(url).text
		ploc = 0
		for i in xrange(50):
			ct, cloc = finder(utext, "<tr><td>", "<", ploc)
			t, ploc = finder(utext, "index.php?page=post&amp;s=list&amp;tags=", '"', cloc)
			tags[t] = ct
			if filewrite:
				with open(fn, 'a') as f:
					f.write("%s %s\n" % (t, ct))
		
	return tags
		
		
if __name__ == "__main__":
	generate_taglist(filewrite=False, fn="ddd.txt")
	
