from deuces import Card
from deuces import Deck
from deuces import Evaluator

# Sklansky starting hand groups.
startingHands = [
[1, 1, 2, 2, 3, 5, 5, 5, 5, 5, 5, 5, 5],
[2, 1, 2, 3, 4, 6, 7, 7, 7, 7, 7, 7, 7],
[3, 4, 1, 3, 4, 5, 7, 9, 9, 9, 9, 9, 9],
[4, 5, 5, 1, 3, 4, 6, 8, 9, 9, 9, 9, 9], 
[6, 6, 6, 5, 2, 4, 5, 7, 9, 9, 9, 9, 9],
[8, 8, 8, 7, 7, 3, 4, 5, 8, 9, 9, 9, 9],
[9, 9, 9, 8, 8, 7, 4, 5, 6, 8, 9, 9, 9],
[9, 9, 9, 9, 9, 9, 8, 5, 5, 6, 8, 9, 9],
[9, 9, 9, 9, 9, 9, 9, 8, 6, 7, 7, 9, 9],
[9, 9, 9, 9, 9, 9, 9, 9, 8, 6, 6, 7, 9],
[9, 9, 9, 9, 9, 9, 9, 9, 9, 8, 7, 7, 8],
[9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 7, 8],
[9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 7]
]

# Sklansky groups to playable positions for 'tight' play.
tightPlay = [ 
[],
[0, 1, 2],
[0, 1, 2],
[0, 1, 2],
[1, 2],
[2],
[],
[],
[]
]

# Sklansky groups to playable positions for 'loose' play.
loosePlay = [ 
[],
[0, 1, 2],
[0, 1, 2],
[0, 1, 2],
[0, 1, 2],
[1, 2],
[2],
[],
[]
]


#use to convert from Deuces rank to sklansky table index
#ie rank 0 in Deuces Library is a Two card which is row/column 12 in sklansky table.
rankToIndex = {
0: 12,
1: 11,
2: 10,
3: 9,
4: 8,
5: 7,
6: 6,
7: 5,
8: 4,
9: 3,
10: 2,
11: 1,
12: 0
}

deck = Deck()
eval = Evaluator() 

bigBlind = 2
smallBlind = 1
players = 6
player_Stacks = []

for i in range(players):
	player_Stacks.append(125)

dealer = 0
hand = 0
roundsToPlay = 100
round = 0;

while round < roundsToPlay:

	#init round
	deck.shuffle()
	pot = 0;
	burn = []
	board = []
	folds = []
	player_Hands = []

	#init player hands
	for i in range(players):
		player_Hands.append([])

	#deal cards to players.
	for i in range(dealer+1, players):
		player_Hands[i].append(deck.draw(1))

	for i in range(0, dealer+1):
		player_Hands[i].append(deck.draw(1))

	for i in range(dealer+1, players):
		player_Hands[i].append(deck.draw(1))

	for i in range(0, dealer+1):
		player_Hands[i].append(deck.draw(1))

	#for k in range(2):
	#	for i in range(players):
	#		player_Hands[i].append(deck.draw(1))

	#todo betting round
	
	utg = 0
	if (dealer + 3) < players:
		utg = (dealer + 3)
	else:
		utg = (dealer + 3) - players

	raiser = 0
	small = 0
	big = 0
	if (dealer + 1) < players:
		player_Stacks[dealer+1] -= smallBlind
		small = dealer+1
		if (dealer + 2) < players:
			player_Stacks[dealer+2] -= bigBlind
			big = dealer + 2
		else:
			player_Stacks[0] -= bigBlind
			big = 0
	else:
		player_Stacks[0] -= smallBlind
		small = 0
		player_Stacks[1] -= bigBlind
		big = 1
	raiser = big

	pot += smallBlind + bigBlind

	action = utg
	bet = bigBlind

	paid = []
	for i in range(players):
		paid.append(0)
	paid[small] = smallBlind
	paid[big] = bigBlind

	while action != raiser:
		if folds.count(action) < 1:
			player_Stacks[action] -= (bet - paid[action])
			#print('Player ' + `action` + ' calls ' + `bet-paid[action]`)
			pot += (bet - paid[action])
			paid[action] = (bet - paid[action])


		action += 1
		if action >= players:
			action = 0

	#print('Hand '+`hand`+' Pot size '+`pot`)

	#burn a cards then deal the flop.
	burn.append(deck.draw(1))
	board.extend(deck.draw(3))

	#todo betting round


	#burn then deal turn card
	burn.append(deck.draw(1))
	board.append(deck.draw(1))

	#todo betting round


	#burn then deal river card
	burn.append(deck.draw(1))
	board.append(deck.draw(1))

	#eval hands.
	best = 7463
	second = best-1
	winners = []
	for i in range(players):
		if folds.count(i) < 1:
			s = eval.evaluate(board, player_Hands[i])
			if s < best:
				winners = []
				second = best
				best = s
				winners.append(i)
			elif s == best:
				winners.append(i)

	#show hands.
	if (best < 166) and (second < 166):
		print('Hand '+`hand`+':')

		for i in range(players):
			if folds.count(i) < 1:
				print('Player '+`i`+' -->')
				Card.print_pretty_cards(player_Hands[i])

		print('Board -->')
		Card.print_pretty_cards(board)

		print('Winner(s) with '+eval.class_to_string(eval.get_rank_class(best))+':')
		for i in range(len(winners)):
			print('Player '+`winners[i]`)

		print('Second place was '+eval.class_to_string(eval.get_rank_class(second))+':')
		print('-----------------------------------------------')

	if len(winners) > 1:
		for i in range(len(winners)):
			#print('winner '+`winners[i]`+' paid '+ `pot/len(winners)`)
			player_Stacks[winners[i]] += pot/len(winners)
	else:
		#print('winner '+`winners[0]`+' paid '+ `pot`)
		player_Stacks[winners[0]] += pot

	dealer += 1
	hand += 1
	if dealer >= players:
		dealer = 0
		round += 1
	

print('Results: ')
for i in range(players):
	print('Player '+`i`+' '+`player_Stacks[i]`)

