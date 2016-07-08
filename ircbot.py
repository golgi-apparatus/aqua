#!/usr/bin/env python
# encoding=utf8  
import sys

reload(sys)  
sys.setdefaultencoding('utf8')

### external libs
import socket
from threading import Thread
from time import sleep
import random

### aqua libs
import linkshort
import scraper

## helper
def choicedict(dic):
	return random.choice(list(dic.values()))

def searchkey(diclist, k, v):
	for i in diclist:
		if diclist[k] == v:
			return i
	
	return None
## bot
class Bot:
	# main functions 
	def __init__(self, _nick, _network, _port, _channels, _ident):
		self.network = _network
		self.nick = _nick
		self.channels = _channels
		self.port = _port
		self.irc = None
		self.ident = _ident
		self.user = {}
		self.scrapers = {
			"gelbooru" : scraper.GelbooruScraper()
			#"pixiv"    : scraper.PixivScraper(username="aquachansama",password="aquaisthebest")
		}
		self.currtags = (None, None)
		self.pingable = True
		
		# game stats
		self.game_on = False
		self.gamestats = {  
			"id" : "0",
			"guesses" : 0,
			"tags" : [],
			"current_guess" : "-1"
		}
		
		self.cmdy = {
			"coffee" : self.water,
			"beer" : self.water,
			"cola" : self.water,
			"coke" : self.water,
			"milk" : self.water,
			"soda" : self.water,
			
			"?rand" : self.randpix,
			"?pic" : self.pic,
			"?sfw" : self.sfw,
			"?safe"	: self.safe,
			"?pron" : self.pron,
			"?lewd" : self.lewd,
			
			"?gay" : self.gel_rand,
			"?gel" : self.gel,
			"?gsfw" : self.gsfw,
			"?gsafe" : self.gsafe,
			"?gpron" : self.gpron,
			"?glewd" : self.glewd,
			"?wallpaper" : self.wallpaper,
			"?tags" : self.tags,
			
			"?megumi" : self.megumi,
			"?me"  : self.aqua,
			"?kiyomi" : self.kiyomi,
			"?fozrucix" : self.fozrucix,
			"?saveybot" : self.saveybot,
			"?ayumi" : self.ayumi,
			"?neko" : self.neko,
			
			"?help" : self.help,
			"?bug" : self.bug,
			#"%%seppuku" : self.seppuku,
			
			"$gelgame" : self.game,
			"$gelgame_safe" : self.game_safe,
			"$gelgame_lewd" : self.game_lewd,
			"$gelgame_sfw" : self.game_sfw,
			"$gelgame_pron" : self.game_pron,
			"$pic" : self.gelgame_guess,
			"$tag" : self.gelgame_tag,
			"?scoreboard" : self.gelgame_scoreboard
		
		}
			
	def connect(self):
		self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.irc.settimeout(300)
		print "setting up irc socket...  %s %i" %(self.network, self.port)
		self.irc.connect( (self.network, self.port) )
		print "connecting to irc..."
		print "sending nick info...NICK %s\r\n" %(self.nick)
		self.irc.send("NICK %s\r\n" %(self.nick))
		print "sending user info...USER %s %s %s :%s\r\n" %(self.ident, self.ident, self.ident, self.ident)
		self.irc.send("USER %s %s %s :%s\r\n" %(self.ident, self.ident, self.ident, self.ident))
		print "pinging!!!"
		self.data = self.irc.recv(4096)
		if self.data.find ('PING') != -1:
			self.irc.send ('PONG ' + self.data.split()[1] + '\r\n')
		#print 'PONG ' + self.data.split() [ 1 ] + '\r\n'
		

		
		return True

	def parse_args(self, a, dat):
		if not self.pingable: return ()
		print "parsing some args!"
		datt = dat
		while (datt[0].replace(":","")) != a:
			print str(datt)+" "+a
			datt.pop(0)
		datt.pop(0)
		return datt
	
	def ping(self):
		try:
			if not self.pingable: 
				return
			data = self.irc.recv(4096)
			if data.find ('PING') != -1:
				self.irc.send ('PONG ' + data.split()[1] + '\r\n')
			
			for chan in self.channels:
				self.irc.send("\r\nJOIN " +chan+ "\r\n")
				print "\r\nJOIN " +chan+ "\r\n"		
				
			return data
			
		except socket.error:
			print "::::::::: ((((((((((((((( socket fail"
			sys.exit(2506)
		except socket.timeout:
			print "TTTTTTTTTTTTTTTTTT socket timeout"
			sys.exit(2507)
	
	def join(self, chan):
		if chan in self.channels: return
		self.channels.append(chan)
	
	def leave(self, chan):
		if chan not in self.channels: return
		self.channels.remove(chan)
	
	def process_data(self, data):
		argss = data.split()
		exc, att = argss[0].find("!"), argss[0].find("@")
		self.user["nick"] = argss[0][1:exc] 
		self.user["ident"] = argss[0][exc:att] 
		self.user["host"] = argss[0][att:-1] 

		no_colon = [s.replace(":","") for s in argss]
		print argss
			
		for key in self.cmdy:
			if key in no_colon: 
				chan = argss[0][1:argss[0].find("!")] if argss[2] == self.nick else argss[2]
				nn = argss[0][1:argss[0].find("!")] 
				pa = self.parse_args(key, argss)
				print pa
				self.cmdy[key](chan, pa, nn)
				return
	
	
	def msg(self, chan, send):
		print chan
		print "PRIVMSG %s :%s\r\n" %(chan,send)
		self.irc.send("PRIVMSG %s :%s\r\n" %(chan,send))	
	
	def send_raw(self, send):
		print send
		self.irc.send(send)
	
	# command functions
	def help(self, chan, dum, nick):
		self.msg(chan, "wow do you need some HELP, %s??? here u go!! https://github.com/golgi-apparatus/aqua/blob/master/readme.md" % nick)
	
	def bug(self, chan, dum, nick):
		self.msg(chan, "wanna report a bug or request a new feature, %s??? do it here! https://github.com/golgi-apparatus/aqua/issues" % nick)

	def water(self, chan, dum, nick):
		self.msg(chan, "%s, drink water you dong!!!" % nick)
		
	def photo(self, chan, dum, nick):
		self.msg(chan, "%s, wow why don't you just go to PORNHUB instead you porn addict...SCREW YOU PORN ADDICTS!!!!!!!!!!!" % nick)

	def seppuku(self, chan, dum, nick):
		self.quit()
		self.connect()

	def quit(self):
		self.pingable = False

		
		
	## pics
	
	def linker(self, tags, scr, err="stop looking up ecchi you...you...h-h-hentai!!!!!!", n="", mode="scrape"):
		c = scr.scrape(tags) if mode == "scrape" else scr.random(())
		#return ("%s, page link: %s \x037 src link: %s \x033total: %i\x038 posted: %s  \x034id: %s \x032tags: %s " %(n, linkshort.isgd_short(scr.link(c['id'])), c["file_url"], c["total_resluts"], c["created_at"], c["id"], c["tags"])) if c else err
		if not c: return err
		self.currtags = (c["id"], c["tags"])
		return ("%s, page link: %s \x037 src link: %s \x033total: %i\x038 posted: %s  \x034id: %s \x032 rating: %s" %(n, scr.link(c['id']), c["file_url"], c["total_resluts"], c["created_at"], c["id"], {"s":"safe", "q": "questionable", "e":"explicit"}[c["rating"]]))

	def tags(self, chan, id, nick):
		if id:
			idd = id[0]
			c = self.scrapers["gelbooru"].get_tags(idd) # generalize this later
			self.msg(chan, "tags for %s: %s" % (idd, c))
		else:
			self.msg(chan, "tags for %s: %s" % (self.currtags[0], self.currtags[1]))
		
	def randpix(self, chan, dum, nick):
		g =  self.linker((), n=nick, scr=choicedict(self.scrapers), mode="random")
		self.msg(chan, g)
	
	
	def pic(self, chan, tags, nick):
		m = self.linker(tags, err="%s, stop looking up ecchi you...you...h-h-hentai!!!!!!" % nick, n=nick, scr=choicedict(self.scrapers), mode="scrape" if tags else "random")
		if m: self.msg(chan, m)
		
		
	def sfw(self, chan, tags, nick):
		tags.append("-rating:explicit")
		m = self.linker(tags, err="just because it is safe for work does not mean it is safe for you!! we all know you just wanted to find some hentai, %s...." % nick, n=nick, scr=choicedict(self.scrapers), mode="scrape")
		if m: self.msg(chan, m)
		
	def lewd(self, chan, tags, nick):
		tags.append("-rating:safe")
		m = self.linker(tags, err="see, there are no disgraceful pictures for embarassments to society like you, %s!" % nick, n=nick, scr=choicedict(self.scrapers), mode="scrape" )
		if m: self.msg(chan, m)		
		
	def safe(self, chan, tags, nick):
		tags.append("rating:safe")
		m = self.linker(tags,  err="%s, little children should not be looking on a site for weeaboos! please go outside and play..." % nick, n=nick, scr=choicedict(self.scrapers), mode="scrape")
		if m: self.msg(chan, m)
		
	def pron(self, chan, tags, nick):
		tags.append("rating:explicit")
		self.msg(chan, "wow you must be a big hentai if you want to only look at the explicit pictures...it's no wonder why you'll never get a girlfriend, %s!" % nick)
		m = self.linker(tags, err="see, %s,  there's no disgraceful pictures for embarassments to society like you!" % nick, n=nick, scr=choicedict(self.scrapers), mode="scrape")
		if m: self.msg(chan, m)

	

	## gelbooru
	def gel_rand(self, chan, dum, nick):
		g =  self.linker((), n=nick, scr=self.scrapers["gelbooru"], mode="random")
		self.msg(chan, g)
	
	
	def gel(self, chan, tags, nick):
		m = self.linker(tags, err="%s, stop looking up ecchi you...you...h-h-hentai!!!!!!" % nick, n=nick, scr=self.scrapers["gelbooru"], mode="scrape" if tags else "random")
		if m: self.msg(chan, m)
		
		
	def gsfw(self, chan, tags, nick):
		tags.append("-rating:explicit")
		m = self.linker(tags, err="just because it is safe for work does not mean it is safe for you!! we all know you just wanted to find some hentai, %s...." % nick, n=nick, scr=self.scrapers["gelbooru"], mode="scrape")
		if m: self.msg(chan, m)
		
	def glewd(self, chan, tags, nick):
		tags.append("-rating:safe")
		m = self.linker(tags, err="see, there are no disgraceful pictures for embarassments to society like you, %s!" % nick, n=nick, scr=self.scrapers["gelbooru"], mode="scrape" )
		if m: self.msg(chan, m)		
		
	def gsafe(self, chan, tags, nick):
		tags.append("rating:safe")
		m = self.linker(tags,  err="%s, little children should not be looking on a site for weeaboos! please go outside and play..." % nick, n=nick, scr=self.scrapers["gelbooru"], mode="scrape")
		if m: self.msg(chan, m)
		
	def gpron(self, chan, tags, nick):
		tags.append("rating:explicit")
		self.msg(chan, "wow you must be a big hentai if you want to only look at the explicit pictures...it's no wonder why you'll never get a girlfriend, %s!" % nick)
		m = self.linker(tags, err="see, %s,  there's no disgraceful pictures for embarassments to society like you!" % nick, n=nick, scr=self.scrapers["gelbooru"], mode="scrape")
		if m: self.msg(chan, m)
		
	def wallpaper(self, chan, tags, nick):
		tags.append("highres")
		tags.append("|")
		tags.append("absurdres")
		m = self.linker(tags, n=nick, scr=self.scrapers["gelbooru"], mode="scrape")
		if m: self.msg(chan, m)
	
	
	def aqua(self, chan, dum, nick):
		self.msg(chan, "this is me ^o^ i am the water goddess. bow down to me!! worship aqua-sama, the lord. i link messed up anime pics and you can play a guessing game with pics with me!!")
		self.gel(chan, ["aqua_(konosuba)"], nick)
	
	def ayumi(self, chan, dum, nick):
		self.msg(chan, "this is ayumi-chan! she is a cool game host who hosts the most popular game on savespam, wordgame! have some high paced fun action with your friends and get better at english vocabulary!")
		self.gel(chan, ["otosaka_ayumi"], nick)
		
	def neko(self, chan, dum, nick):
		self.gel(chan, ["cat_ears"], nick)
		
	def megumi(self, chan, dum, nick):
		self.msg(chan, "this is megu-chan. she is pretty cute but also a big slut!!! she likes playing wordgame extremely fast and making funny faces! she says she's the fastest and best wordgame player in the world but maybe you can beat her? some people have!")
		self.gel(chan, ["katou_megumi"], nick)
	
	def kiyomi(self, chan, dum, nick):
		self.msg(chan, "this is kiyomi-san : O she has cool megane and she is very smart! ask her about the weather or your bus schedule or almost anything factual!! ika musume is her best friend : )")
		self.sfw(chan, ["sakura_kiyomi"], nick)

	def fozrucix(self, chan, dum, nick):
		self.msg(chan, "this is fozrucix-kun!! he is actually a computer! he can process cool fucking jengascript commands! also he has a q timer and posts website link metadata! also he is a FUCKING ASSHOLE!!!!!!!! so he can tell u if anything is bullshit")
		self.gel(chan, ["computer", "|", "burgerpants"], nick)
		
	def saveybot(self, chan, dum, nick):
		self.msg(chan, "this is saveybot! he is the original bot... he can save cool things u type with the .save command! people like to chain him up for some reason..... 8=======D")
		self.gel(chan, ["chains"], nick)

		
		
	# game functions	
	def gelgame(self, chan, tags, mode="sqe"):
		if self.game_on:
			self.msg(chan, "hey there is already a gay going on!! let that one finish first!!")
			return
		rates = {"s":"rating:safe", "q":"rating:questionable", "e":"rating:explicit"}
		# start a new game!!
		self.gamestats["current_tags"] = tags
		print tags
		
		self.msg(chan, "starting the game!!! please wait about 30 seconds.... looking for a pic in %s" % self.gamestats["current_tags"])
		if mode: tags.append(rates[random.choice(mode)])
		winner = self.scrapers["gelbooru"].scrape(tags)
		
		if not winner:
			self.msg(chan, "try again with a different tags : ( nothing found for this set of tags!!")
			self.pingable = True
			return
		# read highscoreboard
		with open("scoreboard.sc", "r") as sc:
			scores = [line.split() for line in sc]
			
		self.gamestats["scoreboard"]  = {s[0] :  {"wins": int(s[1]), "games": int(s[2]), "+": int(s[3]), "-": int(s[4]) } for s in scores}
		
		self.gamestats["players"] = []
		self.gamestats["id"] = winner["id"]
		self.gamestats["guesses"] = 1
		self.gamestats["tag_guesses"] = 0
		self.gamestats["+"] = 0
		self.gamestats["-"] = 0
		self.gamestats["tags"] = winner["tags"].split()
		self.gamestats["tags"].append(rates[winner["rating"]])
		
		self.gamestats["current_guess"] = "-1"
		
		self.gamestats["gel_link"] = "http://www.gelbooru.com/index.php?page=post&s=view&id=%s" % self.gamestats["id"]
		self.msg(chan, "\x034helo gays!! it is time to play gelgame! this version of gelgame is: %s. guess a $tag to get some hints at what the pic is or guess the $pic id number or link to try to guess the picture!!" % mode)
		self.game_on = True
		print self.gamestats
		
		
	def gelgame_guess(self, chan, guess, nick):
		if not self.game_on:
			if not self.pingable: self.msg(chan, "hey there is no gay going on!! start one with $gelgame, $gelgame_safe, $gelgame_lewd, $gelgame_sfw, or $gelgame_pron!!")
			return
			
		print "$$pic attempt!!!"
		if not guess: return
		self.gamestats["current_guess"] = guess[0][guess[0].rfind("=")+1:]
		
		if self.gamestats["id"] == self.gamestats["current_guess"]:
			self.msg(chan, "\x033congratulations %s!!! you are the hentai expert!! that game took\x03 %i pic guesses\x033 and\x032 %i tag guesses \x033( \x039+%i \x034-%i \x033)... \x033here is the picture link!" % (nick, self.gamestats["guesses"], self.gamestats["tag_guesses"], self.gamestats["+"], self.gamestats["-"]))
			self.msg(chan, self.scrapers["gelbooru"].link(self.gamestats["id"]))
			
			if nick not in self.gamestats["scoreboard"]:
				self.gamestats["scoreboard"][nick] = {"wins" : 1, "games" : 1, "+" : 0, "-" : 0}
			
			else:
				self.gamestats["scoreboard"][nick]["wins"]+=1
			
			scores = sorted( ((v["wins"], k, v) for k, v in self.gamestats["scoreboard"].iteritems()), reverse=True) # babby's first generator expression and also lambda (oh no)
			print scores
			with open("scoreboard.sc", "w") as sc:
				for s in scores:
					sc.write("%s %i %i %i %i\n" % (s[1], s[0], s[2]["games"], s[2]["+"], s[2]["-"]))
			
			self.game_on = False
			
		else:
			self.msg(chan, "\x034no, %s, you are a wrong dong!!! please try again..." % nick)
			self.gamestats["guesses"]+=1
			if nick not in tuple(self.gamestats["scoreboard"]):
				self.gamestats["scoreboard"][nick] = {"wins" : 0, "games" : 0, "+" : 0, "-" : 0}	
			if nick not in self.gamestats["players"]:
				self.gamestats["players"].append(nick)
				self.gamestats["scoreboard"][nick]["games"]+=1
						
				
		print self.gamestats
		
	def gelgame_tag(self, chan, tags, nick):
		if not self.game_on:
			if not self.pingable: self.msg(chan, "hey there is no gay going on!! start one with $gelgame, $gelgame_safe, $gelgame_lewd, $gelgame_sfw, or $gelgame_pron!!")
			return
		plus, minus = 0, 0
		print "$$tag attempt!!"
		for t in tags:

			if t == "pantsu": t = "panties"
			print t
			self.gamestats["tag_guesses"]+=1
			if t in self.gamestats["tags"] and t not in self.gamestats["current_tags"]:
				self.msg(chan, "nice!! %s is one of the tags!!" % t)
				self.gamestats["+"]+=1
				self.gamestats["current_tags"].append(t.replace("+","%2b"))
				plus += 1
				
			else:
				if t not in self.gamestats["current_tags"]:
					self.gamestats["-"]+=1
					self.msg(chan, "\x034 %s is not one of the tags" % (t))
					self.gamestats["current_tags"].append("-"+t.replace("+","%2b"))
					minus += 1
					
				else: self.msg(chan, "\x034 %s was already guessed" % t)
		
			if nick not in tuple(self.gamestats["scoreboard"]):
				self.gamestats["scoreboard"][nick] = {"wins" : 0, "games" : 0, "+" : plus, "-" : minus}			
		
			if nick not in self.gamestats["players"]:
				self.gamestats["players"].append(nick)
				self.gamestats["scoreboard"][nick]["games"]+=1
						
			
			if plus: self.gamestats["scoreboard"][nick]["+"]+=plus  
			if minus: self.gamestats["scoreboard"][nick]["-"]+=minus
			
			#self.msg(chan, "\x032taglist: %s" % (" ".join(self.gamestats["current_tags"])))
			print self.gamestats["current_tags"]
			gel_url = "http://www.gelbooru.com/index.php?page=post&s=list&tags=%s" %("+".join(self.gamestats["current_tags"]))
			print gel_url
			self.msg(chan, "\x032taglink: %s" % (linkshort.isgd_short(gel_url)))
		
		print self.gamestats
		
	def game(self, chan, tags, nick):
		gt = Thread(target=self.gelgame, args=(chan, tags,""))
		gt.start()

	def game_safe(self, chan, tags, nick):
		gt = Thread(target=self.gelgame, args=(chan, tags, "s"))
		gt.start()

	def game_lewd(self, chan, tags, nick):
		gt = Thread(target=self.gelgame, args=(chan, tags,"qe"))
		gt.start()
		
	def game_sfw(self, chan, tags, nick):
		gt = Thread(target=self.gelgame, args=(chan, tags, "sq"))
		gt.start()	
		
	def game_pron(self, chan, tags, nick):
		gt = Thread(target=self.gelgame, args=(chan, tags,"e"))
		gt.start()	
	
	def gelgame_scoreboard(self, chan, tags, nick):
		with open("scoreboard.sc", "r") as sc:
			i = 1
			self.msg(chan, "------------------------------")
			self.msg(chan, "| gelgame scoreboard")
			for line in sc:
				l = line.split()
				self.msg(chan, "| %i) %s: %s wins/%s games ( +%s -%s )" %(i, l[0], l[1], l[2], l[3], l[4]))
				i+=1
			self.msg(chan, "------------------------------")

	## pixiv

	
	def quit(self):
		self.irc.send("QUIT :aqua-sama is the best goddess! bow down to me!!!\r\n")
		self.pingable = False
	
