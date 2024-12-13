import random
from card import Card

class Table:
    def __init__(self):
        self.cartes_table = []
        self.deck = self.create_deck()

    def create_deck(self):
        deck = [Card(v, s) for v in Card.values for s in Card.colors]
        random.shuffle(deck)
        return deck

    def generate_cards(self, nombre):
        return [self.deck.pop() for _ in range(nombre)]

    def add_cards(self, phase):
        if phase == "flop" and len(self.cartes_table) == 0:
            self.cartes_table.extend(self.generate_cards(3))
        elif phase == "turn" and len(self.cartes_table) == 3:
            self.cartes_table.extend(self.generate_cards(1))
        elif phase == "river" and len(self.cartes_table) == 4:
            self.cartes_table.extend(self.generate_cards(1))

    def __str__(self):
        return f"Cartes sur la table : {', '.join(map(str, self.cartes_table))}"