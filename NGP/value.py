import itertools, random

suits = ["diamonds", "spades", "hearts", "clubs"]
ranks = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]
hands = ["High Card", "Pair", "Two Pair", "Three of a Kind", "Straight", "Flush", "Full House", "Four of a Kind", "Straigh Flush"]
odds = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
values = [-1, -1, 2, 3, 4, 6, 9, 25, 90]
payout = 0.0
deck = []
h = []
rbins = []
sbins = []


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
		return 8
	elif four:
		return 7
	elif three and pair:
		return 6
	elif flush:
		return 5
	elif straight:
		return 4
	elif three:
		return 3
	elif tp:
		return 2
	elif pair:
		return 1
	else:
		return 0

def discard(hand, rank, strat):
	return hand

def deal():
	return deck.pop(0)

trys = input('Enter number of plays: ')
count = 0
plays = input('Enter number of hands per play: ')
for k in range(trys):
	h = []
	deck = list(itertools.product(range(0,13), range(0,4)))
	random.shuffle(deck)

	for i in range(5):
		h.append(deal())
	r = eval(h)

	#h = discard(h, r)
	hs = []
	rs = []

	#duplicate the held cards for played hand
	for i in range(plays):
		count += 1
		hs.append(h)
		for j in range(len(hs[i]), 5):
			hs[i].append(deal)
		#eval each hand
		rs.append(eval(hs[i]))
		payout = payout + values[rs[i]]
		odds[rs[i]] = odds[rs[i]] + 1.0

	#if k%10 == 0:
	#	print(rbins)
	#	print(sbins)

#print(odds)

for k in range(len(odds)):
	odds[k] = odds[k]/count

print(odds)
print(count)
print(payout)