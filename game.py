from treys import Card

from board import Board
from player import Player


class Game:
    def __init__(self, players):
        self.table = Board()

        self.players = [Player(name, 1000) for name in players]
        self.dealerIndex = 0
        self.smallBlindIndex = 0
        self.bigBlindIndex = 0
        self.min_bet = 0
        self.pot = 0
        self.round_over = False
        self.current_bets = {player.name: 0 for player in self.players}

    def start_game(self):
        print("Début de la partie...")

        self.blind_betting()

        for player in self.players:
            player.cards = self.table.generer_cartes(2)
            player.treyCards = self.table.generer_treys_cartes(2)

        print("\n--- Cartes des joueurs ---")
        for player in self.players:
            # print(
            #   f"Les cartes : {', '.join(map(str, Card.int_to_pretty_str(player.treyCards)))} du joueur {player.name},")
            print("Les cartes du joueur " + player.name)
            Card.print_pretty_cards(player.treyCards)

        print("Cartes distribuées.")
        print("\n--- État initial de la table ---")
        print(self.table)

        print("\n===> Phase avant le flop : Mise pré-flop <===")
        self.pre_flop_betting()

        if self.round_over: return

        print("\n===> Phase actuelle : Flop <===")
        self.table.add_cards("flop")
        print(self.table)

        self.handle_betting()

        if self.round_over: return

        print("\n===> Phase actuelle : Turn <===")
        self.table.add_cards("turn")
        print(self.table)

        self.handle_betting()

        if self.round_over: return

        print("\n===> Phase actuelle : River <===")
        self.table.add_cards("river")
        print(self.table)

        self.handle_betting()

        if self.round_over: return

        self.showdown()

    def blind_betting(self):

        # The first player posts small blind, the second player posts big blind
        self.players[self.smallBlindIndex].bet_chips(10)  # Small blind
        self.current_bets[self.players[0].name] += 10  # Track contribution to pot

        self.players[self.bigBlindIndex].bet_chips(20)  # Big blind
        self.current_bets[self.players[1].name] += 20  # Track contribution to pot

        self.pot += 30  # Add blinds to the pot
        print(f"{self.players[0].name} posts small blind of 10")
        print(f"{self.players[1].name} posts big blind of 20")

        # Set the minimum bet for the first round
        self.min_bet = 20  # The big blind is 20, so the minimum bet is now 20.

    def pre_flop_betting(self):
        while True:
            for player in self.players:
                if not player.is_active:
                    continue

                montant_a_suivre = self.min_bet - self.current_bets[player.name]

                while True:
                    print(f"{player.name}, vous avez {player.chips} jetons.")
                    print(f"Pot total : {self.pot} jetons")
                    print(f"Votre contribution au pot : {self.current_bets[player.name]} jetons")
                    print(f"Montant à suivre : {montant_a_suivre}")

                    if montant_a_suivre > 0:
                        action = input("Voulez-vous [B]et ou [F]old ? ").strip().lower()
                    else:
                        action = input("Voulez-vous [B]et, [F]old, ou [C]heck ? ").strip().lower()

                    if action == 'b':
                        try:
                            amount = int(input(
                                f"Combien voulez-vous miser ? (minimum {montant_a_suivre if montant_a_suivre > 0 else 1}) : "))
                        except ValueError:
                            print("Veuillez entrer un montant valide.")
                            continue

                        if montant_a_suivre > 0 and amount < montant_a_suivre:
                            print(f"Erreur : Vous devez suivre au moins {montant_a_suivre}.")
                            continue
                        if amount > player.chips:
                            print("Vous n'avez pas assez de jetons.")
                            continue

                        if amount > montant_a_suivre:
                            self.min_bet = amount

                        player.bet_chips(amount)
                        self.current_bets[player.name] += amount
                        self.pot += amount
                        break

                    elif action == 'f':
                        player.fold()
                        print(f"{player.name} se couche.")
                        break

                    elif action == 'c' and montant_a_suivre == 0:
                        print(f"{player.name} choisit de checker.")
                        break

                    else:
                        print("Action invalide. Veuillez choisir une action valide.")

            active_players = [p for p in self.players if p.is_active]
            contributions = [self.current_bets[p.name] for p in active_players]
            if len(active_players) == 1:
                print(f"{active_players[0].name} gagne car tous les autres se sont couchés.")
                self.round_over = True
                return
            if len(set(contributions)) == 1:
                break
        print(f"Fin de la phase de mise. Pot total : {self.pot} jetons")

    def handle_betting_round(self, phase_name=""):
        print(f"\n=== Phase actuelle : {phase_name} ===")
        while True:
            for player in self.players:
                if not player.is_active:
                    continue

                montant_a_suivre = self.min_bet - self.current_bets[player.name]
                print(f"{player.name}, vous avez {player.chips} jetons.")
                print(f"Pot total : {self.pot} jetons. Votre contribution : {self.current_bets[player.name]} jetons.")
                print(f"Montant à suivre : {montant_a_suivre}")

                if montant_a_suivre > 0:
                    action = input("Voulez-vous [B]et ou [F]old ? ").strip().lower()
                else:
                    action = input("Voulez-vous [B]et, [F]old, ou [C]heck ? ").strip().lower()

                if self.handle_action(player, action, montant_a_suivre):
                    break

                if self.bets_balanced():
                    break

            print(f"Fin de la phase de mise. Pot total : {self.pot} jetons.")

    def handle_action(self, player, action, montant_a_suivre):
        if action == 'b':
            try:
                amount = int(input(f"Combien voulez-vous miser ? (minimum {montant_a_suivre}) : "))
            except ValueError:
                print("Veuillez entrer un montant valide.")
                return False

            if amount < montant_a_suivre:
                print(f"Erreur : Vous devez suivre au moins {montant_a_suivre}.")
                return False
            if amount > player.chips:
                print("Vous n'avez pas assez de jetons.")
                return False

            player.bet_chips(amount)
            self.current_bets[player.name] += amount
            self.pot += amount

            # Relance
            if amount > montant_a_suivre:
                print(f"{player.name} relance à {amount} jetons.")
                self.min_bet = amount
            return True

        elif action == 'f':  # Se coucher
            player.fold()
            print(f"{player.name} se couche.")
            return True

        elif action == 'c' and montant_a_suivre == 0:  # Checker
            print(f"{player.name} choisit de checker.")
            return True

        else:
            print("Action invalide. Veuillez réessayer.")
            return False

    def bets_balanced(self):
        active_players = [p for p in self.players if p.is_active]
        contributions = [self.current_bets[p.name] for p in active_players]
        return len(set(contributions)) == 1
