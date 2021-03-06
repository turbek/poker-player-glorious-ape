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
#                     "rank": "10",
#                     "suit": "hearts"
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
#             "rank": "9",
#             "suit": "hearts"
#         },
#         {
#             "rank": "J",
#             "suit": "hearts"
#         },
#         {
#             "rank": "A",
#             "suit": "hearts"
#         },
#         {
#             "rank": "Q",
#             "suit": "clubs"
#         },
#         {
#             "rank": "K",
#             "suit": "clubs"
#         }
#     ]
# }

class Player:
    VERSION = "please work, please"

    def betRequest(self, game_state):
        if len(game_state['community_cards']) == 0:
            if self.preflop(game_state) == "highcards":
                if int(game_state['current_buy_in']) <= int(self.player(game_state)['stack'])/2:
                    return int(game_state['current_buy_in'])
                else:
                    return 0
            elif self.preflop(game_state) == "pairinhand":
                return int(game_state['current_buy_in']) + int(game_state['minimum_raise'])
            elif self.ifpairhand(game_state) == "mediumhand":
                return int(game_state['small_blind'] * 2)
            elif self.preflop(game_state) == "fold":
                return 0
            else:
                return 0
        elif len(game_state['community_cards']) >= 3:
            # print(self.if_straight(game_state))
            # if self.if_straight(game_state):
            #     print("sor")
            #     return 1000
            if self.is_flush(game_state):
                return 10000
            elif self.if_drill(game_state) == "drill":
                print("drill")
                return 10000
            elif self.two_pairs(game_state) == "twopair":
                print("two pairs")
                return 10000
            elif self.ifpair(game_state) == "pair":
                print("pair")
                return int(game_state['current_buy_in']) + int(game_state['minimum_raise'])
            elif self.ifpairhand(game_state) == "pairinhand":
                print("pairinhand")
                return int(game_state['current_buy_in']) + int(game_state['minimum_raise'])
            elif self.ifpairhand(game_state) == "mediumhand":
                print("mediumhand")
                return int(game_state['small_blind']*2)
            elif self.ifhighcards(game_state) == "high":
                print("high")
                if int(game_state['current_buy_in']) <= int(self.player(game_state)['stack'])/4:
                    return int(game_state['current_buy_in'])
                else:
                    return 0
            else:
                print("nothing")
                # print("asd")
                return 0



    def showdown(self, game_state):
        pass

    def preflop(self, game_state):
        list = ['7','8','9','10', 'J', 'Q', 'K', 'A']
        hand = self.hand(game_state)
        if self.ifpairhand(game_state) == "pairinhand":
            return "pairinhand"
        elif hand[0]['rank'] in list and hand[1]['rank'] in list:
            return "highcards"
        else:
            return "fold"

    def ifhighcards(self, game_state):
        high = ['10', 'J', 'Q', 'K', 'A']
        hand = self.hand(game_state)
        if hand[0]['rank'] in high and hand[1]['rank'] in high:
            return "high"
        else:
            return "fold"

    def ifpairhand(self, game_state):
        hand = self.hand(game_state)
        hlist = ['3','4','5','6','7','8','9','10', 'J', 'Q', 'K', 'A']
        mlist = ['2']
        if hand[0]['rank'] == hand[1]['rank']:
            if hand[0]['rank'] in hlist:
                return "pairinhand"
            elif hand[0]['rank'] in mlist:
                return "mediumhand"
            else:
                return "fold"
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

    def is_flush(self, game_state):
        card_suits = []
        list_of_cards = self.community_cards(game_state)
        cards_in_hands = self.hand(game_state)
        list_of_cards.extend(cards_in_hands)

        for card in list_of_cards:
            card_suits.append(card['suit'])

        if card_suits.count('spades') == 5:
            return True
        elif card_suits.count('diamonds') == 5:
            return True
        elif card_suits.count('hearts') == 5:
            return True
        elif card_suits.count('clubs') == 5:
            return True
        else:
            return False

    # def if_straight(self, game_state):
    #     hand = self.hand(game_state)
    #     comm_card = self.community_cards(game_state)
    #     list = []
    #     for i in hand:
    #         if i['rank'] == 'J':
    #             list.append(11)
    #         elif i['rank'] == 'Q':
    #             list.append(12)
    #         elif i['rank'] == 'K':
    #             list.append(13)
    #         elif i['rank'] == 'A':
    #             list.append(14)
    #         else:
    #             list.append(int(i['rank']))
    #     for i in comm_card:
    #         if i['rank'] == 'J':
    #             list.append(11)
    #         elif i['rank'] == 'Q':
    #             list.append(12)
    #         elif i['rank'] == 'K':
    #             list.append(13)
    #         elif i['rank'] == 'A':
    #             list.append(14)
    #         else:
    #             list.append(int(i['rank']))
    #     list = set(list)
    #     list = sorted(list)
    #     listnum = len(list)
    #     count = -1
    #     sorcount = 0
    #     print(list)
    #     for i in list:
    #         count += 1
    #         if i+1 == list[count+1]:
    #             sorcount += 1
    #         else:
    #             count = 0
    #     print(count)
    #     return list






# x = Player()
# x.betRequest(gamestate)
