# ordering module
import math
import time
import random
import itertools
global module
global randhand
holevalues = []
actions = []
admin = False
player = ""
account = 0
stake = 0
flop = []
turn = []
river = []
board = []
deck = []
hands = []
extended = []
cards = []
gamecondition = 1
players = 2
allHands = []
holeHands = []
hand_dictionary = {}
rank_dictionary = {0:'A', 1:'K', 2:'Q', 3:'J', 4:'10', 5:'9', 6:'8', 7:'7', 8:'6', 9:'5', 10:'4', 11:'3', 12:'2'}
suit_dictionary = {0:'s', 1:'h', 2:'c', 3:'d'}
from handvalue import *

def generate():
        global allHands
        allHands.extend(list(itertools.combinations(range(0, 52), 5)))

def choose(n, r):
	f = math.factorial
	return f(n) / f(r) / f(n-r)

def classorder(ordering):
	place = 0	
	for i in range(0, 6):
		value = 13**(5-i)*ordering[i]
		place = place + value
	return place

def rank(n):
        return n%13

def suit(n):
        return n/13

def card(n):
        return [rank(n), suit(n)]

def parse1(somedeck):
        global players
        hands = []
	print somedeck
        j = 0
        for i in range(0, players):
                hands.append([somedeck[j], somedeck[j+1]])
                j = j + 2
        return hands

def typeorder(ordering):
	return ordering[0]

def english(value):
	key = value/(13**5)
	type_dictionary = {0:'a straight flush', 1:'four of a kind', 2:'a full house', 3:'a flush', 4:'a straight', 5:'three of a kind', 6:'two pair', 7:'a pair', 8:'a high card' }
	return type_dictionary[key]
		

def prepare(cards, type):
	for r in cards:
		prepared = []
	for i in range(0, 5):
		prepared.append(type(cards[i]))

	# order it here
	prepared.sort()
	return prepared 

def highcard(ranks):
	return [8, ranks[0], ranks[1], ranks[2], ranks[3], ranks[4]]

def pair(pair, three, four, five):
	return [7, pair, three, four, five, 0]

def twopair(pair, second, five):
	return [6, pair, second, five, 0, 0]

def triplet(triplet, four, five):
	return [5, triplet, four, five, 0, 0]

def straight(to):
	return [4, to, 0, 0, 0, 0]

def flush(ranks):
	return [3, ranks[0], ranks[1], ranks[2], ranks[3], ranks[4]]

def house(set, pair):
	return [2, set, pair, 0, 0, 0]

def quatre(quatre, five):
	return [1, quatre, five, 0, 0, 0]

def flushed(to):
	return [0, to, 0, 0, 0, 0]

def order_by(ranks, suits):
	if ranks[0] == ranks[1]:
		if ranks[0] == ranks[2]:
			if ranks[0] == ranks[3]:
				ordering = quatre(ranks[0], ranks[4])
			elif ranks[3] == ranks[4]:
				ordering = house(ranks[0], ranks[3])
			else:
				ordering = triplet(ranks[0], ranks[3], ranks[4])
		elif ranks[2] == ranks[3]:
			if ranks[2] == ranks[4]:
				ordering = house(ranks[2], ranks[0])
			else:
				ordering = twopair(ranks[0], ranks[2], ranks[4])
		elif ranks[3] == ranks[4]:
			ordering = twopair(ranks[0], ranks[3], ranks[2])
		else:
			ordering = pair(ranks[0], ranks[2], ranks[3], ranks[4])
	elif ranks[1] == ranks[2]:
		if ranks[1] == ranks[3]:
			if ranks[1] == ranks[4]:
				ordering = quatre(ranks[1], ranks[0])
			else:
				ordering = triplet(ranks[1], ranks[0], ranks[4])
		elif ranks[3] == ranks[4]:
			ordering = twopair(ranks[1], ranks[3], ranks[0])	
		else:
			ordering = pair(ranks[1], ranks[0], ranks[3], ranks[4])		
	elif ranks[2] == ranks[3]:
		if ranks[3] == ranks[4]:
			ordering = triplet(ranks[2], ranks[0], ranks[1])
		else:
			ordering = pair(ranks[2], ranks[0], ranks[1], ranks[4])
	elif ranks[3] == ranks[4]:
		ordering = pair(ranks[3], ranks[0], ranks[1], ranks[2])
	elif ranks[0] == ranks[1] - 1 == ranks[2] - 2 == ranks[3] - 3 == ranks[4] - 4:
		if suits[0] == suits[4]:
			ordering = flushed(ranks[0])
		else:
			ordering = straight(ranks[0])
	elif ranks[0] + 8 == ranks[1] - 1 == ranks[2] - 2 == ranks[3] - 3 == ranks[4] - 4:
		if suits[0] == suits[4]:
			ordering = flushed(ranks[4])
		else:
			ordering = straight(ranks[4])
	elif suits[0] == suits[4]:
		ordering = flush(ranks)
	else:
		ordering = highcard(ranks)

	return ordering

