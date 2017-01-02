import itertools, random
from tqdm import tqdm
from deuces import Deck, Card, Evaluator

values = [49, 49, 8, 6, 3, 1, 0, -1,-1]
bonus = [0.0, 79.0, 159.0, 399.0, 799.0]
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
			break

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
			break

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
			break

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

	h = []
	for i in range(len(hand)-1, -1, -1):
	 	if keep.count(Card.get_rank_int(hand[i])) > 0:
			h.append(hand.pop(i))
			if (len(h) == len(keep)):
				break

	# if len(keep) > 2:
	# 	#remove cards not in straight
	# 	for i in range(len(hand)-1, -1, -1):
	# 		if keep.count(Card.get_rank_int(hand[i])) == 0:
	# 			hand.pop(i)

	# 	#remove duplicates
	# 	have = []
	# 	for k in range(len(hand)-1, -1, -1):
	# 		if have.count(Card.get_rank_int(hand[k])) < 1:
	# 			have.append(Card.get_rank_int(hand[k]))
	# 		else:
	# 			hand.pop(k)

	# print 'holding straight draw: '
	# print keep
	# Card.print_pretty_cards(hand)

	return h

def holdFlushDraw(hand):
	bins = [0, 0, 0, 0, 0, 0, 0, 0, 0]

	for i in range(len(hand)):
		bins[Card.get_suit_int(hand[i])] += 1

	
	if bins[1] > 2:
		for k in range(len(hand)-1, -1, -1):
			if Card.get_suit_int(hand[k]) != 1:
				hand.pop(k)
	elif bins[2] > 2:
		for k in range(len(hand)-1, -1, -1):
			if Card.get_suit_int(hand[k]) != 2:
				hand.pop(k)
	elif bins[4] > 2:
		for k in range(len(hand)-1, -1, -1):
			if Card.get_suit_int(hand[k]) != 4:
				hand.pop(k)
	elif bins[8] > 2:
		for k in range(len(hand)-1, -1, -1):
			if Card.get_suit_int(hand[k]) != 8:
				hand.pop(k)

	# print 'holding flush draw: '
	# Card.print_pretty_cards(hand)

	return hand

def holdFourSet(hand):

	bins = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	for i in range(len(hand)):
		bins[Card.get_rank_int(hand[i])] += 1

	save = -1
	for i in range(len(bins)):
		if bins[i] == 4:
			save = i
			break

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
		bins[Card.get_suit_int(hand[i])] += 1

	if bins[1] > 2 or bins[2] > 2 or bins[4] > 2 or bins[8] > 2:
		# print bins
		return True
	else:
		return False

ev = Evaluator()
ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
suits = ['c', 's', 'd', 'h']

aces = [ Card.new('Ac'), Card.new('As'), Card.new('Ad'), Card.new('Ah') ]
jacks = [ Card.new('Tc'), Card.new('Ts'), Card.new('Ac'), Card.new('Kc'), Card.new('Qc') ]

jackScore = ev.evaluate(jacks, [])

AcesLow = {}
for k in range(1, 4):
	for i in range(4):
		s = ranks[k] + suits[i]
		aces.append(Card.new(s))
		#Card.print_pretty_cards(aces)
		AcesLow[ev.evaluate(aces, [])] = 1
		aces.pop(4)

LowLow = {}
for k in range(1, 4):

	q = []
	for i in range(4):
		s = ranks[k] + suits[i]
		q.append(Card.new(s))
	
	for r in range(k):
		for i in range(4):
			s = ranks[r] + suits[i]
			q.append(Card.new(s))
			#Card.print_pretty_cards(q)
			LowLow[ev.evaluate(q, [])] = 1
			q.pop(4)

	for r in range(k+1,4):
		for i in range(4):
			s = ranks[r] + suits[i]
			q.append(Card.new(s))
			#Card.print_pretty_cards(q)
			LowLow[ev.evaluate(q, [])] = 1
			q.pop(4)

AcesHigh = {}
for k in range(4, 13):
	for i in range(4):
		s = ranks[k] + suits[i]
		aces.append(Card.new(s))
		#Card.print_pretty_cards(aces)
		AcesHigh[ev.evaluate(aces, [])] = 1
		aces.pop(4)

LowHigh = {}
for k in range(1, 4):

	q = []
	for i in range(4):
		s = ranks[k] + suits[i]
		q.append(Card.new(s))
	
	for r in range(4, 13):
		for i in range(4):
			s = ranks[r] + suits[i]
			q.append(Card.new(s))
			#Card.print_pretty_cards(q)
			LowHigh[ev.evaluate(q, [])] = 1
			q.pop(4)

deck = Deck()


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
	count = 0
	payout = 0.0
	odds = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	for k in range(trys):

		deck.shuffle()
		h1 = deck.draw(5)
		
		score = ev.evaluate(h1, [])
		r = ev.get_rank_class(score)-1 

		h2 = discard(h1[:], r)	

		# print 'before'
		# Card.print_pretty_cards(h1)
		# print 'after'
		# Card.print_pretty_cards(h2)

		hs = []
		rs = []	
		
		#duplicate the held cards for played hands
		for i in range(plays):
			count += 1
			hs.append(h2[:])
			for j in range(len(hs[i]), 5):
				hs[i].append(deck.draw(1))
			#eval each hand
			score = ev.evaluate(hs[i], [])
			rs.append(ev.get_rank_class(score)-1)
			if (rs[i] == 7) and (score < jackScore):
			 	#print 'Jacks or Better'
			 	#Card.print_pretty_cards(hs[i])
			 	payout += bonus[0]
			elif rs[i] == 1:
				if score in AcesLow:
					# print 'hit Four Aces w/ 2-4 on Game {g}'.format(g=n)
					# Card.print_pretty_cards(hs[i])
					payout += bonus[4]
				elif score in AcesHigh:
					# print 'hit Four Aces w/ 5-k on Game {g}'.format(g=n)
					# Card.print_pretty_cards(hs[i])
					payout += bonus[2]
				elif score in LowLow:
					# print 'hit Four 2-4 w/ A-4 on Game {g}'.format(g=n)
					# Card.print_pretty_cards(hs[i])
					payout += bonus[3]
				elif score in LowHigh:
					# print 'hit Four 2-4 w/ 5-k on Game {g}'.format(g=n)
					# Card.print_pretty_cards(hs[i])
					payout += bonus[1]
				else:
					# print 'hit Four 5-k on Game {g}'.format(g=n)
					# Card.print_pretty_cards(hs[i])
					payout += values[rs[i]]
			elif (score == 1):
				# print 'hit Royal Flush on Game {g}'.format(g=n)
				# Card.print_pretty_cards(hs[i])
				payout += bonus[4]
			else:
				payout += values[rs[i]]
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