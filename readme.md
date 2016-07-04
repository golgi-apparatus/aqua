aqua.py
-----------------------
accidental ecchi irc bot in python

about
-----------------------
hello i am aqua!! http://konosuba.wikia.com/wiki/Aqua

i am the water goddess of the axis cult!

i am a multithreaded fun interface that lets you link random pictures from certain websites in irc channels! currently i only support gelbooru but i will be able to link pixiv images as well!!

i am an accidental ecchi bot because i didn't know that gelbooru was filled with weirdo pics : ( oh well!!!

sometimes i take a bit long because i forget older pics so i have to dig for them : ((( but i always take under a minute!!

commands
-----------------------
here is what i can do!!

	pic general (currently supported: gelbooru)
	------------------------------------------------------------------
	?rand				link a random picture	
	?pic <tags> 		link a random picture in <tags>
	?safe <tags>		link a (safe!) random picture in <tags>
	?sfw <tags>			link a (safe or questionable!) random picture in <tags>
	?lewd <tags>		link a (questionable or explicit!) random picture in <tags>
	?pron <tags>		link a (explicit!) random picture in <tags> (wow why would you even use this wtf?????)
			
			
	gelbooru general
	------------------------------------------------------------------
	?gay 				link a random picture on gelbooru
	?gel <tags> 		link a random picture in <tags> from gelbooru
	?gsafe <tags>		link a (safe!) random picture in <tags> from gelbooru
	?gsfw <tags>			link a (safe or questionable!) random picture in <tags> from gelbooru
	?glewd <tags>		link a (questionable or explicit!) random picture in <tags> from gelbooru
	?gpron <tags>		link a (explicit!) random picture in <tags> from gelbooru (wow why would you even use this wtf?????)
	?wallpaper <tags>	link a wallpaper spec (highres | absurdres) picture in <tags> from gelbooru
	
	~~ you can also prepend your tags with - if you DON'T want to see that tag (for example if you only want anime pix and no photos, put -photo as one of the tags)
	~~ gelbooru has some neat features for tags!! check them out here http://gelbooru.com/index.php?page=help&topic=cheatsheet (~pre does not work)
	~~ if you want to use the OR operator (~tag1 ~tag2) use tag1 | tag2 instead
	~~ if you think a picture's rating is wrong, sign into gelbooru and change it!!
	
	
	character cards
	------------------------------------------------------------------
	here are pictures of some of my friends!!! do you want to be my friend??? talk to my lowly servant golgi and send me some pics of you and i will let you be my friend!!! : ))
	
	?me					show a random picture of me! (aqua)
	?megumi				show a random picture of katou megumi
	?kiyomi				show a (sfw) random picture of sakura kiyomi
	?fozrucix			show a random picture of a computer
	?ayumi				show a random picture of otosaka ayumi
	?saveybot			show a random picture of chains
	?neko				show a random neko
	
	
	gelbooru guessing game (gelgame)
	------------------------------------------------------------------
	gelgame is a fun game where you have to find the picture i am thinking of! use $tag <tags> to narrow down your search and click on the is.gd links to go to the page with the current corresponding tags. then when you think you found my picture, use $pic <id> to guess my picture!
	
	$gelgame <tags>				start a new gelgame in <tags>
	$gelgame_safe <tags>		start a new (safe) gelgame in <tags>
	$gelgame_sfw <tags>			start a new (safe or questionable) gelgame in <tags>
	$gelgame_lewd <tags>		start a new (questionable or explicit) gelgame in <tags>
	$gelgame_pron <tags>		start a new (explicit) gelgame in <tags>
	$tag <tags>					add new <tags> to the taglist and post the corresponding gelbooru search link with the tags
	$pic <id>					attempt to guess the picture using <id> (use the id number in the link!)
	
	~~ with more broad searches, you may need to wait up to 30 seconds for me to find a pic! sometimes it's hard for me to remember the older pictures so i have to try to think of them! of course, if you narrow your initial tags a bit more i might be a little faster!
	
	
future things
------------------
- pixiv support (update: if you would really like this, pm golgi on how the interface should be (all the tags are in japanese!!))
- high score board for gelgame
- faster notag searching
- more pic sites!!!
	- add "user:danbooru" to your tags in a gelbooru search for danbooru	
	- use ?gsafe for safebooru