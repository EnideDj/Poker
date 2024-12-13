from cmath import phase

from treys import Card, Evaluator

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


    '''
    This method extracts current bets for each player
    '''
    def get_current_bets(self):
        return {player.name: player.currentBet for player in self.players}

    def start_game(self):

        print("Début de la partie...")

        while len(self.players) > 1:
            self.round_over = False
            # Initialization and card distribution
            self.print_player_cards()
            print("Cartes distribuées.")

            # Initializing blinds
            self.blind_betting()
            self.afficher_jetons()
            # Main loop
            phase_index = 0
            phases = ["pré-flop", "flop", "turn", "river"]
            while not self.round_over and phase_index < len(phases):
                # Resetting player
                for player in self.players:
                    player.is_fold = True
                phase = phases[phase_index]
                print(f"\n===> Phase actuelle : {phase} <===")
                self.print_player_cards()
                print("=========Cartes de la table===========")
                self.board.print_cards(phase)
                self.handle_bet(phase)
                phase_index += 1

            # If the round was not terminated in pre-flop
            if not self.round_over:
                self.showdown()


    '''
    Blind initialization
    Initially set to 20
    '''
    def blind_betting(self):
        self.players[self.smallBlindIndex].bet_chips(10)
        #self.get_current_bets()[self.players[self.smallBlindIndex].name] += 10
        self.pot += 10

        self.players[self.bigBlindIndex].bet_chips(20)
        #self.get_current_bets()[self.players[self.bigBlindIndex].name] += 20
        self.pot += 20

        print("\n--- État initial de la table ---")

        print(f"{self.players[0].name} petite blind de 10")
        print(f"{self.players[1].name} grosse blind de 20")

        self.min_bet = 20


    def afficher_jetons(self):

        print("\n Affichage des jetons : ")
        for player in self.players:
            print(f"{player.name} : {player.chips} jetons")

    def bets_balanced(self):
        active_players = [p for p in self.players if p.is_fold]
        contributions = [self.get_current_bets()[p.name] for p in active_players]
        # If all the bets are equal, then the length of the associated is 1
        # We also must verify that we go to the next phase if
        return len(set(contributions)) == 1 and len(self.players) - len(active_players) < 2

    def handle_action(self, player, action, amount_to_follow):
        while True:
            if action == 'b':
                try:
                    amount = int(input(f"Combien voulez-vous miser ? (minimum {amount_to_follow}) : "))
                except ValueError:
                    print("Veuillez entrer un montant valide.")
                    continue
                    # return False
                if amount < amount_to_follow:
                    print(f"Erreur : Vous devez suivre au moins {amount_to_follow}.")
                    continue
                    # return False
                if amount > player.chips:
                    print("Vous n'avez pas assez de jetons.")
                    continue
                     # return False

                player.bet_chips(amount)
                #{player.name: 0 for player in self.players}[player.name] += amount
                self.pot += amount

                if amount > amount_to_follow:
                    self.min_bet = self.get_current_bets()[player.name]
                    print(f"{player.name} relance à {amount} jetons.")
                else:
                    print(f"{player.name} suit avec {amount} jetons.")
                return True

            elif action == 'f':
                player.fold()
                print(f"{player.name} se couche.")
                return "FOLD"

                '''
                elif action == 'c':
                # TODO: check chips
                if amount_to_follow > player.chips:
                    print("Vous n'avez pas assez de jetons. Réessayez")
                    continue
                player.bet_chips(amount_to_follow)
                {player.name: 0 for player in self.players}[player.name] += amount_to_follow
                self.pot += amount_to_follow
                return True
                '''
            else:
                print("Action invalide. Veuillez réessayer.")
                return False


    def get_active_players(self):
        return [p for p in self.players if p.is_fold]

    def handle_bet(self, phase):

        # Players that folds at preflop
        # To not disturb our looo, we remove players later
        abandoned_players = []
        # Asking every player what to do
        for player in self.players:
            # Minimal amount to follow
            amount_to_follow = max(0,self.min_bet - min(self.get_current_bets().values()))
            print(f"\n\n{player.name}, vous avez {player.chips} jetons.")
            print(f"Pot total : {self.pot} jetons. Votre contribution : {self.get_current_bets()[player.name]} jetons.")
            print(f"Montant à suivre : {amount_to_follow}")

            if amount_to_follow > 0:
                action = input("Voulez-vous [B]et ou [F]old ? ").strip().lower()
            #else:
                # If the amount to follow is above 0, we can check too
             #   action = input("Voulez-vous [B]et, [F]old, ou [C]heck ? ").strip().lower()

            result = self.handle_action(player, action, amount_to_follow)
            ##if not self.handle_action(player, action, amount_to_follow):

            # If a player folds at pre-flop, she abandons the game
            if phase == 'pré-flop' and result == "FOLD":
                print(f"{player.name} abandonne la main.")
                player.fold()
                abandoned_players.append(player)



        # If only one player is active, she wins the round
        if len(self.get_active_players()) == 1:
            winner = self.get_active_players()[0]
            print(f"{winner.name} gagne car tous les autres se sont couchés.")
            if phase == "pré-flop":
                self.round_over = True
                self.afficher_jetons()
                for player in self.players:
                    player.is_fold = False


        else:
            # We go to the next phase if
            # 1 - There is more than one active player (if the other folded the player wins)
            # 2 - All the players have chosen their action
            if len(self.get_active_players()) > 1 and self.bets_balanced():
                if phase == 'pré-flop':
                    print("Les mises sont équilibrées. Passons à la prochaine phase")
                print("Mises équilibrées")



    def print_player_cards(self):
        print("\n--- Cartes des joueurs ---")
        for player in self.players:
            print("Les cartes du joueur " + player.name)
            Card.print_pretty_cards(player.treyCards)

    def showdown(self, isRoundComplete=True):
        print("\nPhase de Showdown !")

        evaluator = Evaluator()
        scores = {player.name : evaluator.evaluate(self.board.board, player.treyCards) for player in self.players}
        ranks = [evaluator.class_to_string(evaluator.get_rank_class(score)) for score in scores.values()]

        for i in range(len(ranks)):
            print(f"Player {self.players[i]} hand rank = {scores[self.players[i].name]} ({ranks[i]})\n")

        winner_name = max(scores, key=scores.get)
        print(f"Le grand gagnant est {winner_name} !")

        winner = [player for player in self.players if player.name == winner_name]

        # Winner gains the pot
        print(f"{winner_name} remporte le pot de {self.pot} jetons !")
        winner[0].chips += self.pot
        # Pot is reset
        self.pot = 0

        self.afficher_jetons()

        for player in self.players:
            if player.chips <= 0:
                print(f'{player.name} est a court de jetons ! Elimination !')
                self.players.remove(player)
            # Resetting bet amount
            player.reset_current_bet()





