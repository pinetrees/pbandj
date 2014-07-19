#!/usr/bin/python
import random 
import pickle
players = 2
size = 5 + 2*players
population = range(0, 52)
cards = random.sample(population, size)
from ordering import *
from globals import *
generate()

def clear_players():
	global loggedin
	player = ""
	players = []
	playerkey = {}
	pickle.dump(players, open("players.pl", "w"))
	pickle.dump(playerkey, open("playerkey.pl", "w"))
	loggedin = False

def register_player():
	players = pickle.load(open("players.pl", "r"))
	playerkey = pickle.load(open("playerkey.pl", "r"))
	try:
		name = raw_input('enter your name: ')
		players.append([name, 100])
		playerkey[name] = len(players)-1
		print "you're registered, ", name, ". you have 100 chips. go login"
	except ValueError:
		print "no"
	pickle.dump(players, open("players.pl", "w"))
	pickle.dump(playerkey, open("playerkey.pl", "w"))

def list_players():
	playerkey = pickle.load(open("playerkey.pl", "r"))
	for playername in playerkey:
		print playername

def load_player():
	global account
	global player
	global module
	players = pickle.load(open("players.pl", "r"))
	playerkey = pickle.load(open("playerkey.pl", "r"))
	playername = raw_input('name: ')
	if playername in playerkey:
		player = playername
		account = players[playerkey[player]][1]
		players[playerkey[player]][1] = 0
		pickle.dump(players, open("players.pl", "w"))
		print "Welcome,", player
		balance()
		change_module(account_module)
	else:
		print 'this is not a player'
		
def increment_account():
	global account
	account = account + 1

def dump_player():
	global account
	global player
	global module
	global gamecondition
	players = pickle.load(open("players.pl", "r"))
	playerkey = pickle.load(open("playerkey.pl", "r"))
	if player == "":
		return
	players[playerkey[player]][1] = account
	pickle.dump(players, open("players.pl", "w"))
	print "Goodbye, ", player
	print account, "chips have been stored"
	account = 0
	player = ""
	if gamecondition == 1:
		change_module(startup_module)
	else:
		return

def hand_result(values):
        global account
        global stake
	print 'Your hand: '
	declare_hand(values[0])
        if choose_hand(values) == 1:
                print "Hand one wins with", english(values[0])
                account = account + 2*stake 
                stake = 0
        elif choose_hand(values) == 0:
                print "A tie with", english(values[0])
                account = account + stake
                stake = 0
        else:
		print translate(hands[1])
		declare_hand(values[1])
		print "Hand two wins with", english(values[1])
                stake = 0

def balance():
        print "Your balance is", account

def bet(wager):
        global stake
	stake = stake + wager

def pot():
	global stake
	print 'The pot is', stake*2

def place_bet(round):
        global account
        print "Your balance is: ", account, ", how much will you bet?"
	try:
       		wager = int(raw_input('>>'))
       		bet(wager)
		if round == 0:
			record_action(wager)
		account = account - wager
	except ValueError:
		print "You have bet 0"

def opposition():
	print 'The opposition calls.'

def record_action(wager):
	global actions
	holedata = hash_hole(hands[0])
	actions.append([holedata, wager])
	print actions

def deal():
	global cards
	global flop
	global turn
	global river
	global deck
	global hands
	global extended
	deck = random.sample(population, size)
	flop = [deck[4], deck[5], deck[6]]
	turn = [deck[7]]
	river = [deck[8]]
	hands = parse1(deck)
	showhand()
	place_bet(0)
	opposition()
	pot()
	showflop()
	place_bet(1)
	opposition()
	pot()
	showturn()
	place_bet(22)
	opposition()
	pot()
	showriver()
	place_bet(3)
	opposition()
	pot()
	result()

def quit():
	global gamecondition
	gamecondition = 0
	dump_player()
	return gamecondition
	
def options():
	for f in range(1, len(module)):
		print '<',f,'>', module[f][1]

def showhand():
	print 'Your hand: ', translate(hands[0])

def showflop():
	showhand()
	print 'Board: ', translate(flop)

def showturn():
	showhand()
	print 'Board: ', translate(flop + turn)

def showriver():
	showhand()
	print 'Board: ', translate(flop + turn + river)

def showboard():
	print translate(flop + turn + river)

def showdeck():
	print translate(deck)

def result():
	values = []
	for hand in hands:
		values.append(choose_best(hand + flop + turn + river))
	hand_result(values)
	balance()

def enter_game():
	global module
	change_module(game_module)

def enter_training():
	global module
	change_module(training_module)

def enter_admin():
	global module
	global admin
	change_module(admin_module)
	admin = True

def enter_testing():
	global module
	change_module(testing_module)

def change_module(new_module):
	global module
	module = new_module
	module[0][0]()

def module_information():
	global module
	print 'This is the',module[0][1], 'module'	

def random_hole():
	global deck
	global randhand
	randhand = random.sample(deck, 2)
	for item in randhand:
		deck.remove(item)
	print translate(randhand)

def player_hole():
	global deck
	global hands
	hole = random.sample(deck, 2)
	hands.append(hole)
	for item in hole:
		deck.remove(item)
	print translate(hole)
	
