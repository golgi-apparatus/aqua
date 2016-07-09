from datetime import datetime

# epic i made an object with like 10 lines

class Log():
	def __init__(self, fn):
		self.fn = fn
	
	def __write__(self, data):
		with open(self.fn, "a") as f:
			now = datetime.now()
			f.write("[%04i-%02i-%02i %02i:%02i:%02i] %s\n" %(now.year, now.month, now.day, now.hour, now.minute, now.second, data))
	
	def write(self, nick, msg):
		self.__write__("<%s> %s" % (nick, msg))
			
	def raw(self, data):
		self.__write__("*** %s" % (data))
			
	def nick(self, nick1, nick2):
		self.__write__("* %s is now known as %s" % (nick1, nick2))
		
	def join(self, nick):
		self.__write__("* %s has joined" % nick) 
		
	def quit(self, nick, reason):
		self.__write__("* %s has quit (Reason: %s)" % (nick, reason)) 
		
	def leave(self, nick, reason):
		self.__write__("* %s has left the channel (Reason: %s)" % (nick, reason)) 