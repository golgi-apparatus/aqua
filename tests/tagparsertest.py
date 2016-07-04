from random import choice
def tag_parser(tags):
	tlen = len(tags)
	newtags = []
	t = 0
	while t < tlen:
		tt = tags[t]
		if t > 0 and t < tlen-1 and tt == "|":
			cc = choice((-1,1))
			tt = tags[t+cc]
			if cc == -1: t+=1
			if choice((0, 1)) == 0: newtags[-1] = tt
		else: newtags.append(tt)
		t+=1

	return {}.fromkeys(newtags).keys()
	
print tag_parser(["yuri", "|", "yaoi"])