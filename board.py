
from treys import Deck

from treys import Card

class Board:
    def __init__(self):

        self.deck = Deck()

        # Drawing board
        self.board = self.deck.draw(5)

        # Setting pot to zero
        self.pot = 0

        # Deprecated
       # self.old_deck = self._creer_deck()

    def print_cards(self, phase):
        if phase == "flop":
            self.print_flop()
        elif phase == "turn":
            self.print_turn()
        elif phase == "river":
            self.print_river()



    def print_flop(self):
        # Printing the three first cards
        Card.print_pretty_cards([*self.board[0:3]])

    def print_turn(self):
        # Printing the three first cards
        Card.print_pretty_cards([*self.board[0:4]])

    def print_river(self):
        # Printing the three last cards
        Card.print_pretty_cards([*self.board[0:5]])


    def add_to_pot(self, amount):
        self.pot += amount


    def __str__(self):
        return f"Cartes sur la table : {', '.join(map(str, self.board))} - Pot : {self.pot}"