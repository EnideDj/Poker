from table import Table
from player import Player

class Game:
    def __init__(self, players):
        self.board = Board()

        self.players = [Player(name, 1000) for name in players]
        self.dealerIndex = 0
        self.smallBlindIndex = 0
        self.bigBlindIndex = 0
        self.min_bet = 0
        self.pot = 0
        self.round_over = False
        self.current_bets = {player.name: 0 for player in self.players}
        self.last_raise = 0

    def start_game(self):
        print("Début de la partie...")

        for player in self.players:
            player.cards = self.table.generate_cards(2)

        print("\n--- Cartes des joueurs ---")
        for player in self.players:
            print(f"Les cartes : {', '.join(map(str, player.cards))} du joueur {player.name},")

        print("Cartes distribuées.")
        print("\n--- État initial de la table ---")
        print(self.table)

        self.blind_betting()

        for phase in ["pré-flop", "flop", "turn", "river"]:
            if self.round_over:
                break
            print(f"\n===> Phase actuelle : {phase} <===")

            if phase == "pré-flop":
                self.pre_flop_betting()
            else:
                self.table.add_cards(phase)
                print(self.table)
                self.handle_betting(phase)

        if not self.round_over:
            self.showdown()

    def blind_betting(self):
        self.players[0].bet_chips(10)
        self.current_bets[self.players[0].name] += 10
        self.pot += 10

        self.players[1].bet_chips(20)
        self.current_bets[self.players[1].name] += 20
        self.pot += 20

        print(f"{self.players[0].name} petite blind de 10")
        print(f"{self.players[1].name} grosse blind de 20")

        self.min_bet = 20

    def pre_flop_betting(self):
        print("\n=== Phase actuelle : pré-flop ===")

        while True:
            active_players = [p for p in self.players if p.is_active]

            if len(active_players) == 1:
                winner = active_players[0]
                print(f"{winner.name} gagne car tous les autres se sont couchés.")
                winner.chips += self.pot
                self.pot = 0
                self.round_over = True
                return

            for player in self.players:
                if not player.is_active:
                    continue

                amount_to_follow = max(0, self.min_bet - self.current_bets[player.name])
                print(f"{player.name}, vous avez {player.chips} jetons.")
                print(f"Pot total : {self.pot} jetons. Votre contribution : {self.current_bets[player.name]} jetons.")
                print(f"Montant à suivre : {amount_to_follow}")

                if amount_to_follow > 0:
                    action = input("Voulez-vous [B]et ou [F]old ? ").strip().lower()
                else:
                    action = input("Voulez-vous [B]et, [F]old, ou [C]heck ? ").strip().lower()

                if not self.handle_action(player, action, amount_to_follow):
                    continue

            if self.bets_balanced():
                print("Les mises sont équilibrées. La phase suivante peut commencer.")
                break

    def handle_betting_for_player(self, player):
        amount_to_folllow = max(0, self.min_bet - self.current_bets[player.name])
        print(f"{player.name}, vous avez {player.chips} jetons.")
        print(f"Pot total : {self.pot} jetons. Votre contribution : {self.current_bets[player.name]} jetons.")
        print(f"Montant à suivre : {amount_to_folllow}")

        if amount_to_folllow > 0:
            action = input("Voulez-vous [B]et ou [F]old ? ").strip().lower()
        else:
            action = input("Voulez-vous [B]et, [F]old, ou [C]heck ? ").strip().lower()

        self.handle_action(player, action, amount_to_folllow)

    def handle_betting(self, phase_name):
        print(f"\n=== Phase actuelle : {phase_name} ===")

        while True:
            active_players = [p for p in self.players if p.is_active]

            if len(active_players) == 1:
                winner = active_players[0]
                print(f"{winner.name} gagne car tous les autres se sont couchés.")
                winner.chips += self.pot
                self.pot = 0
                self.round_over = True
                return

            for player in self.players:
                if not player.is_active:
                    continue

                amount_to_folllow = max(0, self.min_bet - self.current_bets[player.name])
                print(f"{player.name}, vous avez {player.chips} jetons.")
                print(f"Pot total : {self.pot} jetons. Votre contribution : {self.current_bets[player.name]} jetons.")
                print(f"Montant à suivre : {amount_to_folllow}")

                if amount_to_folllow > 0:
                    action = input("Voulez-vous [B]et ou [F]old ? ").strip().lower()
                else:
                    action = input("Voulez-vous [B]et, [F]old, ou [C]heck ? ").strip().lower()

                if not self.handle_action(player, action, amount_to_folllow):
                    continue

            if self.bets_balanced():
                print("Les mises sont équilibrées. La phase suivante peut commencer.")
                break

    def bets_balanced(self):

        active_players = [p for p in self.players if p.is_active]
        contributions = [self.current_bets[p.name] for p in active_players]
        return len(set(contributions)) == 1

    def handle_action(self, player, action, amount_to_folllow):
        if action == 'b':
            try:
                amount = int(input(f"Combien voulez-vous miser ? (minimum {amount_to_folllow}) : "))
            except ValueError:
                print("Veuillez entrer un montant valide.")
                return False

            if amount < amount_to_folllow:
                print(f"Erreur : Vous devez suivre au moins {amount_to_folllow}.")
                return False
            if amount > player.chips:
                print("Vous n'avez pas assez de jetons.")
                return False

            player.bet_chips(amount)
            self.current_bets[player.name] += amount
            self.pot += amount

            if amount > amount_to_folllow:
                self.min_bet = self.current_bets[player.name]
                print(f"{player.name} relance à {amount} jetons.")
            else:
                print(f"{player.name} suit avec {amount} jetons.")
            return True

        elif action == 'f':
            player.fold()
            print(f"{player.name} se couche.")
            return True

        elif action == 'c' and amount_to_folllow == 0:
            print(f"{player.name} choisit de checker.")
            return True

        else:
            print("Action invalide. Veuillez réessayer.")
            return False

    def showdown(self):
        print("\nPhase de Showdown !")
