import itertools
from tqdm import tqdm
from deuces import Deck, Card, Evaluator

ev = Evaluator()
deck = Deck()

count = input('Enter number of hands to play: ')

for k in tqdm(range(count)):
	
	deck.shuffle()

	#get a hand and turn it into a key
	h = deck.draw(5)
	score1 = ev.evaluate(h, [])

