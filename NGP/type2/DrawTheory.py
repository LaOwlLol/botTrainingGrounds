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
		if (playbook[1][k][pk]/playbook[0][k][pk]) >= -0.1:
			return list(pk)
	
	# if we make it this far just return a new one not in the list
	return getRandomPlay()

def playToKey(play):
	return ''.join(str(e) for e in play)

def handToKey(hand):
	handStr = '' 
	for i in range(len(hand)):
		handStr += Card.STR_RANKS[Card.get_rank_int(hand[i])]
		handStr += Card.INT_SUIT_TO_CHAR_SUIT[Card.get_suit_int(hand[i])]
	return handStr

def handSort(hand):
	return sorted(hand[:], key=lambda x: (Card.get_rank_int(x), Card.get_suit_int(x) ))

values = [256, 128, 64, 32, 16, 8, 4, 2, 1]

f = open('handLog', 'w')

ev = Evaluator()
deck = Deck()

handMem = [{}, {}]
score = {}
count = input('Enter number of \'games\' to play: ')
hands = input('Enter number of hands per game: ')
for k in tqdm(range(count)):
	for m in range(hands):
		deck.shuffle()

		#get a hand and turn it into a key
		h = handSort(deck.draw(5))
		key1 = handToKey(h)

		if key1 not in handMem[0]:
			f.write(key1+'\n')
			handMem[0][key1] = {}
			handMem[1][key1] = {}
			#save the initiial rank
			score1 = ev.evaluate(h, [])
			rank1 = ev.get_rank_class(score1) - 1
			score[key1] = rank1
			p = getRandomPlay()
		else:
			rank1 = score[key1]
			p = determinePlay(key1, handMem)
			

		# randomly generate a "play"
		key2 = playToKey(p)
		
		#count the current play
		if key2 in handMem[0][key1]:
			handMem[0][key1][key2] += 1
		else:
			handMem[0][key1][key2] = 1
			handMem[1][key1][key2] = 0.0

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

		# if we improved value of this play goes up
		# if we did worse value of this play goes down
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
	print ' key: {n} >> {q} = {p}/{r}'.format(n=k, q=handMem[1][key][k]/handMem[0][key][k], p=handMem[1][key][k], r=handMem[0][key][k])

while True:
	
	key = raw_input('Enter card (or "" to quit): ')
	if key == "q":
		break
	if key == "dump":
		f = open('statLog', 'w')
		for hk in list(handMem[1].keys()):
			f.write(hk+'\n')
			for pk in list(handMem[1][hk].keys()):
				f.write(pk+' >> '+ str(handMem[1][hk][pk]/handMem[0][hk][pk]) + ' == '+ str(handMem[1][hk][pk]) + '/' + str(handMem[0][hk][pk]) +'\n')
		f.close()
		break


	if key in handMem[0]:
		for k in list(handMem[0][key].keys()):
			print ' key: {n} >> {q} = {p}/{r}'.format(n=k, q=handMem[1][key][k]/handMem[0][key][k], p=handMem[1][key][k], r=handMem[0][key][k])
	else:
		print 'No Record, Try again.'