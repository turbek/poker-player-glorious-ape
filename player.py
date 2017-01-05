# gamestate = {
#     "tournament_id":"550d1d68cd7bd10003000003",     # Id of the current tournament
#
#     "game_id":"550da1cb2d909006e90004b1",           # Id of the current sit'n'go game. You can use this to link a
#                                                     # sequence of game states together for logging purposes, or to
#                                                     # make sure that the same strategy is played for an entire game
#
#     "round":0,                                      # Index of the current round within a sit'n'go
#
#     "bet_index":0,                                  # Index of the betting opportunity within a round
#
#     "small_blind": 10,                              # The small blind in the current round. The big blind is twice the
#                                                     #     small blind
#
#     "current_buy_in": 80,                          # The amount of the largest current bet from any one player
#
#     "pot": 400,                                     # The size of the pot (sum of the player bets)
#
#     "minimum_raise": 240,                           # Minimum raise amount. To raise you have to return at least:
#                                                     #     current_buy_in - players[in_action][bet] + minimum_raise
#
#     "dealer": 1,                                    # The index of the player on the dealer button in this round
#                                                     #     The first player is (dealer+1)%(players.length)
#
#     "orbits": 7,                                    # Number of orbits completed. (The number of times the dealer
#                                                     #     button returned to the same player.)
#
#     "in_action": 1,                                 # The index of your player, in the players array
#
#     "players": [                                    # An array of the players. The order stays the same during the
#         {                                           #     entire tournament
#
#             "id": 0,                                # Id of the player (same as the index)
#
#             "name": "Albert",                       # Name specified in the tournament config
#
#             "status": "active",                     # Status of the player:
#                                                     #   - active: the player can make bets, and win the current pot
#                                                     #   - folded: the player folded, and gave up interest in
#                                                     #       the current pot. They can return in the next round.
#                                                     #   - out: the player lost all chips, and is out of this sit'n'go
#
#             "version": "Default random player",     # Version identifier returned by the player
#
#             "stack": 1010,                          # Amount of chips still available for the player. (Not including
#                                                     #     the chips the player bet in this round.)
#
#             "bet": 0                              # The amount of chips the player put into the pot
#         },
#         {
#             "id": 1,                                # Your own player looks similar, with one extension.
#             "name": "Glorious Ape",
#             "status": "active",
#             "version": "Default random player",
#             "stack": 1590,
#             "bet": 80,
#             "hole_cards": [                         # The cards of the player. This is only visible for your own player
#                                                     #     except after showdown, when cards revealed are also included.
#                 {
#                     "rank": "K",                    # Rank of the card. Possible values are numbers 2-10 and J,Q,K,A
#                     "suit": "hearts"                # Suit of the card. Possible values are: clubs,spades,hearts,diamonds
#                 },
#                 {
#                     "rank": "K",
#                     "suit": "spades"
#                 }
#             ]
#         },
#         {
#             "id": 2,
#             "name": "Chuck",
#             "status": "out",
#             "version": "Default random player",
#             "stack": 0,
#             "bet": 0
#         }
#     ],
#     "community_cards": [                            # Finally the array of community cards.
#         {
#             "rank": "10",
#             "suit": "spades"
#         },
#         {
#
#             "rank": "A",
#
#
#             "suit": "hearts"
#         },
#         {
#             "rank": "8",
#             "suit": "clubs"
#         }
#     ]
# }

class Player:
    VERSION = "destroying team orange HAHAHAHA"

    def betRequest(self, game_state):
        # if len(game_state['community_cards']) == 0:
        #     if self.preflop(game_state) == "highcards" or "pairinhand":
        #         return 20
        # elif len(game_state['community_cards']) > 3:
        if self.if_drill(game_state) == "drill":
            # print("drill")
            return 1000
        elif self.two_pairs(game_state) == "twopair":
            # print("two pairs")
            return 1000
        elif self.ifpair(game_state) == "pair":
            # print("pair")
            return 1000
        elif self.ifpairhand(game_state) == "pairinhand":
            # print("pairinhand")
            return 1000
        elif self.ifhighcards(game_state) == "high":
            # print("high")
            return int(self.player(game_state)['stack'])/2
        # elif self.ifhighcards(game_state) == "10":
        #     print("10")
        #     return 200
        else:
            # print("nothing")
            return 0



    def showdown(self, game_state):
        pass

    def preflop(self, game_state):
        list = ['10', 'J', 'Q', 'K', 'A']
        hand = self.hand(game_state)
        if self.ifpairhand(game_state) == "pairinhand":
            return "pairinhand"
        elif hand[0]['rank'] in list and hand[1]['rank'] in list:
            return "highcards"
        else:
            return "fold"

    def ifhighcards(self, game_state):
        high = ['J', 'Q', 'K', 'A']
        hand = self.hand(game_state)
        if hand[0]['rank'] in high and hand[1]['rank'] in high:
            return "high"
        else:
            return "fold"

    def ifpairhand(self, game_state):
        hand = self.hand(game_state)
        if hand[0]['rank'] == hand[1]['rank']:
            return "pairinhand"
        else:
            return "fold"

    def ifpair(self, game_state):
        hand = self.hand(game_state)
        comm = self.community_cards(game_state)
        list = []
        for i in comm:
            list.append(i['rank'])
        for i in list:
            if hand[0]["rank"] == i or hand[1]["rank"] == i:
                return 'pair'


    def if_drill(self, game_state):
        hand = self.hand(game_state)
        comm = self.community_cards(game_state)
        list = []
        for i in comm:
            list.append(i['rank'])
        count = 0
        count2 = 0
        for i in list:
            if hand[0]['rank'] == i:
                count += 1
        if self.ifpairhand(game_state) == "pairinhand":
            for i in list:
                if hand[0]['rank'] == i:
                    count2 += 1
        if count == 2 or count2 == 1:
            return 'drill'
        else:
            return 'fold'

    def player(self, game_state):
        for player in game_state['players']:
            if player['name'] == 'Glorious Ape':
                return player

    def hand(self, game_state):
        player = self.player(game_state)
        return player['hole_cards']

    def community_cards(self, game_state):
        return game_state['community_cards']

    def two_pairs(self, game_state):
        hand = self.hand(game_state)
        comm_card = self.community_cards(game_state)
        if hand[0]['rank'] != hand[1]['rank']:
            comm_card_values = set([])
            for card in comm_card:
                comm_card_values.add(card["rank"])
            if hand[0]['rank'] in comm_card_values and hand[1]['rank'] in comm_card_values:
                return "twopair"
            else:
                return "fold"





# x = Player()
# x.betRequest(gamestate)
