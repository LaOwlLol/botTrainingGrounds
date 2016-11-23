import itertools, random
from deuces import Card, Deck, Evaluator

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
def holdStraightDraw(hand):
	bins = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	for i in range(len(hand)):
		bins[Card.get_rank_int(hand[i])] += 1

	keep = []
	last = 0

	if bins[0] > 0:
		keep.append(0)

	for i in range(13):
		if bins[i] > 0 and i == (last+1):
			last = i
			keep.append(i)
		elif bins[i] > 0 and i > (last+1):
			last = i
			del keep[:]
			keep.append(i)

	if len(keep) == 2 and last == 3 and bin[12] > 0:
		keep.append(12);
	elif len(keep) == 3 and last == 4 and bin[12] > 0:
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

	print 'holding straight draw: '
	Card.print_pretty_cards(hand)

	return hand

deck = Deck()
evl = Evaluator()

h = deck.draw(5)
s = evl.evaluate(h, [])
c = evl.get_rank_class(s)
#print s
#print c
Card.print_pretty_cards(h)
print evl.class_to_string(c)

if c == 9:
	h = holdHigh(h)
if hasStraightDraw(h):
	h = holdStraightDraw(h)

Card.print_pretty_cards(h)

for i in range(len(h), 5):
	h.append(deck.draw(1))
Card.print_pretty_cards(h)

s = evl.evaluate(h, [])
c = evl.get_rank_class(s)
#print s
#print c
print evl.class_to_string(c)

for i in range(10):
	print Card.get_suit_int(deck.draw(1))
