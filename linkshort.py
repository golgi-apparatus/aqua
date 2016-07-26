#!/usr/bin/env python
# encoding=utf8  
import urllib2, json, urllib
def waaai_short(url):
	wurl = 'http://api.waa.ai/shorten?url=%s' % url 
	print wurl
	wreq = urllib2.Request(wurl, headers={'User-Agent' : "aqua-chan"})
	wlink = urllib2.urlopen(wreq)
	wj = json.loads(wlink.read())
	print wj
	return wj['data']["url"] if wj["success"] else "waa.ai fail : ("
	
def isgd_short(url):
	url = urllib.quote(url)
	iurl = "https://is.gd/create.php?format=simple&url=%s" % url
	print iurl
	ireq = urllib2.Request(iurl, headers={'User-Agent' : "aqua-chan"})
	ilink = urllib2.urlopen(ireq)
	return ilink.read()