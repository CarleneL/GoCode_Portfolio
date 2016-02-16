'''

BlackJack Game

User Stories:

1) User can play the blackjack game in terminal against the dealer
2) Dealer automatically plays his hand with a fixed algorithm (If it's 16 or below they hit, if it's above 16, they stay)
3) User can play the blackjack game repeatedly
4) User can choose to hit or stay
5) User can see what cards they have been dealt
6) User can only see one dealer card, not the bottom card

'''
from random import randint
from random import shuffle

'''
Basic Card class. 
Each Card is composed of a suit and it's value
'''
class Card(object):
	def __init__(self,suit,value):
		self.suit = suit
		self.value = value

	def get_value(self):
		return str(self.value) + "-" + self.suit

	def __str__(self):
		return str(self.value) + "-" + str(self.suit)

'''
The deck class is composed of cards.
Has the capability to create, shuffle, and deal cards
'''
class Deck(object):
	def __init__(self):
		self.size = 52
		self.array_of_cards = []

	def make_deck(self):
		suits = ["hearts", "diamonds", "spades", "clubs"]
		values = [2,3,4,5,6,7,8,9,10,"Jack", "Queen", "King", "Ace"]
		self.array_of_cards = [Card(suit, val) for suit in suits for val in values]
		Deck.shuffle(self)

	def print_deck(self):
		string = ""
		for card in self.array_of_cards:
			#print "|" + str(card.value) + "-" + card.suit
			print card.get_value()
		#return string
		
	def shuffle(self):
		shuffle(self.array_of_cards)

	def deal(self):
		return self.array_of_cards.pop()

'''
The Hand class is a list of cards
It has the ability to calculate it's value, and determine if it is busted or has blackjack
'''
class Hand(object):
	def __init__(self, list_of_cards):
		self.hand = list_of_cards
		self.score = 0
		self.busted = False
		self.blackjack = False

	def value_of_hand(self):
		self.score = 0
		for card in self.hand:
			if card.value in ["Jack", "Queen", "King"]:
				self.score += 10
			elif card.value == "Ace":
				continue
			else:
				self.score += card.value
		for card in self.hand:
			if card.value == "Ace":
				Hand.handle_ace(self)

		Hand.is_busted(self)
		Hand.is_blackjack(self)

	def handle_ace(self):
		if self.score <= 10:
			self.score += 11
		else:
			self.score +=1 
		
	def is_busted(self):
		if self.score >21:
			self.busted = True

	def is_blackjack(self):
		if self.score == 21:
			self.blackjack = True

	def add_card(self, card):
		self.hand.append(card)
		Hand.value_of_hand(self)

	def show_hand(self):
		string = ""
		for card in self.hand:
			string += "|" + str(card)
		string += "|"
		return string

'''
The player class has a name and holds a hand. 
There is only one method to request another card if the player chooses to hit
'''
class Player(object):
	def __init__(self, name, hand):
		self.name = name
		self.hand = hand

	def hit(self, deck_of_cards):
		self.hand.add_card(deck_of_cards.deal())

'''
The Dealer class extends Player and overrides the hit method. 
Dealer hits so long as the value of his hand is less than or equal to 17
The Deal class also has a method to reveal all but one of their cards
'''
class Dealer(Player):
	def hit(self, deck_of_cards):
		if self.hand.score <= 17:
			self.hand.add_card(deck_of_cards.deal())
		else:
			return False

	def dealers_hand(self):
		dealer_hand = self.hand.show_hand()
		first_card = str(self.hand.hand[0])
		return dealer_hand.replace(first_card,"*")

'''
This is the Game Engine
The play method kicks of the game loop 
All the other helper methods initialize the game attributes and calculate the score
'''
class Game(object):
	def __init__(self):
		self.keep_playing = True
		self.deck = None
		self.players = []

	def init_deck(self):
		print "Let's play blackjack!"
		self.deck = Deck()
		self.deck.make_deck()

	def deal_hands(self):
		return [self.deck.deal(), self.deck.deal()]

	def init_players(self, name = ""):
		self.players.append(Dealer("Dealer",Hand(Game.deal_hands(self))))
		self.players.append(Player("Player 1", Hand(Game.deal_hands(self))))
		for plyr in self.players:
			plyr.hand.value_of_hand()
			plyr.hand.value_of_hand()

	def player_turn(self, player):
		while not (player.hand.busted or player.hand.blackjack):
			user_choice = raw_input("Would you you like to hit or stay: ").lower().strip()
			if user_choice == "hit":
				player.hit(self.deck)
				print player.hand.show_hand()
			elif user_choice == "stay":
				break
			else:
				print "I don't understand your choice. Please try again"
				continue
		if player.hand.busted:
			print player.name + " busted. Dealer wins."
		elif player.hand.blackjack:
			print player.name + " has Blackjack!"

	def dealer_turn(self, dealer):
		print "**** Dealers turn ****"
		print dealer.dealers_hand()
		while not dealer.hand.busted:
			if dealer.hand.score <= 17:
				dealer.hit(self.deck)
				print "Dealer Hits"
				print dealer.dealers_hand()
			else:
				print "Dealer stays"
				break
		if dealer.hand.busted:
			print "Dealer busted."
		elif dealer.hand.blackjack:
			print "Dealer has Blackjack!"

	def check_scores(self, list_of_players):
		if list_of_players[0].hand.score == list_of_players[1].hand.score:
			print "It's a draw"
		elif list_of_players[0].hand.score > list_of_players[1].hand.score:
				print list_of_players[0].name + " wins!"
		else:
			print list_of_players[1].name + " wins!"

	def find_winner(self, list_of_players):
		if not len(list_of_players):
			print "No winner this round!"
		elif len(list_of_players) == 1:
			print list_of_players[0].name + " is the winner!"
		else:
			self.check_scores(list_of_players)

	def keep_playing_game(self):
		while True:
			choice = raw_input("Want to play a new game Y or N? ").lower()
			if choice == "n":
				self.keep_playing = False
				break
			elif choice == "y":
				self.deck = None
				self.players = []
				break
			else:
				print "Please enter Y or N"

	def play(self):
		while self.keep_playing:
			self.init_deck()
			self.init_players()
			card_dealer = self.players[0]
			player1 = self.players[1]

			print player1.hand.show_hand()
			self.player_turn(player1)

			if not player1.hand.busted:
				self.dealer_turn(self.players[0])
			for player in self.players:
				print player.name + ": " + player.hand.show_hand()

			self.find_winner(filter(lambda x: not x.hand.busted, self.players))
			
			self.keep_playing_game()


g = Game()
g.play()



	


















