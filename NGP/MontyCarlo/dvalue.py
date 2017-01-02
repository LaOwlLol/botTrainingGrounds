import itertools, random
from tqdm import tqdm
from deuces import Deck, Card, Evaluator

odds = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
values = [90, 25, 9, 6, 4, 3, 2, -1,-1]
stg = [[8], [7], [8], [8], [8], [4], [3], [2], [6, 5, 1]]

def discard(hand, rank):
	for i in range(len(stg[rank])):
		#discard all
		if stg[rank][i] == 0:
			return []
		elif stg[rank][i] == 1:
			return holdHigh(hand)
		elif stg[rank][i] == 2:
			return holdPair(hand)
		elif stg[rank][i] == 3:
			return holdTwoPair(hand)
		elif stg[rank][i] == 4:
			return holdThreeSet(hand)
		elif stg[rank][i] == 5:
			if hasStraightDraw(hand):
				return holdStraightDraw(hand)
		elif stg[rank][i] == 6:
			if hasFlushDraw(hand):
				return holdFlushDraw(hand)
		elif stg[rank][i] == 7:
			return holdFourSet(hand)
		else:
			return hand

def holdHigh(hand):

	bins = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	for i in range(len(hand)):
		bins[Card.get_rank_int(hand[i])] += 1

	save = -1
	
	for i in range(len(bins)-1, -1, -1):
		if bins[i] > 0:
			save = i

	for i in range(len(hand)-1, -1, -1):
		if Card.get_rank_int(hand[i]) != save:
			hand.pop(i)

	return hand

def holdPair(hand):
	bins = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	for i in range(len(hand)):
		bins[Card.get_rank_int(hand[i])] += 1

	save = -1
	for i in range(len(bins)):
		if bins[i] == 2:
			save = i

	for i in range(len(hand)-1, -1, -1):
		if Card.get_rank_int(hand[i]) != save:
			hand.pop(i)

	return hand

def holdTwoPair(hand):
	bins = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	for i in range(len(hand)):
		bins[Card.get_rank_int(hand[i])] += 1

	save = []
	for i in range(len(bins)):
		if bins[i] == 2:
			save.append(i)

	for i in range(len(hand)-1, -1, -1):
		if save.count(Card.get_rank_int(hand[i])) < 1:
			hand.pop(i)

	return hand

def holdThreeSet(hand):
	bins = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	for i in range(len(hand)):
		bins[Card.get_rank_int(hand[i])] += 1

	save = -1
	for i in range(len(bins)):
		if bins[i] == 3:
			save = i

	for i in range(len(hand)-1, -1, -1):
		if Card.get_rank_int(hand[i]) != save:
			hand.pop(i)

	return hand

def holdStraightDraw(hand):
	bins = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	for i in range(len(hand)):
		bins[Card.get_rank_int(hand[i])] += 1

	keep = []
	last = -1
	scount = 0
	for i in range(13):
		if bins[i] > 0:
			scount += 1
			keep.append(i)
			last = i
			if scount > 2:
				break
		else:
			del keep[:]
			scount = 0

	if scount < 3:
		del keep[:]

	if len(keep) == 3 and last < 12:
		if bins[last+1] > 0:
			keep.append(last+1)
	elif bins[12] > 0 and bins[0] > 0 and bins[1] > 0:
		keep.append(0)
		keep.append(1)
		keep.append(12)

	if len(keep) > 2:
		#remove cards not in straight
		for i in range(len(hand)-1, -1, -1):
			if keep.count(Card.get_rank_int(hand[i])) == 0:
				hand.pop(i)

		#remove duplicates
		have = []
		for k in range(len(hand)-1, -1, -1):
			if have.count(Card.get_rank_int(hand[k])) < 1:
				have.append(Card.get_rank_int(hand[k]))
			else:
				hand.pop(k)

	# print 'holding straight draw: '
	# print keep
	# Card.print_pretty_cards(hand)

	return hand

def holdFlushDraw(hand):
	bins = [0, 0, 0, 0, 0, 0, 0, 0, 0]

	for i in range(len(hand)):
		bins[Card.get_suit_int(hand[i])-1] += 1

	for i in range(len(bins)):
		if bins[i] > 2:
			for k in range(len(hand)-1, -1, -1):
				if Card.get_suit_int(hand[k])-1 != i:
					hand.pop(k)
			break

	#print 'holding flush draw: {h}'.format(h=hand)

	return hand

def holdFourSet(hand):

	bins = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	for i in range(len(hand)):
		bins[Card.get_rank_int(hand[i])] += 1

	save = -1
	for i in range(len(bins)):
		if bins[i] == 4:
			save = i

	for i in range(len(hand)-1, -1, -1):
		if Card.get_rank_int(hand[i]) != save:
			hand.pop(i)

	return hand

def hasStraightDraw(hand):
	bins = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	for i in range(len(hand)):
		bins[Card.get_rank_int(hand[i])] += 1

	scount = 0
	for i in range(13):
		if bins[i] > 0:
			scount += 1
			if scount > 2:
				return True
		else:
			scount = 0

	if bins[0] > 0 and bins[1] > 0 and bins[12] > 0:
		return True

	return False

def hasFlushDraw(hand):
	bins = [0, 0, 0, 0, 0, 0, 0, 0, 0]

	for i in range(len(hand)):
		bins[Card.get_suit_int(hand[i])-1] += 1

	if bins[0] > 2 or bins[1] > 2 or bins[2] > 2 or bins[3] > 2:
		return True
	else:
		return False

trys = input('Enter number of plays: ')
#trys = 100000
plays = input('Enter number of hands per play: ')
count = 0
payout = 0.0
deck = Deck()
ev = Evaluator()
for k in tqdm(range(trys)):

	deck.shuffle()
	h = deck.draw(5)
	
	r = ev.get_rank_class(ev.evaluate(h, []))-1 

	h = discard(h, r)	

	hs = []
	rs = []

	#duplicate the held cards for played hands
	for i in range(plays):
		count += 1
		hs.append(h)
		for j in range(len(hs[i]), 5):
			hs[i].append(deck.draw(1))
		#eval each hand
		rs.append(ev.get_rank_class(ev.evaluate(hs[i], []))-1)
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
print(payout/count)
print(stg)