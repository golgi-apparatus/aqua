#!/usr/bin/env python
# encoding=utf8  
from datetime import datetime
def now():
	n = datetime.now()
	return "[%04i-%02i-%02i %02i:%02i:%02i] " %(n.year, n.month, n.day, n.hour, n.minute, n.second)
	
def plog(f, s):
	n = now()
	print(n+s)
	with open(f, "a") as l:
		l.write(n+s+"\n")
	
main_log = "aqua_debug.log"