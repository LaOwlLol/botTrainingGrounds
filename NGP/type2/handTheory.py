import itertools, random
from tqdm import tqdm
from deuces import Deck, Card, Evaluator

def getRandomPlay():
	p = []
	for i in range(5):
		p.append(int(random.getrandbits(1)))
	return p

def determinePlay(k, playbook):
	
	for pk in list(playbook[0][k].keys()):
		#if it's a good play try it again
		if (playbook[1][k][pk]/playbook[0][k][pk]) >= 0:
			return list(pk)
		#otherwise try something else
		else:
			#do we know other plays?
			#grab one not this one though and not a neg one
			for n in list(playbook[0][k].keys()):
				if (playbook[1][k][n]/playbook[0][k][n]) >= 0 and n != pk:
					return list(n)

	# if we make it this far just return a new one not in the list
	r = getRandomPlay()
	while playToKey(r) in playbook[0][k]:
		r = getRandomPlay()
	return r

def playToKey(play):
	return ''.join(str(e) for e in play)

def handToKey(hand):
	handStr = '' 
	for i in range(len(hand)):
		handStr += str(Card.get_rank_int(hand[i]))
	return handStr

def handSort(hand):
	return sorted(hand[:], key=lambda x: Card.get_rank_int(x))

values = [49, 49, 8, 6, 3, 1, 0, -1,-1]

f = open('handLog', 'w')

ev = Evaluator()
deck = Deck()

handMem = [{}, {}]
count = input('Enter number of hands to play: ')
for k in tqdm(range(count)):
	
	deck.shuffle()
	#get a hand and turn it into a key
	h = handSort(deck.draw(5))
	key1 = handToKey(h)

	if key1 not in handMem[0]:
		f.write(key1+'\n')
		handMem[0][key1] = {}
		handMem[1][key1] = {}
		p = getRandomPlay()
	else:
		p = determinePlay(key1, handMem)

	#save the initiial rank
	score1 = ev.evaluate(h, [])

	# randomly generate a "play"
	key2 = playToKey(p)
	
	#count the current play
	if key2 in handMem[0][key1]:
		handMem[0][key1][key2] += 1
	else:
		handMem[0][key1][key2] = 1

	#use the play to discard
	for i in range(4, -1, -1):
		if p[i]:
			h.pop(i)

	#draw back to five
	for i in range(len(h), 5):
		h.append(deck.draw(1))

	#remember the score
	score2 = ev.evaluate(h, [])

	# if we improved value of this play goes up
	if score2 < score1:
		if key2 in handMem[1][key1]:
			handMem[1][key1][key2] += 1.0
		else:
			handMem[1][key1][key2] = 1.0
	# if we did worse value of this play goes down
	elif score1 < score2:
		if key2 in handMem[1][key1]:
			handMem[1][key1][key2] -= 1.0
		else:
			handMem[1][key1][key2] = -1.0
	else:
		if key2 not in handMem[1][key1]:
			handMem[1][key1][key2] = 0.0

f.close()

while True:
	
	c = ''
	
	c = raw_input('Enter card (or "" to quit): ')
	if c == "":
		break

	if c in handMem[0]:
		print handMem[0][c]
		print handMem[1][c]
	else:
		print 'No Record, Try again.'