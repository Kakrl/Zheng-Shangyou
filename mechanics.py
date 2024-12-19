import random

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Player:
    def __init__(self, hand, is_past_winner, score):
        self.hand = hand
        self.is_past_winner = is_past_winner
        self.score = score
        self.card_dict = {
            0:  '3',
            1:  '3',
            2:  '4',
            3:  '5',
            4:  '6',
            5:  '7',
            6:  '8',
            7:  '9',
            8:  '10',
            9:  'Jack',
            10: 'Queen',
            11: 'King',
            12: 'Ace',
            13: '2',
            14: 'Black Joker',
            15: 'Red Joker'
        }
        self.power_dict = {
            '3':            0,
            '4':            1,
            '5':            2,
            '6':            3,
            '7':            4,
            '8':            5,
            '9':            6,
            '10':           7,
            'Jack':         8,
            'Queen':        9,
            'King':        10,
            'Ace':         11,
            '2':           12,
            'Black Joker': 13,
            'Red Joker':   14
        }
        self.playable_moves = {
            'single': False,
            'single run': False,
            'pair': False,
            'pair run': False,
            'triple no-carry': False,
            'triple single-carry': False,
            'triple pair-carry': False,
            'triple bomb': False,
            'quad bomb': False,
            'joker bomb': False
        }
    
    def display_hand(self):
        hand = ''
        for idx in range(16):
            for count in range(self.hand[idx]):
                hand += self.card_dict[idx] + ', '
        print(hand[:-2])
    
    def display_options(self, rules): #only called when all cards can be played
        print("These are the possible options you can play:")
        self.playable_moves['single'] = True
        if rules[2] == 'y': #min three singles in a row for a run
            threshold = 3
        else:
            threshold = 5
        in_a_row = 1
        for num in self.hand:
            if num != 0:
                in_a_row += 1
            else:
                in_a_row = 1
            if in_a_row == threshold:
                self.playable_moves['single run'] = True
                break
        for count in self.hand:
            if count >= 2:
                self.playable_moves['pair'] = True
                break
        if rules[0] == 'y': #min two pair for a run
            threshold = 2
        else:
            threshold = 3
        in_a_row = 1
        for count in self.hand:
            if count >= 2:
                in_a_row += 1
            else:
                in_a_row = 1
            if in_a_row == threshold:
                self.playable_moves['pair run'] = True
                break
        if rules[1] == 'y': #triple is a bomb
            for count in self.hand:
                if count >= 3:
                    self.playable_moves['triple bomb'] = True
        else:
            for count in self.hand:
                if count >= 3:
                    self.playable_moves['triple no-carry'] = True
                    if sum(self.hand) >= 4:
                        self.playable_moves['triple single-carry'] = True
                        #need triple pair-carry <-----------------------------------------------------------
        if rules[3] == 'y': #yes to joker bomb
            if self.hand[14] == 1 and self.hand[15] == 1:
                self.playable_moves['joker bomb'] = True
        for count in self.hand:
            if count == 4:
                self.playable_moves['quad bomb'] = True
        return [moves for moves, is_allowed in self.playable_moves.items() if is_allowed]
    
    def can_play(self, rules, play_type, last_played):
        if play_type == 'single':
            for card, count in enumerate(self.hand):
                if count != 0 and card > last_played:
                    return True
        elif play_type == 'single run':
            if rules[2] == 'y': #min three singles in a row for a run
                threshold = 3
            else:
                threshold = 5
            in_a_row = 1
            for card, count in enumerate(self.hand):
                if count != 0:
                    in_a_row += 1
                else:
                    in_a_row = 1
                if in_a_row >= threshold and (card-threshold+1) > last_played:
                    return True
        elif play_type == 'pair':
            for card, count in enumerate(self.hand):
                if (count >= 2 and card > last_played) or (rules[3] == 'n' and self.hand[14] == 1 and self.hand[15] == 1): #no joker bomb edge case
                    return True
        elif play_type == 'pair run':
            if rules[0] == 'y': #min two pair for a run
                threshold = 2
            else:
                threshold = 3
            in_a_row = 1
            for card, count in enumerate(self.hand):
                if count >= 2:
                    in_a_row += 1
                else:
                    in_a_row = 1
                if in_a_row == threshold and (card-threshold+1) > last_played:
                    return True
        elif play_type == 'triple no-carry':
            if rules[1] == 'n':
                for card, count in enumerate(self.hand):
                    if count >= 3 and card > last_played:
                        return True
        elif play_type == 'triple single-carry':
            if rules[1] == 'n':
                for card, count in enumerate(self.hand):
                    if count >= 3:
                        if sum(self.hand) >= 4 and card > last_played:
                            return True
        elif play_type == 'triple pair-carry':
            pass
        elif play_type == 'triple bomb' or (rules[1] == 'y' and play_type != 'quad bomb' and play_type != 'joker bomb'):
            pass
        elif play_type == 'quad bomb' or play_type != 'joker bomb':
            pass
        #check for bomb
        if rules[3] == 'y' and self.hand[14] == 1 and self.hand[15] == 1: #joker bomb
            return True
        return False
    
    def pick_possible_start_cards(self, rules, play_type, last_played):
        return None
    
    def pick_option(self, rules, is_new_round, option_type, last_played):
        print("It's your turn! Here is your hand:")
        Player.display_hand(self)
        if is_new_round:
            play_types = Player.display_options(self, rules)
            msg = 'Out of these options, which would you like to play? '
            options = '('
            for option in play_types:
                options += option + ', '
            options = options[:-2] + ')\n'
            play_type = input(msg + options)
            while play_type not in play_types:
                play_type = input("Please try again. " + options)
        else: #confirm if player can play or not
            if Player.can_play(self, rules, play_type, last_played):
                play_type = input("Would you like to play or pass? (play/pass)\n")
                while play_type not in ['play', 'pass']:
                    play_type = input("Please try again. (play/pass)\n")
                if play_type == 'play':
                    play_type = option_type
                else:
                    print("You passed.")
            else:
                print("No playable moves! Auto-passing.")
        if play_type != 'pass':
            last_played = Player.pick_possible_start_cards(self, rules, play_type, last_played)
        return play_type, last_played
    
    def bot1_pick(self, rules, is_new_round, option_type, last_played):
        return option_type, last_played
    
    def bot2_pick(self, rules, is_new_round, option_type, last_played):
        return option_type, last_played
    
    def superbot_pick(self, rules, is_new_round, option_type, last_played):
        return option_type, last_played

