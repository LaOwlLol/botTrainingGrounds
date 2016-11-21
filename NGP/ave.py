import itertools, random
from tqdm import tqdm

suits = ["diamonds", "spades", "hearts", "clubs"]
ranks = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]
hands = ["High Card", "Pair", "Two Pair", "Three of a Kind", "Straight", "Flush", "Full House", "Four of a Kind", "Straigh Flush"]
values = [-1, -1, 2, 3, 4, 6, 9, 25, 90]
stg = [ [6, 5, 1],
[2],
[3],
[4],
[8],
[8],
[8],
[7],
[8]]

deck = []
h = []
rbins = []
sbins = []


def eval(hand):
	rbins = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
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

	if sbins[0] > 4 or sbins[1] > 4 or sbins[2] > 4 or sbins[3] > 4:
		flush = True

	scount = 0
	for i in range(13):
		if rbins[i] > 0:
			scount = scount + 1
			if scount == 5 or (i == 12 and scount > 3 and rbins[0] > 0):
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
		bins[hand[i][0]] += 1

	save = -1
	if bins[0] > 0:
		save = 0
	else:
		for i in range(len(bins)-1, -1, -1):
			if bins[i] > 0:
				save = i

	for i in range(len(hand)-1, -1, -1):
		if hand[i][0] != save:
			hand.pop(i)

	return hand

def holdPair(hand):
	bins = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	for i in range(len(hand)):
		bins[hand[i][0]] += 1

	save = -1
	for i in range(len(bins)):
		if bins[i] == 2:
			save = i

	for i in range(len(hand)-1, -1, -1):
		if hand[i][0] != save:
			hand.pop(i)

	return hand

def holdTwoPair(hand):
	bins = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	for i in range(len(hand)):
		bins[hand[i][0]] += 1

	save = []
	for i in range(len(bins)):
		if bins[i] == 2:
			save.append(i)

	for i in range(len(hand)-1, -1, -1):
		if save.count(hand[i][0]) < 1:
			hand.pop(i)

	return hand

def holdThreeSet(hand):
	bins = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	for i in range(len(hand)):
		bins[hand[i][0]] += 1

	save = -1
	for i in range(len(bins)):
		if bins[i] == 3:
			save = i

	for i in range(len(hand)-1, -1, -1):
		if hand[i][0] != save:
			hand.pop(i)

	return hand

def holdStraightDraw(hand):
	bins = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	for i in range(len(hand)):
		bins[hand[i][0]] += 1

	keep = []
	last = 0

	if bins[0] > 0:
		keep.append(0)

	for i in range(1,12):
		if bins[i] > 0 and i == (last+1):
			last = i
			keep.append(i)
		elif bins[i] > 0 and i > (last+1):
			last = i
			del keep[:]
			keep.append(i)

		if len(keep) == 3 and bins[i+1] > 0:
			keep.append(i+1)
			last = i+1
			break
		elif len(keep) == 3 and bins[i+1] < 1:
			break

	if (last == 11 and len(keep) == 2 and bins[12] > 0):
		last = 12
		keep.append(12)


	if len(keep) < 3:
		del keep[:]

	if bins[11] > 0 and bins[12] > 0 and bins[0] > 0:
		del keep[:]
		if bins[10] > 0:
			keep.append(10)
		keep.append(11)
		keep.append(12)
		keep.append(0)

	if len(keep) > 2:
		#remove cards not in straight
		for i in range(len(hand)-1, -1, -1):
			if keep.count(hand[i][0]) == 0:
				hand.pop(i)

		#remove duplicates
		have = []
		for k in range(len(hand)-1, -1, -1):
			if have.count(hand[k][0]) < 1:
				have.append(hand[k][0])
			else:
				hand.pop(k)

	#print 'holding straight draw: {k}'.format(k=keep)
	#print '\t hand: {h}'.format(h=hand)

	return hand

def holdFlushDraw(hand):
	bins = [0, 0, 0, 0]

	for i in range(len(hand)):
		bins[hand[i][1]] += 1

	for i in range(len(bins)):
		if bins[i] > 2:
			for k in range(len(hand)-1, -1, -1):
				if hand[k][1] != i:
					hand.pop(k)
			break

	#print 'holding flush draw: {h}'.format(h=hand)

	return hand

def holdFourSet(hand):

	bins = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	for i in range(len(hand)):
		bins[hand[i][0]] += 1

	save = -1
	for i in range(len(bins)):
		if bins[i] == 4:
			save = i

	for i in range(len(hand)-1, -1, -1):
		if hand[i][0] != save:
			hand.pop(i)

	return hand

def hasStraightDraw(hand):
	bins = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	for i in range(len(hand)):
		bins[hand[i][0]] += 1

	scount = 0
	for i in range(13):
		if bins[i] > 0:
			scount = scount + 1
			if scount > 2 or (i == 12 and scount > 1 and bins[0] > 0):
				return True
		else:
			scount = 0

	return False

def hasFlushDraw(hand):
	bins = [0, 0, 0, 0]

	for i in range(len(hand)):
		bins[hand[i][1]] += 1

	if bins[0] > 2 or bins[1] > 2 or bins[2] > 2 or bins[3] > 2:
		return True
	else:
		return False

def deal():
	return deck.pop(0)

bigl = 99999
bigw = -99999
games = input('Enter the number of \'games\': ')
trys = input('Enter number of plays: ')
#trys = 100000
plays = input('Enter number of hands per play: ')

totOdds = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
totpay = 0.0
ave = 0.0
for n in tqdm(range(games)):
	payout = 0.0
	count = 0
	odds = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	for k in range(trys):
		h = []
		deck = list(itertools.product(range(0,13), range(0,4)))
		random.shuffle(deck)

		for i in range(5):
			h.append(deal())
		r = eval(h)

		h = discard(h, r)	

		hs = []
		rs = []

		#duplicate the held cards for played hands
		for i in range(plays):
			count += 1
			hs.append(h)
			for j in range(len(hs[i]), 5):
				hs[i].append(deal())
			#eval each hand
			rs.append(eval(hs[i]))
			payout = payout + values[rs[i]]
			odds[rs[i]] = odds[rs[i]] + 1.0

		#if k%10 == 0:
		#	print(rbins)
		#	print(sbins)

	#print(odds)
	for k in range(len(odds)):
		totOdds[k] += odds[k]/count

	#print'GAME: {t}'.format(t=n)
	#print(odds)
	#print'Net Pay: {p}'.format(p=payout)
	#print'Net %: {t}'.format(t=(payout/count))
	if payout > bigw:
		bigw = payout
	elif payout < bigl:
		bigl = payout

	totpay += payout
	ave += payout/count

for k in range(len(totOdds)):
		totOdds[k] = totOdds[k]/games
print'Hands Played per \'game\': {c}'.format(c=plays*trys)
print'\'Average\' odds: {t}'.format(t=totOdds)
print'\'Average\' Net: {t}'.format(t=(totpay/games))
print'\'Average\' Net %: {a}'.format(a=ave/games)
print'\'Max Payout: {b} Min Payout: {l}'.format(b=bigw, l=bigl)
print(stg)