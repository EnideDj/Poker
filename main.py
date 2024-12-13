from game import Game


def main():
    print("Enide Djender - Arnaud Endignous")
    print("Bienvenue au Texas Hold'em Poker !")
    player_names = []

    while True:
        try:
            num_players = int(input("Combien de joueurs participent ? (2-6) : "))
            if 2 <= num_players <= 6:
                break
            print("Veuillez entrer un nombre entre 2 et 6.")
        except ValueError:
            print("Entrée invalide. Veuillez entrer un nombre.")

    for i in range(num_players):
        name = input(f"Entrez le nom du joueur {i + 1} : ")
        player_names.append(name)

    game = Game(player_names)
    game.start_game()


if __name__ == "__main__":
    main()