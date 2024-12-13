class Card:
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    colors = ['Trèfle', 'Carreau', 'Cœur', 'Pique']

    def __init__(self, value, color):
        self.value = value
        self.color = color

    def __str__(self):
        return f"{self.value} de {self.color}"