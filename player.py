from treys import Deck


class Player:
    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.cards = []
        self.treyCards = Deck().draw(2)
        self.is_active = True

    def bet_chips(self, amount):
        if amount > self.chips:
            raise ValueError("Not enough chips")
        self.chips -= amount
        return amount

    def fold(self):
        self.is_active = False

    @staticmethod
    def check():
        return True  

    def __str__(self):
        return f"{self.name} - Jetons : {self.chips} - Cartes : {', '.join(map(str, self.cards))}"