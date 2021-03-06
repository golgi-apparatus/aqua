#!/usr/bin/env python
# encoding=utf8  
import sys

reload(sys)  
sys.setdefaultencoding('utf8')

### external libs
import socket
from threading import Thread
from time import sleep, time
import random
import requests

### aqua libs
import linkshort
import scraper
from log import Log
from aqua_utils import plog, main_log

## helper

def choicedict(dic):
	return random.choice(list(dic.values()))

def searchkey(diclist, k, v):
	for i in diclist:
		if diclist[k] == v:
			return i
	
	return None
	
def ping_url(url):
	try:
		t0 = time()
		requests.get(url)
		t1 = time()
		
	except:
		plog(main_log, "cockblocked!!!!!!!!!!! : ((")
		sleep(1)
		t0 = time()
		requests.get(url)
		t1 = time()
		
	return (t1-t0)*1000
	
## bot

class Bot:
	def __init__(self, _nick, _network, _port, _channels, _ident, _ctl):
		self.RECONNECT = 0
		self.QUIT = 1
		self.network = _network
		self.qcode = self.RECONNECT
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
		self.logs = {}
		
		# game stats
		self.game_on = False
		self.can_scoreboard = True
		self.gamestats = {  
			"id" : "0",
			"guesses" : 0,
			"tags" : [],
			"current_guess" : "-1"
		}
		
		self.ctl = _ctl
		
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
			"?gelping": self.gelping,
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
			"?regume" : self.regume,
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
			"?scoreboard" : self.gelgame_scoreboard,
			
			self.ctl : self.admin  # self.ctl is the string you use to access admin commands. for security, define this in a file called "aqua_controller" and save it to the same directory as this aqua.py. when using admin commands, be careful to do it in pm and not in a public channel! (todo (read: idkwhen): pm only/registered user check)
		
		}

	### main irc actions
	
	def msg(self, chan, send):
		plog(main_log, chan)
		mm = "PRIVMSG %s :%s\r\n" %(chan,send)
		plog(main_log, mm)
		self.irc.send(mm)
		if chan not in self.logs: self.logs[chan] = Log("logs/%s.log" %(chan))
		self.logs[chan].write(self.nick, send)
	
	def send_raw(self, send):
		plog(main_log, send)
		self.irc.send(send)
		
	def join(self, chan):
		if chan in self.channels: return
		self.channels.append(chan)
		for c in self.channels:
			self.irc.send("\r\nJOIN " +c+ "\r\n")
			plog(main_log, "\r\nJOIN " +c+ "\r\n")			
			
	def leave(self, chan):
		if chan not in self.channels: return
		self.irc.send("\r\nPART "+chan+" i am too holy for this channel!"+"\r\n")
		plog(main_log, "\r\nPART"+chan+" i am too holy for this channel!"+"\r\n")
		self.channels.remove(chan)

	def quit(self, code): # code decides whether to reconnect or not
		self.irc.send("QUIT :aqua-sama is the best goddess! bow down to me!!!\r\n")
		self.pingable = False
		self.qcode = code
		return code
		
		
	## aqua utilities
	
	def connect(self):
		self.irc = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
		self.irc.settimeout(300)
		plog(main_log, "setting up irc socket...  %s %i" %(self.network, self.port))
		self.irc.connect( (self.network, self.port) )
		plog(main_log, "connecting to irc...")
		plog(main_log, "sending nick info...NICK %s\r\n" %(self.nick))
		self.irc.send("NICK %s\r\n" %(self.nick))
		plog(main_log, "sending user info...USER %s %s %s :%s\r\n" %(self.ident, self.ident, self.ident, self.ident))
		self.irc.send("USER %s %s %s :%s\r\n" %(self.ident, self.ident, self.ident, self.ident))
		plog(main_log, "pinging!!!")
		self.data = self.irc.recv(4096)
		if self.data.find ('PING') != -1:
			self.irc.send ('PONG ' + self.data.split()[1] + '\r\n')
		for chan in self.channels:
			self.irc.send("\r\nJOIN " +chan+ "\r\n")
			plog(main_log, "\r\nJOIN " +chan+ "\r\n")
		#plog(main_log, 'PONG ' + self.data.split()[1] + '\r\n'
		self.pingable = True
		return True

	def parse_args(self, a, dat):
		if not self.pingable: return ()
		plog(main_log, "parsing some args!")
		datt = dat
		while (datt[0].replace(":","")) != a:
			plog(main_log, str(datt)+" "+a)
			datt.pop(0)
		datt.pop(0)
		return datt
	
	def ping(self):
		self.irc.setblocking(1)
		try:
			if not self.pingable: 
				return
			data = self.irc.recv(4096)
			self.irc.setblocking(0)
			if data.find ('PING') != -1:
				self.irc.send ('PONG ' + data.split()[1] + '\r\n')
				for chan in self.channels:
					self.irc.send("\r\nJOIN " +chan+ "\r\n")
					plog(main_log, "\r\nJOIN " +chan+ "\r\n")	
				
			return data
			
		except socket.error:
			plog(main_log, "::::::::: ((((((((((((((( socket fail")
			self.pingable = False
			sys.exit(2506)
		except socket.timeout:
			plog(main_log, "TTTTTTTTTTTTTTTTTT socket timeout")
			self.pingable = False
			sys.exit(2507)
	
	def process_data(self, data):
		argss = data.split()
		if argss[0] == "PING": # don't do all the rest if it's just a ping wow exception master
			return
		
		exc, att = argss[0].find("!"), argss[0].find("@")
		self.user["nick"] = argss[0][1:exc] 
		self.user["ident"] = argss[0][exc:att] 
		self.user["host"] = argss[0][att:-1] 

		no_colon = [s.replace(":","") for s in argss]
		plog(main_log, str(argss))
		
		
		nn = argss[0][1:argss[0].find("!")] 
		chan = argss[0][1:argss[0].find("!")] if argss[2] == self.nick else argss[2]
		
		for key in self.cmdy:
			if key in no_colon: 
				chan = argss[0][1:argss[0].find("!")] if argss[2] == self.nick else argss[2]
				pa = self.parse_args(key, argss)
				plog(main_log, str(pa))
				self.cmdy[key](chan, pa, nn)
				return
	
		for c in '/:*?"<>|\\': # lol gay
			if c in chan:
				chan = "__home__"
				break
				
		if chan not in self.logs: self.logs[chan] = Log("logs/%s.log" %(chan))
		if (len(argss) > 3): content = " ".join(argss[3:])[1:]
		if (len(argss) > 2): a2 = " ".join(argss[2:])[1:][1:]
		
		if argss[1] == "PRIVMSG": self.logs[chan].write(nn, content)
		elif argss[1] == "NICK": self.logs[chan].nick(nn, a2)
		elif argss[1] == "JOIN": self.logs[chan].join(nn)
		elif argss[1] == "QUIT": self.logs[chan].self.QUIT(nn, a2)
		elif argss[1] == "PART": self.logs[chan].leave(nn, a2)
		else: self.logs[chan].raw(data)
	
	## command functions
	
	def help(self, chan, dum, nick):
		self.msg(chan, "wow do you need some HELP, %s??? here u go!! https://github.com/golgi-apparatus/aqua/blob/master/readme.md" % nick)
	
	def bug(self, chan, dum, nick):
		self.msg(chan, "wanna report a bug or request a new feature, %s??? do it here! https://github.com/golgi-apparatus/aqua/issues" % nick)

	def water(self, chan, dum, nick):
		self.msg(chan, "%s, drink water you dong!!!" % nick)
		
	def photo(self, chan, dum, nick):
		self.msg(chan, "%s, wow why don't you just go to PORNHUB instead you porn addict...SCREW YOU PORN ADDICTS!!!!!!!!!!!" % nick)


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
			self.msg(chan, "tags for %s: %s" % (idd, c) if c else  "tags error! please put a valid id number in the argument!")
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
	
	def gelping(self, chan, dum, nick):
		api_link = "http://gelbooru.com/index.php?page=dapi&s=post&q=index"
		best = ping_url(api_link)
		plog(main_log, str(best))
		worst = ping_url(api_link+"&pid=%i" % (self.scrapers["gelbooru"].MAXGEL/100 - 1))
		plog(main_log, str(worst))
		self.msg(chan, "%s here is my current gelbooru ping!! best=%ims worst=%ims" % (nick, best, worst))
		
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
		
	def regume(self, chan, dum, nick):
		self.msg(chan, "this is regume-chan! she is very outgoing and conversational and fun to talk to! ping her with a topic of your choice and she'll respond to you!")
		self.gel(chan, ["id:2616196"], nick)

		
		
	## game functions	
	def gelgame(self, chan, tags, mode="sqe"):
		if self.game_on:
			self.msg(chan, "hey there is already a gay going on!! let that one finish first!!")
			return
		rates = {"s":"rating:safe", "q":"rating:questionable", "e":"rating:explicit"}
		# start a new game!!
		self.gamestats["current_tags"] = tags
		plog(main_log, str(tags))
		
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
		plog(main_log, str(self.gamestats))
		
		
	def gelgame_guess(self, chan, guess, nick):
		if not self.game_on:
			if not self.pingable: self.msg(chan, "hey there is no gay going on!! start one with $gelgame, $gelgame_safe, $gelgame_lewd, $gelgame_sfw, or $gelgame_pron!!")
			return
			
		plog(main_log, "$$pic attempt!!!")
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
			plog(main_log, str(scores))
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
		plog(main_log, str(self.gamestats))
		
	def gelgame_tag(self, chan, tags, nick):
		if not self.game_on:
			if not self.pingable: self.msg(chan, "hey there is no gay going on!! start one with $gelgame, $gelgame_safe, $gelgame_lewd, $gelgame_sfw, or $gelgame_pron!!")
			return
		plus, minus = 0, 0
		plog(main_log, "$$tag attempt!!")
		for t in tags:

			if t == "pantsu": t = "panties"
			plog(main_log, t)
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
			plog(main_log, str(self.gamestats)["current_tags"])
			gel_url = "http://www.gelbooru.com/index.php?page=post&s=list&tags=%s" %("+".join(self.gamestats["current_tags"]))
			plog(main_log, gel_url)
			self.msg(chan, "\x032taglink: %s" % (linkshort.isgd_short(gel_url)))
		
		plog(main_log, str(self.gamestats))
		
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
		if self.can_scoreboard:
			self.can_scoreboard = False
			with open("scoreboard.sc", "r") as sc:
				i = 1
				self.msg(chan, "------------------------------")
				self.msg(chan, "| gelgame scoreboard")
				for line in sc:
					l = line.split()
					self.msg(chan, "| %i) %s: %s wins/%s games ( +%s -%s )" %(i, l[0], l[1], l[2], l[3], l[4]))
					i+=1
				self.msg(chan, "------------------------------")
			self.can_scoreboard = True
	
	# maybe you will figure out how to compromise aqua??? lol good luck~
	def admin(self, chan, tags, nick):
		plog(main_log, "!!!admin!!!")
		if not tags: return
		plog(main_log, str(tags))
		if tags[0] == "msg" and tags[2]:
			self.msg(tags[1], " ".join(tags[2:]))
				
		elif tags[0] == "join" and tags[1]:
			plog(main_log, str(tags)[1:])
			for t in tags[1:]: self.join(t)
			
		elif tags[0] == "leave" and tags[1]:
			plog(main_log, str(tags)[1:])
			for t in tags[1:]: self.leave(t)
		
		elif tags[0] == "quit":
			self.quit(self.QUIT)
			sys.exit(2511)
			
		elif tags[0] == "rec":
			self.quit(self.RECONNECT)
			self.connect()
						
