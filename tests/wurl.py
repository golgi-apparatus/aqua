import urllib2
import json

def waaai_short(url):
	wurl = 'http://api.waa.ai/shorten?url=%s' % url 
	print wurl
	wreq = urllib2.Request(wurl, headers={'User-Agent' : "aqua-chan"})
	wlink = urllib2.urlopen(wreq)
	wj = json.loads(wlink.read())
	print wj
	return wj['data']["url"] if wj["success"] else "waa.ai fail : ("
	
print waaai_short("http://gelbooru.com/index.php?page=post%26s=list%26tags=yaoi+-photo")