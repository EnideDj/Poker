import random

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
        self.old_deck = self._creer_deck()

    def print_flop(self):
        # Printing the three first cards
        Card.print_pretty_cards([*self.board[0:3]])

    def print_turn(self):
        # Printing the three first cards
        Card.print_pretty_cards([*self.board[3:4]])

    def print_river(self):
        # Printing the three last cards
        Card.print_pretty_cards([*self.board[4:5]])

    def _creer_deck(self):
        deck = [Card(v, s) for v in Card.valeurs for s in Card.sortes]
        random.shuffle(deck)
        return deck

    def generer_cartes(self, nombre):
        return [self.deck.pop() for _ in range(nombre)]

    def generer_treys_cartes(self, nombre):
        return self.treysDeck.draw(nombre)

    def add_to_pot(self, amount):
        self.pot += amount

    def add_cards(self, phase):
        if phase == "flop" and len(self.board) == 0:
            self.board.extend(self.generer_cartes(3))
        elif phase == "turn" and len(self.board) == 3:
            self.board.extend(self.generer_cartes(1))
        elif phase == "river" and len(self.board) == 4:
            self.board.extend(self.generer_cartes(1))


    def __str__(self):
        return f"Cartes sur la table : {', '.join(map(str, self.board))} - Pot : {self.pot}"