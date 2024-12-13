from cmath import phase

from treys import Card

from board import Board
from player import Player


class Game:
    def __init__(self, players):
        # Board initialization
        self.board = Board()
        # Every player is assigned 1000 chips
        self.players = [Player(name, 1000) for name in players]

        # Positions
        self.dealerIndex = 0
        self.smallBlindIndex = 0
        self.bigBlindIndex = 1

        # Bets and pot
        self.min_bet = 0
        self.pot = 0

        # Flag that indicates whether this round is terminated
        self.round_over = False

        # ???
        self.last_raise = 0

    '''
    This method extracts current bets for each player
    '''
    def get_current_bets(self):
        return {player.name: 0 for player in self.players}

    def start_game(self):

        # Initialization and card distribution
        print("Début de la partie...")
        self.print_player_cards()
        print("Cartes distribuées.")

        # Initializing blinds
        self.blind_betting()

        # Main loop
        phase_index = 0
        phases = ["pré-flop", "flop", "turn", "river"]
        while not self.round_over and phase_index < len(phases):
            phase = phases[phase_index]
            print(f"\n===> Phase actuelle : {phase} <===")
            self.print_player_cards()
            print("=========Cartes de la table===========")
            self.board.print_cards(phase)
            self.handle_bet(phase)
            phase_index += 1

        if not self.round_over:
            self.showdown()


    '''
    Blind initialization
    Initially set to 20
    '''
    def blind_betting(self):
        self.players[self.smallBlindIndex].bet_chips(10)
        self.get_current_bets()[self.players[self.smallBlindIndex].name] += 10
        self.pot += 10

        self.players[self.bigBlindIndex].bet_chips(20)
        self.get_current_bets()[self.players[self.bigBlindIndex].name] += 20
        self.pot += 20

        print("\n--- État initial de la table ---")

        print(f"{self.players[0].name} petite blind de 10")
        print(f"{self.players[1].name} grosse blind de 20")

        self.min_bet = 20



    def bets_balanced(self):
        active_players = [p for p in self.players if p.is_active]
        contributions = [self.get_current_bets()[p.name] for p in active_players]
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
            self.get_current_bets()[player.name] += amount
            self.pot += amount

            if amount > amount_to_folllow:
                self.min_bet = self.get_current_bets()[player.name]
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


    def get_active_players(self):
        return [p for p in self.players if p.is_active]

    def handle_bet(self, phase):
        while True:

            # If only one player is active, it wins the round
            if len(self.get_active_players()) == 1:
                winner = self.get_active_players()[0]
                print(f"{winner.name} gagne car tous les autres se sont couchés.")
                winner.chips += self.pot
                self.pot = 0
                self.round_over = True
                if phase == "pré-flop":
                    self.round_over = True
                break

            # If multiple active players
            index = 0
            while len(self.get_active_players()) > 1 and index < len(self.get_active_players()):
                player = self.get_active_players()[index]

                # Minimal amount to follow
                amount_to_follow = max(0, self.min_bet - self.get_current_bets()[player.name])
                print(f"{player.name}, vous avez {player.chips} jetons.")
                print(f"Pot total : {self.pot} jetons. Votre contribution : {self.get_current_bets()[player.name]} jetons.")
                print(f"Montant à suivre : {amount_to_follow}")

                if amount_to_follow > 0:
                    action = input("Voulez-vous [B]et ou [F]old ? ").strip().lower()
                else:
                    # If the amount to follow is above 0, we can check too
                    action = input("Voulez-vous [B]et, [F]old, ou [C]heck ? ").strip().lower()

                if not self.handle_action(player, action, amount_to_follow):
                    continue

                # If the player has fold, we continue
                if not player.is_active:
                    # In this case, we break
                    break

                index += 1

            if len(self.get_active_players()) > 1 and self.bets_balanced():
                print("Mises équilibrées")
                break





    def print_player_cards(self):
        print("\n--- Cartes des joueurs ---")
        for player in self.players:
            print("Les cartes du joueur " + player.name)
            Card.print_pretty_cards(player.treyCards)

    def showdown(self):
        print("\nPhase de Showdown !")


'''
    Pre flop ne fonctionne que si on bet. Fold mal fait

'''