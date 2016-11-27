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
		#if it's a 'good' play try it again
		if (playbook[1][k][pk]/playbook[0][k][pk]) >= -1:
			return list(pk)
	
	# if we make it this far just return a new one not in the list
	return getRandomPlay()

def playToKey(play):
	return ''.join(str(e) for e in play)

def handToKey(hand):
	handStr = '' 
	for i in range(len(hand)):
		handStr += Card.STR_RANKS[Card.get_rank_int(hand[i])]
	return handStr

def handSort(hand):
	return sorted(hand[:], key=lambda x: Card.get_rank_int(x))

values = [80, 50, 8, 6, 3, 1, -.5, -1,-2]

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
	rank1 = ev.get_rank_class(score1) - 1

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
	rank2 = ev.get_rank_class(score2) - 1

	# # if we improved value of this play goes up
	# if score2 < score1:
	# 	if key2 in handMem[1][key1]:
	# 		handMem[1][key1][key2] += 1.0
	# 	else:
	# 		handMem[1][key1][key2] = 1.0
	# # if we did worse value of this play goes down
	# elif score1 < score2:
	# 	if key2 in handMem[1][key1]:
	# 		handMem[1][key1][key2] -= 1.0
	# 	else:
	# 		handMem[1][key1][key2] = -1.0
	# else:
	# 	if key2 in handMem[1][key1]:
	# 		handMem[1][key1][key2] += 0.1
	# 	else:
	# 		handMem[1][key1][key2] = 0.1

	# if we improved value of this play goes up
	# if we did worse value of this play goes down
	if key2 not in handMem[1][key1]:
		handMem[1][key1][key2] = 0.0

	handMem[1][key1][key2] += values[rank2] - values[rank1]

f.close()

gr = -1
key = ''
for k in list(handMem[0].keys()):
	if len(handMem[0][k]) > gr :
		gr = len(handMem[0][k])
		key = k

print key

for k in list(handMem[0][key].keys()):
	print ' key: {n} >> {q}'.format(n=k, q=handMem[1][key][k]/handMem[0][key][k])

while True:
	
	c = ''
	
	c = raw_input('Enter card (or "" to quit): ')
	if c == "":
		break

	if c in handMem[0]:
		for k in list(handMem[0][c].keys()):
			print ' key: {n} >> {q}'.format(n=k, q=handMem[1][c][k]/handMem[0][c][k])
	else:
		print 'No Record, Try again.'