def order(cards, ordermethod):
	return ordermethod(order_by(prepare(cards, rank), prepare(cards, suit)))

def transform(hands, method):
	transformed = []
	for hand in hands:
		transformed.append(order(hand, method))
	return transformed

def hash_cards(cards):
	hash = ""
	cards = sorted(cards)
	rank_dictionary = {0:'A', 1:'K', 2:'Q', 3:'J', 4:'10', 5:'9', 6:'8', 7:'7', 8:'6', 9:'5', 10:'4', 11:'3', 12:'2'}
	suit_dictionary = {0:'s', 1:'h', 2:'c', 3:'d'}
	for i in range(0, 5):
		hash = hash + rank_dictionary[rank(cards[i])] + suit_dictionary[suit(cards[i])]
	return hash

def translate(cards):
	global rank_dictionary
	global suit_dictionary
	english = []
	#cards = sorted(cards)
	for card in cards:
		english.append(rank_dictionary[rank(card)] + suit_dictionary[suit(card)])
	return ", ".join(english) 

def hash_hands(orderedhands):
	hashmap = {}
	for i in range(0,len(orderedhands)):
		hashmap[hash_cards(orderedhands[i])] = i
	return hashmap

def reverse_hash_hands(orderedhands):
	hashmap = {}
	for i in range(0,len(orderedhands)):
		hashmap[i] = hash_cards(orderedhands[i])
	return hashmap

def hash_class_weight(classed):
	classes = set(classed)
	weight = {}
	for cl in classes:
		weight[cl] = classed.count(cl)
	return weight	

def orderhands(hands):
	return sorted(hands, key=order_by)	

def timer(function, args=None):
	start = time.time()
	function(args)
	print time.time() - start

def class_array(hands):
	classed = []
	for h in hands:
		classed.append(order(h))
	return classed

def number(hand):
	return order(hand, classorder)

def choose_best(seven):
	global hand_dictionary
	choices = list(itertools.combinations(seven, 5))	
	values = []
	for choice in choices:
		values.append(number(choice)) 
		hand_dictionary[number(choice)] = choice
	return min(values)

def choose_hand(values):
        if values[0] < values[1]:
		return 1
        elif values[0] == values[1]:
		return 0
        else:
		return 2

def declare_hand(value):
	print translate(hand_dictionary[value])

def declare_hands(values):
	for value in values:
		declare_hand(value)

def hand_ranks(handvalues):
	i = 0
	j = 0
	k = 0
	handlose = {}
	handtie = {}
	handwin = {}
	for handvalue in handvalues:
		for hand in handvalues:
			if hand < handvalue:
				i = i + handvalues[hand]
			if hand == handvalue:
				j = j + handvalues[hand]
			if hand > handvalue:
				k = k + handvalues[hand]
		handlose[handvalue] = i
		handtie[handvalue] = j
		handwin[handvalue] = k
		i = 0
		j = 0
		k = 0
	handoutcome = [handlose, handtie, handwin]
	return handoutcome

def win_chance(numbered_cards):
	return handoutcome[2][numbered_cards]/float(choose(52, 5))
	
def print_outcomes(cards):
	worsethan = handoutcome[0][number(cards)]/float(len(allHands))
	equalto = handoutcome[1][number(cards)]/float(len(allHands))
	betterthan = handoutcome[2][number(cards)]/float(len(allHands))
	print 'Worse than:',worsethan*100,'%'
	#print 'Equal to:',equalto,'%'
	print 'Better than:',betterthan*100,'%'
	print 'of all possible hands'

def generate_hole():
	global holeHands
        holeHands.extend(list(itertools.combinations(range(0, 52), 2)))
	
def convert_hole():
	global holeHands
	convertedHole = []
	for hole in holeHands:
		ranks = [rank(hole[0]), rank(hole[1])]
		ranks.sort()
		transformed = [ranks, suit(hole[0]) == suit(hole[1])]
		if transformed not in convertedHole:
			convertedHole.append(transformed)
			print transformed
		else:
			pass
	holeHands = convertedHole

def value_hole_hand(hand):
	deck = range(0, 52)
	deck.remove(hand[0])
	deck.remove(hand[1])
	extended = list(itertools.combinations(deck, 5))
	goodness = 0
	for extend in extended:
		goodness = goodness + win_chance(choose_best(hand+extend))
	print goodness

def order_hole():
	global holeHands
	generate_hole()
	convert_hole()
	print holeHands	

def hash_hole(hole):
	value = 13*rank(hole[0])+rank(hole[1])
	if suit(hole[0]) == suit(hole[1]):
		value = value + 169
	return value

def hash_all_holes(holeHands):
	global holevalues
	for hole in holeHands:
		holevalues.append([hole, hash_hole(hole)])
	print holevalues
	
