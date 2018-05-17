import random


class Card(object):

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def show(self):
        print("{}{}".format(self.value, self.suit))


class Deck(object):

    def __init__(self):
        self.deck = []
        self.build()

    def build(self):
        for s in ['d', 'c', 'h', 's']:
            for v in ['A', 2, 3, 4, 5, 6, 7, 8, 9, 'T', 'J', 'Q', 'K']:
                self.deck.append(Card(v, s))

    def shuffle(self):
        for i in range(len(self.deck)-1, 0, -1):
            r = random.randint(0, i)
            self.deck[r], self.deck[i] = self.deck[i], self.deck[r]

    def draw(self, number_of_cards):
        self.drawn_cards = []
        for n in range(0, number_of_cards):
            self.drawn_cards.append(self.deck.pop())
        return self.drawn_cards


class Player(object):

    def __init__(self, name, hand, stack):
        self.name = name
        self.hand = hand
        self.stack = stack
        self.status = "in"
        self.player_bet = -1

    def show_hand(self):
        print("{} has hand:".format(self.name))
        for c in self.hand:
            c.show()

    def show_stack(self):
        print("{} has stack: {}bb".format(self.name, self.stack))

    def bet(self):

        while not 1 <= self.player_bet <= self.stack:
            try:
                self.player_bet = float(input("Enter betsize:"))
            except ValueError:
                print("Enter an integer")

        self.stack = self.stack - self.player_bet

        return self.player_bet

    def call_bet(self, current_bet):

        to_call = current_bet - self.player_bet
        # print(">>>>> to call =", to_call)

        if  self.stack < to_call:
            self.player_bet = self.player_bet + self.stack
            self.stack = 0.0
        else:
            self.player_bet = current_bet
            self.stack = self.stack - to_call

        return to_call

    def raise_bet(self, current_bet):

        if self.stack >= 2*current_bet:
            raise_size = 0
            while not current_bet <= raise_size <= self.stack:
                try:
                    betsize = float(input("Enter betsize:"))
                    raise_size = betsize - current_bet
                except ValueError:
                    print("Enter an integer")

            additional_bet = betsize - self.player_bet
            self.stack = self.stack - additional_bet
            self.player_bet = betsize

        else:
            additional_bet = self.stack
            self.player_bet = self.player_bet + additional_bet
            self.stack = 0.0

        return additional_bet

    # def raise_all_in(self, current_bet):
    #     self.player_bet = self.stack
    #     self.stack = 0

    def option_agg(self):
        choice = None
        while choice not in ('c', 'b'):
            print('c to check, b to bet:')
            choice = input()
        if choice == 'c':
            return 0.0
        if choice == 'b':
            return self.bet()

    def option_def(self, current_bet):
        choice = None
        while choice not in ('f', 'c', 'r'):
            print('f to fold, c to call, r to raise:')
            choice = input()
        if choice == 'f':
            self.status = 'out'
            return 0.0
        elif choice == 'c':
            return self.call_bet(current_bet)
        elif choice =='r':
            return self.raise_bet(current_bet)



class Dealer(object):

    def deal(self, num_players):

        deck = Deck()
        deck.shuffle()

        preflop_all_cards = deck.draw(2 * num_players)
        self.hands = [preflop_all_cards[i:i + 2] for i in range(0, len(preflop_all_cards), 2)]

        preflop = {'name': 'Preflop', 'cards': self.hands}
        flop = {'name': 'Flop', 'cards': deck.draw(3)}
        turn = {'name': 'Turn', 'cards': deck.draw(1)}
        river = {'name': 'River', 'cards': deck.draw(1)}
        showdown = {'name': 'Showdown', 'cards': (flop['cards'] + turn['cards'] + river['cards'])}

        self.streets =  [preflop, flop, turn, river, showdown]

    def show_cards(self, street):
        print("{}:".format(street['name']))

        for card in street['cards']:
            card.show()

    def receive_bet(self, player, hand):
        if hand.max_bet == 0:
            bet_received =  player.option_agg()
        else:
            bet_received = player.option_def(hand.max_bet)

        hand.pot = hand.pot + bet_received

        if player.stack == 0:
            player.status = 'all in'

        return bet_received

    def distribute_pot(self, winner):
        winner.stack = winner.stack + potsize



class Hand(object):

    def __init__(self, player_info):
        self.num_active_players = len(player_info)
        self.active_players = []
        self.all_in_players = []
        self.inactive_players = []
        self.pot = 0

    def show_stacks(self, active_players):
        for player in active_players:
            print("{} has stack {}bb".format(player.name, player.stack))

    def player_action(self, dealer):
        pass

    def play_street(self, dealer, street):

        if street['name'] == 'Preflop':
            for player in self.active_players:
                player.show_hand()
        else:
            dealer.show_cards(street)

        self.show_stacks(self.active_players)

        if street['name'] != 'Showdown':
            self.player_action(dealer)
            while not all(b == self.active_players[0] for b in self.active_players):
                self.player_action(dealer)
        else:
            self.show_stacks(self.inactive_players)


    def play(self):

        dealer = Dealer()
        dealer.deal(self.num_active_players)

        i = 0
        for player in player_info:
            player = Player(player['name'], dealer.hands[i], player['stack'])
            self.active_players.append(player)
            i += 1

        for street in dealer.streets:

            if self.num_active_players > 1:
                self.play_street(dealer, street)



player1 = {'name': 'James', 'stack': 120}
player2 = {'name': 'Ben', 'stack': 100}
player3 = {'name': 'Josh', 'stack': 80}

player_info = [player1, player2, player3]

hand = Hand(player_info)
hand.play()