def opponent_hole():
	global deck
	global hands
	hole = random.sample(deck, 2)
	hands.append(hole)
	for item in hole:
		deck.remove(item)

def generate_flop():
	global deck
	global flop
	global board
	flop = random.sample(deck, 3)
	for item in flop:
		board.append(item)
		deck.remove(item)
	print translate(hands[0])
	print translate(board)

def generate_turn():
	global deck
	global turn
	global board
	turn = random.sample(deck, 1)
	for item in turn:
		board.append(item)
		deck.remove(item)
	print translate(hands[0])
	print translate(board)


def random_hand(type):
	global randhand
	randhand = random.sample(population, 5)
	if type == 9:
		print translate(randhand)
		return
	i = 0
	while number(randhand)/13**5 != type:
		i = i + 1
		randhand = random.sample(population, 5)
	print "I looked through",i,"hands to find you",english(number(randhand))
	print randhand
	print translate(randhand)
	
def select_hand():
	global randhand
	randhand = []
	deck = range(0, 52)
	while len(randhand) < 5:
		options = []
		for rank in rank_dictionary:
			print '<',rank,'>', rank_dictionary[rank]
		cardrank = int(raw_input('>'))
		for suit in suit_dictionary:
			if cardrank + 13*suit in deck:
				options.append(suit)
				print '<',suit,'>', suit_dictionary[suit]
		cardsuit = int(raw_input('>'))
		if cardsuit not in options:
			print 'not an option'
		else:
			card = 13*cardsuit + cardrank
			deck.remove(card)
			randhand.append(card)
			print randhand
	print translate(randhand)

def random_any():
	global randhand
	random_hand(9)

def random_flushed():
	global randhand
	random_hand(0)

def random_flush():
	global randhand
	random_hand(3)

def random_straight():
	global randhand
	random_hand(4)

def randhand_rank():
	global randhand
	print "you have",english(number(randhand))
	print_outcomes(randhand)

def reload_deck():
	global deck
	global hands
	global flop
	global turn
	global river
	hands = []
	flop = []
	turn = []
	river = []
	deck = range(0, 52)
	print deck

def print_deck():
	global deck
	print translate(deck)
	
startup_module = [[module_information, 'startup'], [load_player, 'login'], [register_player, 'register'], [quit, 'quit']]

startup_module.append([enter_testing, 'testing'])

account_module = [[module_information, 'account'], [enter_game, 'game'], [enter_training, 'training'], [balance, 'see balance'], [dump_player, 'logout'], [enter_admin, 'admin'], [quit, 'quit']]

admin_module = [[module_information, 'admin']]

game_module = [[module_information, 'game'], [deal, 'deal a new hand'], [balance, 'see balance'], [quit, 'quit the game'], [clear_players, 'clear players'], [dump_player, 'logout'], [increment_account, 'buy chips'], [list_players, 'list players']]

training_module = [[module_information, 'training'], [print_deck, 'see the deck'], [select_hand, 'choose a hand'], [random_hole, 'generate random hole cards'], [random_any, 'generate a random hand'], [random_flushed, 'generate a random straight flush'], [random_flush, 'generate a random flush'], [random_straight, 'generate a random straight'], [randhand_rank, 'see how the hand ranks'], [quit, 'quit']]

testing_module = [[module_information, 'testing']]

def test_function():
	func = raw_input('enter the function, be careful!: ')
	exec(func)

testing_module.append([test_function, 'test a function'])

training_module.append([reload_deck, 'load the deck'])
training_module.append([player_hole, 'generate your hole cards'])
training_module.append([opponent_hole, 'generate an opponent"s hole cards'])
training_module.append([generate_flop, 'generate the flop'])
training_module.append([generate_turn, 'generate the turn'])

def generate_river():
	global deck
	global river
	global board
	river = random.sample(deck, 1)
	for item in river:
		board.append(item)
		deck.remove(item)
	print translate(hands[0])
	print translate(board)

training_module.append([generate_river, 'generate the river'])
training_module.append([result, 'see the result'])

function_dictionary = {'options':options, 'balance':balance, 'bet':place_bet, 'pot':pot, 'deal':deal, 'quit':quit, 'hand':showhand, 'flop':showflop, 'turn':showturn, 'river':showriver, 'board':showboard, 'deck':showdeck, 'result':result }
number_dictionary = {'0':options, 'balance':balance, 'bet':place_bet, 'pot':pot, 'deal':deal, 'quit':quit, 'hand':showhand, 'flop':showflop, 'turn':showturn, 'river':showriver, 'board':showboard, 'deck':showdeck, 'result':result }

change_module(startup_module)
randhand = random.sample(population, 5)
while (gamecondition == 1):
	while (admin == True):
		try:
			exec(raw_input('enter a command: '))
		except ValueError:
			print 'please try that again'
	try:
		options()
		rawfunc = raw_input('>')
		func = int(rawfunc)
       		if func in range(1, len(module)):
			module[func][0]()
		elif func == 0:
			change_module(startup_module)
		else:
			print "null"
	except ValueError:
		pass
