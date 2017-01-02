import itertools, random

suits = ["diamonds", "spades", "hearts", "clubs"]
ranks = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]
hands = ["Straigh Flush", "Four of a Kind", "Full House", "Flush", "Straight", "Three of a Kind", "Two Pair", "Pair", "High Card"]
deck = []
h = []

def eval(hand):
	rbins = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	sbins = [0, 0, 0, 0]
	flush = False
	straight = False
	four = False
	three = False
	tp = False
	pair = False

	for k in range(len(hand)):
		rbins[hand[k][0]] = rbins[hand[k][0]] + 1
		sbins[hand[k][1]] = sbins[hand[k][1]] + 1

	if sbins[0] >= 5 or sbins[1] >= 5 or sbins[2] >= 5 or sbins[3] >= 5:
		flush = True

	scount = 0
	for i in range(14):
		if rbins[i] > 0:
			scount = scount + 1
			if scount == 5 or (i == 13 and scount == 4 and rbins[0] > 0):
				straight = True
			#print 'At {k} scount is {s}'.format(k=i, s=scount)
		else:
			scount = 0

	for i in range(13):
		if rbins[i] == 2 and pair:
			tp = True
		elif rbins[i] == 2:
			pair = True
		elif rbins[i] == 3:
			three = True
		elif rbins[i] == 4:
			four = True

	if straight and flush:
		return 0
	elif four:
		return 1
	elif three and pair:
		return 2
	elif flush:
		return 3
	elif straight:
		return 4
	elif three:
		return 5
	elif tp:
		return 6
	elif pair:
		return 7
	else:
		return 8



def deal():
	return deck.pop(0)


deck = list(itertools.product(range(0,13), range(0,4)))
random.shuffle(deck)
for i in range(5):
	h.append(deal())
for i in range(len(h)):
	print'{r} of {s}'.format(r=ranks[h[i][0]], s=suits[h[i][1]])
print(hands[eval(h)])