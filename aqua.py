#!/usr/bin/env python
# encoding=utf8  
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

### external libs
import socket
from threading import Thread

### aqua libs
import ircbot

def pinger(bot):
	pingas = []
	while bot.pingable:
		pdat = bot.ping()
		pingas.append(Thread(target=bot.process_data, args=(pdat,)))
		pingas[-1].start()
		pingas = [t for t in pingas if t.is_alive()]
			
def sender(bot):
	while bot.pingable:
		m = raw_input("\t\tmsg> ")
		if m == "/quit": 
			bot.quit()
			sys.exit(9002)
		
		if m == "/join":
			c = raw_input("\t\t join which channel ?? > ")
			bot.join(c)
			
		c = raw_input("\t\tchannel> ")
		bot.msg(c, m)	


if __name__ == "__main__":
	chans = ["#savespam","#aquatest"]
	aqua = ircbot.Bot("aqua-sama", "irc.esper.net", 6667, chans, "mizu-chan")
	
	if(not aqua.connect()):
		print "epic fail : ("
		quit()
	
	print "starting the threads!!"
	
	pt = Thread(target=pinger, args=(aqua,))
	st = Thread(target=sender, args=(aqua,))
	
	print "starting ping thread! %s" % pt.name
	pt.start()
	print "starting send thread! %s" % st.name
	st.start()
	