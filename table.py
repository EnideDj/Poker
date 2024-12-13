import random
from card import Card

class Table:
    def __init__(self):
        self.cartes_table = []
        self.pot = 0
        self.deck = self._creer_deck()

    def _creer_deck(self):
        deck = [Card(v, s) for v in Card.valeurs for s in Card.sortes]
        random.shuffle(deck)
        return deck

    def _generer_cartes(self, nombre):
        return [self.deck.pop() for _ in range(nombre)]

    def add_to_pot(self, amount):
        self.pot += amount

    def add_cards(self, phase):
        if phase == "flop" and len(self.cartes_table) == 0:
            self.cartes_table.extend(self._generer_cartes(3))
        elif phase == "turn" and len(self.cartes_table) == 3:
            self.cartes_table.extend(self._generer_cartes(1))
        elif phase == "river" and len(self.cartes_table) == 4:
            self.cartes_table.extend(self._generer_cartes(1))

    def __str__(self):
        return f"Cartes sur la table : {', '.join(map(str, self.cartes_table))} - Pot : {self.pot}"