class Game:
    def __init__(self, age, player, bot1, bot2, superbot):
        self.age = age
        self.player = player
        self.bot1 = bot1
        self.bot2 = bot2
        self.superbot = superbot
        
    def get_settings(self, message):
        if not message:
            ansr = input("Yay! Would you like to play standard or custom rules? (standard/custom)\n")
        else:
            ansr = input(message)
        while ansr not in ['standard', 'custom']:
            ansr = input("Please try again. (standard/custom)\n")
        if ansr == 'standard':
            rules = ['y', 'n', 'n', 'y']
            print("Here are your selected rules:")
            Game.display_settings(rules)
        else:
            a = input("Please select your rules.\nTwo Pair Run: (y/n)\n")
            while a not in ['y', 'n']:
                a = input("Please try again. (y/n)\n")
            b = input("Three-of-a-kind Bomb: (y/n)\n")
            while b not in ['y', 'n']:
                b = input("Please try again. (y/n)\n")
            c = input("Three Single Run: (y/n)\n")
            while c not in ['y', 'n']:
                c = input("Please try again. (y/n)\n")
            d = input("Joker Bomb: (y/n)\n")
            while d not in ['y', 'n']:
                d = input("Please try again. (y/n)\n")
            rules = [a, b, c, d]
            print("Here are your selected rules:")
            Game.display_settings(rules)
        confirmation = input("Does that sound alright? (y/n)\n")
        while confirmation not in ['y', 'n']:
            confirmation = input("Please try again. (y/n)\n")
        if confirmation == 'n':
            Game.get_settings(self, "Alright, would you like to play standard or custom rules? (standard/custom)\n")
        self.settings = rules
        
    def order(self):
        #circular linked list (clockwise: player -> bot1 -> bot2 -> superbot -> player -> ...)
        first = Node(self.player)
        second = Node(self.bot1)
        third = Node(self.bot2)
        last = Node(self.superbot)
        first.next = second
        second.next = third
        third.next = last
        last.next = first
        if self.age == 1: #if new game
            if first.data.hand[0] == 1:
                curr_player = first
            elif second.data.hand[0] == 1:
                curr_player = second
            elif third.data.hand[0] == 1:
                curr_player = third
            else:
                curr_player = last
        else: #find winner and base order off that
            if first.data.is_past_winner == True:
                curr_player = first
            elif second.data.is_past_winner == True:
                curr_player = second
            elif third.data.is_past_winner == True:
                curr_player = third
            else:
                curr_player = last
        self.curr_player = curr_player

    def display_settings(rules):
        if rules[0] == 'y':
            print("Two Pair Run")
        else:
            print("Three Pair Run")
        if rules[1] == 'y':
            print("Three-of-a-kind Bomb")
        else:
            print("Four-of-a-kind Bomb")
        if rules[2] == 'y':
            print("Three Single Run")
        else:
            print("Five Single Run")
        if rules[3] == 'y':
            print("Joker Bomb")
        else:
            print("No Joker Bomb")
    
    def play_phase(self):
        print("The round has started.")
        winner = False
        is_new_round = True
        pass_count = 0
        option_type = ''
        last_played = -1
        while not winner:
            if self.curr_player.data == self.player: #let player play
                option_type, last_played = self.curr_player.data.pick_option(self.settings, is_new_round, option_type, last_played)
            elif self.curr_player.data == self.bot1: #bot1 algorithm
                option_type, last_played = self.curr_player.data.bot1_pick(self.settings, is_new_round, option_type, last_played)
            elif self.curr_player.data == self.bot2: #bot2 algorithm
                option_type, last_played = self.curr_player.data.bot2_pick(self.settings, is_new_round, option_type, last_played)
            else: #superbot play algorithm
                option_type, last_played = self.curr_player.data.superbot_pick(self.settings, is_new_round, option_type, last_played)
            if option_type == 'pass': #count passes in a row
                pass_count += 1
            else:
                pass_count = 0
            if pass_count == 3: #if everyone else passed
                print("Everyone passed!")
                is_new_round = True
                pass_count = 0
            else:
                is_new_round = False
            if self.curr_player.data.hand == [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]: #if someone has no cards left in hand
                winner = True
                self.curr_player.next.data.is_past_winner = False
                self.curr_player.next.data.score += sum(self.curr_player.next.data.hand)
                self.curr_player.next.next.data.is_past_winner = False
                self.curr_player.next.next.data.score += sum(self.curr_player.next.next.data.hand)
                self.curr_player.next.next.next.data.is_past_winner = False
                self.curr_player.next.next.next.data.score += sum(self.curr_player.next.next.next.data.hand)
                self.curr_player.data.is_past_winner = True
                self.age += 1
                if self.curr_player.data == self.player:
                    print("Congradulations! You have won this round.")
                else:
                    print("Oh no! You have lost.")
                    if self.curr_player.data == self.bot1:
                        bot = "Bot 1"
                    elif self.curr_player.data == self.bot2:
                        bot = "Bot 2"
                    else:
                        bot = "Superbot"
                    print(bot + " has won this round.")
                print("Here are the cards left in each hand from this round:")
                print("You: " + sum(self.player.hand) + " cards")
                print("Bot 1: " + sum(self.bot1.hand) + " cards")
                print("Bot 2: " + sum(self.bot2.hand) + " cards")
                print("Superbot: " + sum(self.superbot.hand) + " cards")
                Game.display_scoreboard()
            if not winner:
                self.curr_player = self.curr_player.next
        Game.order()
        Game.end()
        
    def end(self):
        confirmation = 'n'
        while confirmation == 'n':
            ansr = input("Would you like to reset the game, play the next round, or end the game? (reset/next/end)\n")
            while ansr not in ['next', 'end', 'reset']:
                ansr = input("Please try again. (reset/next/end)\n")
            confirmation = input("You have selected {ansr}. Please confirm. (y/n)\n")
            while confirmation not in ['y', 'n']:
                confirmation = input("Please try again. (y/n)\n")
        if ansr == 'reset':
            start()
        elif ansr == 'next':
            Game.deal()
            Game.play_phase()
        else:
            print("Thank you for playing!")
            exit()
        
    def display_scoreboard(self):
        print("Here is the overall scoreboard:")
        print("Player's Score: {self.player.score}")
        print("Bot 1's Score: {self.bot1.score}")
        print("Bot 2's Score: {self.bot2.score}")
        print("Superbot's Score: {self.superbot.score}")
    
    def deal(self): #each hand list's index represents cards from 3-of-hearts,3,4,5,6,7,8,9,10,J,Q,K,A,2,BJoker,RJoker
        deck = [1, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1]
        indices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        while indices:
            rand = random.randint(0, len(indices)-1)
            self.curr_player.data.hand[indices[rand]] += 1
            deck[indices[rand]] -= 1
            if deck[indices[rand]] == 0:
                indices.remove(indices[rand])
            self.curr_player = self.curr_player.next
        assert(deck == [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

def start():
    player = Player([0]*16, False, 0)
    bot1 = Player([0]*16, False, 0)
    bot2 = Player([0]*16, False, 0)
    superbot = Player([0]*16, False, 0)
    game = Game(1, player, bot1, bot2, superbot)
    
    #circular linked list (clockwise: player -> bot1 -> bot2 -> superbot -> player -> ...)
    first = Node(player)
    second = Node(bot1)
    third = Node(bot2)
    last = Node(superbot)
    first.next = second
    second.next = third
    third.next = last
    last.next = first
    game.curr_player = first
    game.deal()
    game.get_settings('')
    game.order()
    game.play_phase()