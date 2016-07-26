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


if __name__ == "__main__":
	chans = ["#savespam","#aquatest"]
	with open("aqua_controller", "r") as f:
		ctl = f.read()
		
	aqua = ircbot.Bot("aqua-sama", "irc.esper.net", 6667, chans, "mizu-chan", ctl)
	
	if(not aqua.connect()):
		print "epic fail : ("
		quit()
	print "starting!!!"
	
	while aqua.qcode == aqua.RECONNECT: pinger(aqua)