from treys import Deck


class Player:
    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.cards = []
        self.treyCards = Deck().draw(2)
        self.is_fold = True
        self.currentBet = 0

    def bet_chips(self, amount):
        if not amount > self.chips:
            self.chips -= amount
            self.currentBet += amount
            return amount

    def fold(self):
        self.is_fold = False

    def reset_current_bet(self):
        self.currentBet = 0

    def __str__(self):
        return f"{self.name} - Jetons : {self.chips} - Cartes : {', '.join(map(str, self.cards))}"