class Card:
    valeurs = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    sortes = ['Trèfle', 'Carreau', 'Cœur', 'Pique']

    def __init__(self, valeur, sorte):
        self.valeur = valeur
        self.sorte = sorte

    def __str__(self):
        return f"{self.valeur} de {self.sorte}"