import random
import copy
import time

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
    
    def show_hand(self):
        hand = ''
        for idx in range(16):
            for count in range(self.hand[idx]):
                hand += self.card_dict[idx] + ', '
        return hand[:-2]
    
    def update_options(self, rules, is_new_round, play_type, last_played_card, last_played_count):
        for key in self.playable_moves.keys():
            self.playable_moves[key] = False
        if is_new_round:
            self.playable_moves['single'] = True
            if rules[2] == 'y': #min three singles in a row for a run
                threshold = 3
            else:
                threshold = 5
            in_a_row = 0
            for num in range(1,13):
                if self.hand[num] != 0:
                    in_a_row += 1
                else:
                    in_a_row = 0
                if in_a_row == threshold:
                    self.playable_moves['single run'] = True
                    break
            for count in self.hand:
                if count >= 2:
                    self.playable_moves['pair'] = True
                    break
            if rules[3] == 'n' and self.hand[14] == 1 and self.hand[15] == 1:
                self.playable_moves['pair'] = True
            if rules[0] == 'y': #min two pair for a run
                threshold = 2
            else:
                threshold = 3
            in_a_row = 0
            for num in range(1,13):
                if self.hand[num] >= 2:
                    in_a_row += 1
                else:
                    in_a_row = 0
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
                        temp = 0
                        for num in self.hand:
                            if num >= 2:
                                temp += 1
                        if temp >= 2:
                            self.playable_moves['triple pair-carry'] = True
            if rules[3] == 'y': #yes to joker bomb
                if self.hand[14] == 1 and self.hand[15] == 1:
                    self.playable_moves['joker bomb'] = True
            for count in self.hand:
                if count == 4:
                    self.playable_moves['quad bomb'] = True
        else:
            if play_type == 'single':
                for card, count in enumerate(self.hand):
                    if count != 0 and card > last_played_card:
                        self.playable_moves[play_type] = True
            elif play_type == 'single run':
                in_a_row = 0
                for num in range(1,13):
                    if self.hand[num] != 0:
                        in_a_row += 1
                    else:
                        in_a_row = 0
                    if in_a_row >= last_played_count and (num-last_played_count+1) > last_played_card:
                        self.playable_moves[play_type] = True
            elif play_type == 'pair':
                for card, count in enumerate(self.hand):
                    if (count >= 2 and card > last_played_card) or (rules[3] == 'n' and self.hand[14] == 1 and self.hand[15] == 1): #no joker bomb edge case
                        self.playable_moves[play_type] = True
            elif play_type == 'pair run':
                in_a_row = 0
                for num in range(1,13):
                    if self.hand[num] >= 2:
                        in_a_row += 1
                    else:
                        in_a_row = 0
                    if in_a_row >= last_played_count and (num-last_played_count+1) > last_played_card:
                        self.playable_moves[play_type] = True
            elif play_type == 'triple no-carry':
                if rules[1] == 'n':
                    for card, count in enumerate(self.hand):
                        if count >= 3 and card > last_played_card:
                            self.playable_moves[play_type] = True
            elif play_type == 'triple single-carry':
                if rules[1] == 'n':
                    for card, count in enumerate(self.hand):
                        if count >= 3:
                            if sum(self.hand) >= 4 and card > last_played_card:
                                self.playable_moves[play_type] = True
            elif play_type == 'triple pair-carry':
                if rules[1] == 'n':
                    temp = 0
                    for count in self.hand:
                        if count >= 2:
                            temp += 1
                    if temp >= 2:
                        for card, count in enumerate(self.hand):
                            if count >= 3 and card > last_played_card:
                                self.playable_moves[play_type] = True
            if rules[1] == 'y' and play_type != 'quad bomb' and play_type != 'joker bomb':
                for card, count in enumerate(self.hand):
                    if count >= 3:
                        if play_type != 'triple bomb':
                            self.playable_moves['triple bomb'] = True
                        else:
                            if card > last_played_card:
                                self.playable_moves[play_type] = True
            if play_type != 'joker bomb':
                for card, count in enumerate(self.hand):
                    if count == 4:
                        if play_type != 'quad bomb':
                            self.playable_moves['quad bomb'] = True
                        else:
                            if card > last_played_card:
                                self.playable_moves[play_type] = True
            if rules[3] == 'y' and self.hand[14] == 1 and self.hand[15] == 1: #joker bomb
                self.playable_moves['joker bomb'] = True
        return [moves for moves, is_allowed in self.playable_moves.items() if is_allowed]
    
    def pick_possible_start_cards(self, rules, is_new_round, play_type, last_played_card, last_played_count):
        length = -1
        ansr = ''
        options = []
        if play_type == 'single':
            for card, count in enumerate(self.hand):
                if count != 0 and card > last_played_card:
                    options.append([card])
        elif play_type == 'single run':
            lengths = []
            if is_new_round:
                if rules[2] == 'y':
                    threshold = 3
                else:
                    threshold = 5
                in_a_row = 0
                for num in range(1,13):
                    if self.hand[num] != 0:
                        in_a_row += 1
                    else:
                        in_a_row = 0
                    if in_a_row >= threshold and str(in_a_row) not in lengths:
                        lengths.append(str(in_a_row))
                if len(lengths) > 1:
                    msg = '(' + lengths[0]
                    for num in lengths[1:]:
                        msg += '/' + num
                    msg += ') --> '
                    length = input("What length of single run do you want to play? " + msg)
                    while length not in lengths:
                        length = input("Please try again. " + msg)
                else:
                    length = lengths[0]
            else:
                length = last_played_count
            length = int(length)
            for card in range(length, 13):
                in_a_row = 0
                for prev_card in range(length-1,-1,-1):
                    if self.hand[card-prev_card] != 0:
                        in_a_row += 1
                    else:
                        in_a_row = 0
                if in_a_row == length and card-length+1 > last_played_card:
                    options.append([num for num in range(card-length+1, card+1)])
        elif play_type == 'pair':
            for card, count in enumerate(self.hand):
                if count >= 2 and card > last_played_card:
                    options.append([card, card])
            if rules[3] == 'n' and self.hand[14] == 1 and self.hand[15] == 1:
                options.append([self.hand[14], self.hand[15]])
        elif play_type == 'pair run':
            lengths = []
            if is_new_round:
                if rules[0] == 'y':
                    threshold = 2
                else:
                    threshold = 3
                in_a_row = 0
                for num in range(1,13):
                    if self.hand[num] >= 2:
                        in_a_row += 1
                    else:
                        in_a_row = 0
                    if in_a_row >= threshold and str(in_a_row) not in lengths:
                        lengths.append(str(in_a_row))
                if len(lengths) > 1:
                    msg = '(' + lengths[0]
                    for num in lengths[1:]:
                        msg += '/' + num
                    msg += ') --> '
                    length = input("What length of pair run do you want to play? " + msg)
                    while length not in lengths:
                        length = input("Please try again. " + msg)
                else:
                    length = lengths[0]
            else:
                length = last_played_count
            length = int(length)
            for card in range(length, 13):
                in_a_row = 0
                for prev_card in range(length-1,-1,-1):
                    if self.hand[card-prev_card] >= 2:
                        in_a_row += 1
                    else:
                        in_a_row = 0
                if in_a_row == length and card-length+1 > last_played_card:
                    temp = []
                    for num in range(card-length+1, card+1):
                        temp.append(num)
                        temp.append(num)
                    options.append(temp)
        elif play_type == 'triple no-carry' or play_type == 'triple single-carry' or play_type == 'triple pair-carry' or play_type == 'triple bomb':
            for card, count in enumerate(self.hand):
                if count >= 3 and card > last_played_card:
                    options.append([card, card, card])
        elif play_type == 'quad bomb':
            for card, count in enumerate(self.hand):
                if count == 4 and card > last_played_card:
                    options.append([card])
        elif play_type == 'joker bomb':
            options.append([14, 15])
        orig_hand = copy.deepcopy(self.hand)
        if len(options) > 1:
            choices = [str(num+1) for num in range(len(options))]
            msg = '\n'
            count = 1
            for option in options:
                cards = ''
                for card in option:
                    cards += self.card_dict[card] + ', '
                msg += str(count) + ') ' + cards[:-2] + '\n'
                count += 1
            choices_msg = '('
            for choice in choices:
                choices_msg += choice + '/'
            choices_msg = choices_msg[:-1] + ') --> '
            msg += choices_msg
            ansr = ''
            ansr = input("Out of these options for your " + play_type + ", which would you like?" + msg)
            while ansr not in choices:
                ansr = input("Please try again. " + choices_msg)
            option = options[int(ansr)-1]
        else:
            option = options[0]
        for card in option:
            self.hand[card] -= 1
        if play_type == 'triple single-carry' or play_type == 'triple pair-carry':
            if play_type == 'triple single-carry':
                carry_options = [[card] for card, count in enumerate(self.hand) if count != 0 and card > last_played_card]
                pairing = 'single'
            elif play_type == 'triple pair-carry':
                carry_options = [[card, card] for card, count in enumerate(self.hand) if count >= 2 and card > last_played_card]
                pairing = 'pair'
            if len(carry_options) > 1:
                choices = [str(num+1) for num in range(len(carry_options))]
                msg = '\n'
                count = 1
                for carry_option in carry_options:
                    cards = ''
                    for card in carry_option:
                        cards += self.card_dict[card] + ', '
                    msg += str(count) + ') ' + cards[:-2] + '\n'
                    count += 1
                choices_msg = '('
                for choice in choices:
                    choices_msg += choice + '/'
                choices_msg = choices_msg[:-1] + ') --> '
                msg += choices_msg
                ansr = input("Out of these options for the " + pairing + " for the triple to carry, which would you like?" + msg)
                while ansr not in choices:
                    ansr = input("Please try again. " + choices_msg)
                carry_option = carry_options[int(ansr)-1]
            else:
                carry_option = carry_options[0]
            for card in carry_option:
                self.hand[card] -= 1
                option.append(card)
        play = ''
        for card in option:
            play += self.card_dict[card] + ', '
        print("Selection: " + play[:-2])
        if sum(self.hand) != 0:
            print("Hand after selection: " + Player.show_hand(self))
            if len(options) > 1:
                confirmation = input('Confirm if this is the wanted play. (y/n) --> ')
                while confirmation not in ['y', 'n']:
                    confirmation = input('Please try again. (y/n) --> ')
                if confirmation == 'n':
                    print("Okay, what would you like to do instead?")
                    self.hand = copy.deepcopy(orig_hand)
                    return Player.pick_possible_start_cards(self, rules, is_new_round, play_type, last_played_card, last_played_count)
            else:
                last_played_card = option[0]
                last_played_count = len(option)
        if len(option) > 1:
            print("\nYou played " + play[:-2] + ".")
        else:
            print("\nYou played a " + play[:-2] + ".")
        print('')
        return last_played_card, last_played_count
    
    def pick_option(self, rules, is_new_round, option_type, last_played_card, last_played_count):
        print("It's your turn! Here is your hand: " + Player.show_hand(self))
        play_types = Player.update_options(self, rules, is_new_round, option_type, last_played_card, last_played_count)
        options = '('
        for option in play_types:
            options += option + ', '
        options = options[:-2] + ')'
        if is_new_round:
            if len(play_types) > 1:
                msg = 'Out of these options, which would you like to play? '
                play_type = input(msg + options + ' --> ')
                while play_type not in play_types:
                    play_type = input("Please try again. " + options + ' --> ')
            else:
                play_type = play_types[0]
                print("You can only play a " + play_type + "!")
            print('\n')
        else: #confirm if player can play or not
            if play_types:
                play_type = input("Would you like to play or pass? (play/pass) --> ")
                while play_type not in ['play', 'pass']:
                    play_type = input("Please try again. (play/pass) --> ")
                if play_type == 'pass':
                    print("\nYou passed.\n")
                elif len(play_types) > 1:
                    play_type = input("Alright! Which of these options would you like to play? " + options + ' --> ')
                    while play_type not in play_types:
                        play_type = input("Please try again. " + options + ' --> ')
                    print('')
                else:
                    play_type = play_types[0]
                    if play_type == option_type:
                        print("\nYou can only match type and play a " + play_type + "!")
                    else:
                        print("\nYou have chosen to play a " + play_type + ".")
            else:
                print("No playable moves! Auto-passing.\n")
                play_type = 'pass'
        if play_type != 'pass':
            if (option_type != 'triple bomb' and play_type == 'triple bomb') or (option_type != 'quad bomb' and play_type == 'quad bomb'):
                last_played_card = -1
            last_played_card, last_played_count = Player.pick_possible_start_cards(self, rules, is_new_round, play_type, last_played_card, last_played_count)
            return play_type, play_type, last_played_card, last_played_count
        else:
            return 'pass', option_type, last_played_card, last_played_count
    
    def bot1_pick(self, rules, is_new_round, option_type, last_played_card, last_played_count): #play random type but force lowest run and pick highest
        play_types = Player.update_options(self, rules, is_new_round, option_type, last_played_card, last_played_count)
        if not is_new_round:
            play_types.append('pass')
        if play_types[0] == 'pass':
            print("Bot 1 passed.\n")
            return 'pass', option_type, last_played_card, last_played_count
        if len(play_types) > 1:
            rand = random.randint(0, len(play_types)-1)
        else:
            rand = 0
        play_type = play_types[rand]
        if play_type == 'pass':
            print("Bot 1 passed.\n")
            return 'pass', option_type, last_played_card, last_played_count
        options = []
        if play_type == 'single':
            options = [[card] for card, count in enumerate(self.hand) if count != 0 and card > last_played_card]
        elif play_type == 'single run':
            if is_new_round:
                if rules[2] == 'y':
                    threshold = 3
                else:
                    threshold = 5
                length = threshold
            else:
                length = last_played_count
            for card in range(length, 13):
                in_a_row = 0
                for prev_card in range(length-1,-1,-1):
                    if self.hand[card-prev_card] != 0:
                        in_a_row += 1
                    else:
                        in_a_row = 0
                if in_a_row == length and card-length+1 > last_played_card:
                    options.append([num for num in range(card-length+1, card+1)])
        elif play_type == 'pair':
            options = [[card, card] for card, count in enumerate(self.hand) if count >= 2 and card > last_played_card]
            if rules[3] == 'n' and self.hand[14] == 1 and self.hand[15] == 1:
                options.append([self.hand[14], self.hand[15]])
        elif play_type == 'pair run':
            if is_new_round:
                if rules[0] == 'y':
                    threshold = 2
                else:
                    threshold = 3
                length = threshold
            else:
                length = last_played_count
            for card in range(length, 13):
                in_a_row = 0
                for prev_card in range(length-1,-1,-1):
                    if self.hand[card-prev_card] >= 2:
                        in_a_row += 1
                    else:
                        in_a_row = 0
                if in_a_row == length and card-length+1 > last_played_card:
                    temp = []
                    for num in range(card-length+1, card+1):
                        temp.append(num)
                        temp.append(num)
                    options.append(temp)
        elif play_type == 'triple no-carry' or play_type == 'triple single-carry' or play_type == 'triple pair-carry':
            options = [[card, card, card] for card, count in enumerate(self.hand) if count >= 3 and card > last_played_card]
        elif play_type == 'triple bomb':
            if option_type != 'triple bomb':
                options = [[card, card, card] for card, count in enumerate(self.hand) if count >= 3]
            else:
                options = [[card, card, card] for card, count in enumerate(self.hand) if count >= 3 and card > last_played_card]
        elif play_type == 'quad bomb':
            if option_type != 'quad bomb':
                options = [[card, card, card, card] for card, count in enumerate(self.hand) if count == 4]
            else:
                options = [[card, card, card, card] for card, count in enumerate(self.hand) if count == 4 and card > last_played_card]
        elif play_type == 'joker bomb':
            options = [[14, 15]]
        option = options[-1]
        for card in option:
            self.hand[card] -= 1
        if play_type == 'triple single-carry' or play_type == 'triple pair-carry':
            if play_type == 'triple single-carry':
                carry_options = [[card] for card, count in enumerate(self.hand) if count != 0 and card > last_played_card]
            elif play_type == 'triple pair-carry':
                carry_options = [[card, card] for card, count in enumerate(self.hand) if count >= 2 and card > last_played_card]
            carry_option = carry_options[-1]
            for card in carry_option:
                self.hand[card] -= 1
                option.append(card)
        hand = ''
        for card in option:
            hand += self.card_dict[card] + ', '
        if len(option) > 1:
            print("Bot 1 played " + hand[:-2] + ".")
        else:
            print("Bot 1 played a " + hand[:-2] + ".")
        if sum(self.hand) == 1:
            print("Warning: Bot 1 only has 1 card remaining!")
        print('')
        return play_type, play_type, option[0], len(option)
    
    def bot2_pick(self, rules, is_new_round, option_type, last_played_card, last_played_count): #play random type, length, and selection
        play_types = Player.update_options(self, rules, is_new_round, option_type, last_played_card, last_played_count)
        if not is_new_round:
            play_types.append('pass')
        if play_types[0] == 'pass':
            print("Bot 2 passed.\n")
            return 'pass', option_type, last_played_card, last_played_count
        if len(play_types) > 1:
            rand = random.randint(0, len(play_types)-1)
        else:
            rand = 0
        play_type = play_types[rand]
        if play_type == 'pass':
            print("Bot 2 passed.\n")
            return 'pass', option_type, last_played_card, last_played_count
        options = []
        if play_type == 'single':
            options = [[card] for card, count in enumerate(self.hand) if count != 0 and card > last_played_card]
        elif play_type == 'single run':
            lengths = []
            if is_new_round:
                if rules[2] == 'y':
                    threshold = 3
                else:
                    threshold = 5
                in_a_row = 0
                for num in range(1,13):
                    if self.hand[num] != 0:
                        in_a_row += 1
                    else:
                        in_a_row = 0
                    if in_a_row >= threshold and in_a_row not in lengths:
                        lengths.append(in_a_row)
                rand = random.randint(0, len(lengths)-1)
                length = lengths[rand]
            else:
                length = last_played_count
            for card in range(length, 13):
                in_a_row = 0
                for prev_card in range(length-1,-1,-1):
                    if self.hand[card-prev_card] != 0:
                        in_a_row += 1
                    else:
                        in_a_row = 0
                if in_a_row == length and card-length+1 > last_played_card:
                    options.append([num for num in range(card-length+1, card+1)])
        elif play_type == 'pair':
            options = [[card, card] for card, count in enumerate(self.hand) if count >= 2 and card > last_played_card]
            if rules[3] == 'n' and self.hand[14] == 1 and self.hand[15] == 1:
                options.append([self.hand[14], self.hand[15]])
        elif play_type == 'pair run':
            lengths = []
            if is_new_round:
                if rules[0] == 'y':
                    threshold = 2
                else:
                    threshold = 3
                in_a_row = 0
                for num in range(1,13):
                    if self.hand[num] != 0:
                        in_a_row += 1
                    else:
                        in_a_row = 0
                    if in_a_row >= threshold and in_a_row not in lengths:
                        lengths.append(in_a_row)
                rand = random.randint(0, len(lengths)-1)
                length = lengths[rand]
            else:
                length = last_played_count
            for card in range(length, 13):
                in_a_row = 0
                for prev_card in range(length-1,-1,-1):
                    if self.hand[card-prev_card] >= 2:
                        in_a_row += 1
                    else:
                        in_a_row = 0
                if in_a_row == length and card-length+1 > last_played_card:
                    temp = []
                    for num in range(card-length+1, card+1):
                        temp.append(num)
                        temp.append(num)
                    options.append(temp)
        elif play_type == 'triple no-carry' or play_type == 'triple single-carry' or play_type == 'triple pair-carry':
            options = [[card, card, card] for card, count in enumerate(self.hand) if count >= 3 and card > last_played_card]
        elif play_type == 'triple bomb':
            if option_type != 'triple bomb':
                options = [[card, card, card] for card, count in enumerate(self.hand) if count >= 3]
            else:
                options = [[card, card, card] for card, count in enumerate(self.hand) if count >= 3 and card > last_played_card]
        elif play_type == 'quad bomb':
            if option_type != 'quad bomb':
                options = [[card, card, card, card] for card, count in enumerate(self.hand) if count == 4]
            else:
                options = [[card, card, card, card] for card, count in enumerate(self.hand) if count == 4 and card > last_played_card]
        elif play_type == 'joker bomb':
            options = [[14, 15]]
        if len(options) > 1:
            rand = random.randint(0, len(options)-1)
        else:
            rand = 0
        option = options[rand]
        for card in option:
            self.hand[card] -= 1
        if play_type == 'triple single-carry' or play_type == 'triple pair-carry':
            if play_type == 'triple single-carry':
                carry_options = [[card] for card, count in enumerate(self.hand) if count != 0 and card > last_played_card]
            elif play_type == 'triple pair-carry':
                carry_options = [[card, card] for card, count in enumerate(self.hand) if count >= 2 and card > last_played_card]
            if len(carry_options) > 1:
                rand = random.randint(0, len(carry_options)-1)
            else:
                rand = 0
            carry_option = carry_options[rand]
            for card in carry_option:
                self.hand[card] -= 1
                option.append(card)
        hand = ''
        for card in option:
            hand += self.card_dict[card] + ', '
        if len(option) > 1:
            print("Bot 2 played " + hand[:-2] + ".")
        else:
            print("Bot 2 played a " + hand[:-2] + ".")
        if sum(self.hand) == 1:
            print("Warning: Bot 2 only has 1 card remaining!")
        print('')
        return play_type, play_type, option[0], len(option)
    
    def superbot_pick(self, rules, is_new_round, option_type, last_played_card, last_played_count): #CURR: play random type, pick longest length, select lowest possible   FUTURE: don't allow to break bombs and play them after a certain number of rounds
        play_types = Player.update_options(self, rules, is_new_round, option_type, last_played_card, last_played_count)
        if not is_new_round:
            play_types.append('pass')
        if play_types[0] == 'pass':
            print("Superbot passed.\n")
            return 'pass', option_type, last_played_card, last_played_count
        if len(play_types) > 1:
            rand = random.randint(0, len(play_types)-1)
        else:
            rand = 0
        play_type = play_types[rand]
        if play_type == 'pass':
            print("Superbot passed.\n")
            return 'pass', option_type, last_played_card, last_played_count
        options = []
        if play_type == 'single':
            options = [[card] for card, count in enumerate(self.hand) if count != 0 and card > last_played_card]
        elif play_type == 'single run':
            lengths = []
            if is_new_round:
                if rules[2] == 'y':
                    threshold = 3
                else:
                    threshold = 5
                in_a_row = 0
                for num in range(1,13):
                    if self.hand[num] != 0:
                        in_a_row += 1
                    else:
                        in_a_row = 0
                    if in_a_row >= threshold and in_a_row not in lengths:
                        lengths.append(in_a_row)
                length = lengths[-1]
            else:
                length = last_played_count
            for card in range(length, 13):
                in_a_row = 0
                for prev_card in range(length-1,-1,-1):
                    if self.hand[card-prev_card] != 0:
                        in_a_row += 1
                    else:
                        in_a_row = 0
                if in_a_row == length and card-length+1 > last_played_card:
                    options.append([num for num in range(card-length+1, card+1)])
        elif play_type == 'pair':
            options = [[card, card] for card, count in enumerate(self.hand) if count >= 2 and card > last_played_card]
            if rules[3] == 'n' and self.hand[14] == 1 and self.hand[15] == 1:
                options.append([self.hand[14], self.hand[15]])
        elif play_type == 'pair run':
            lengths = []
            if is_new_round:
                if rules[0] == 'y':
                    threshold = 2
                else:
                    threshold = 3
                in_a_row = 0
                for num in range(1,13):
                    if self.hand[num] != 0:
                        in_a_row += 1
                    else:
                        in_a_row = 0
                    if in_a_row >= threshold and in_a_row not in lengths:
                        lengths.append(in_a_row)
                length = lengths[-1]
            else:
                length = last_played_count
            for card in range(length, 13):
                in_a_row = 0
                for prev_card in range(length-1,-1,-1):
                    if self.hand[card-prev_card] >= 2:
                        in_a_row += 1
                    else:
                        in_a_row = 0
                if in_a_row == length and card-length+1 > last_played_card:
                    temp = []
                    for num in range(card-length+1, card+1):
                        temp.append(num)
                        temp.append(num)
                    options.append(temp)
        elif play_type == 'triple no-carry' or play_type == 'triple single-carry' or play_type == 'triple pair-carry':
            options = [[card, card, card] for card, count in enumerate(self.hand) if count >= 3 and card > last_played_card]
        elif play_type == 'triple bomb':
            if option_type != 'triple bomb':
                options = [[card, card, card] for card, count in enumerate(self.hand) if count >= 3]
            else:
                options = [[card, card, card] for card, count in enumerate(self.hand) if count >= 3 and card > last_played_card]
        elif play_type == 'quad bomb':
            if option_type != 'quad bomb':
                options = [[card, card, card, card] for card, count in enumerate(self.hand) if count == 4]
            else:
                options = [[card, card, card, card] for card, count in enumerate(self.hand) if count == 4 and card > last_played_card]
        elif play_type == 'joker bomb':
            options = [[14, 15]]
        option = options[0]
        for card in option:
            self.hand[card] -= 1
        if play_type == 'triple single-carry' or play_type == 'triple pair-carry':
            if play_type == 'triple single-carry':
                carry_options = [[card] for card, count in enumerate(self.hand) if count != 0 and card > last_played_card]
            elif play_type == 'triple pair-carry':
                carry_options = [[card, card] for card, count in enumerate(self.hand) if count >= 2 and card > last_played_card]
            carry_option = carry_options[0]
            for card in carry_option:
                self.hand[card] -= 1
                option.append(card)
        hand = ''
        for card in option:
            hand += self.card_dict[card] + ', '
        if len(option) > 1:
            print("Superbot played " + hand[:-2] + ".")
        else:
            print("Superbot played a " + hand[:-2] + ".")
        if sum(self.hand) == 1:
            print("Warning: Superbot only has 1 card remaining!")
        print('')
        return play_type, play_type, option[0], len(option)

class Game:
    def __init__(self, age, player, bot1, bot2, superbot):
        self.age = age
        self.player = player
        self.bot1 = bot1
        self.bot2 = bot2
        self.superbot = superbot
        
    def get_settings(self, message):
        if not message:
            ansr = input("Yay! Would you like to play standard or custom rules? (standard/custom) --> ")
        else:
            ansr = input(message)
        while ansr not in ['standard', 'custom']:
            ansr = input("Please try again. (standard/custom) --> ")
        if ansr == 'standard':
            rules = ['y', 'n', 'n', 'y']
            print("\nHere are your selected rules:")
            Game.display_settings(rules)
        else:
            a = input("\nPlease select your rules.\nTwo Pair Run: (y/n) --> ")
            while a not in ['y', 'n']:
                a = input("Please try again. (y/n) --> ")
            b = input("Three-of-a-kind Bomb: (y/n) --> ")
            while b not in ['y', 'n']:
                b = input("Please try again. (y/n) --> ")
            c = input("Three Single Run: (y/n) --> ")
            while c not in ['y', 'n']:
                c = input("Please try again. (y/n) --> ")
            d = input("Joker Bomb: (y/n) --> ")
            while d not in ['y', 'n']:
                d = input("Please try again. (y/n) --> ")
            rules = [a, b, c, d]
            print("\nHere are your selected rules:")
            Game.display_settings(rules)
        confirmation = input("\nDoes that sound alright? (y/n) --> ")
        while confirmation not in ['y', 'n']:
            confirmation = input("Please try again. (y/n) --> ")
        if confirmation == 'n':
            Game.get_settings(self, "Alright, would you like to play standard or custom rules? (standard/custom) --> ")
        self.settings = rules
        
    def order(self):
        if self.age == 1: #if new game
            if self.curr_player.next.data.hand[0] == 1:
                self.curr_player = self.curr_player.next
            elif self.curr_player.next.next.data.hand[0] == 1:
                self.curr_player = self.curr_player.next.next
            elif self.curr_player.next.next.next.data.hand[0] == 1:
                self.curr_player = self.curr_player.next.next.next
        else: #find winner and base order off that
            if self.curr_player.next.data.is_past_winner == True:
                self.curr_player = self.curr_player.next
            elif self.curr_player.next.next.data.is_past_winner == True:
                self.curr_player = self.curr_player.next.next
            elif self.curr_player.next.next.next.data.is_past_winner == True:
                self.curr_player = self.curr_player.next.next.next

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
        print("\n\n\n\n\nThe game has started.\n\n\n")
        for _ in range(4): #combine the three of hearts into the threes
            if self.curr_player.data.hand[0] == 1:
                self.curr_player.data.hand[1] += 1
                self.curr_player.data.hand[0] = 0
            self.curr_player = self.curr_player.next
        winner = False
        self.is_new_round = True
        pass_count = 0
        option_type = ''
        self.last_played_option_type = ''
        self.last_played_card = -1
        self.last_played_count = -1
        while not winner:
            if self.curr_player.data == self.player: #let player play
                option_type, self.last_played_option_type, self.last_played_card, self.last_played_count = self.curr_player.data.pick_option(self.settings, self.is_new_round, self.last_played_option_type, self.last_played_card, self.last_played_count)
            elif self.curr_player.data == self.bot1: #bot1 algorithm
                option_type, self.last_played_option_type, self.last_played_card, self.last_played_count = self.curr_player.data.bot1_pick(self.settings, self.is_new_round, self.last_played_option_type, self.last_played_card, self.last_played_count)
            elif self.curr_player.data == self.bot2: #bot2 algorithm
                option_type, self.last_played_option_type, self.last_played_card, self.last_played_count = self.curr_player.data.bot2_pick(self.settings, self.is_new_round, self.last_played_option_type, self.last_played_card, self.last_played_count)
            else: #superbot play algorithm
                option_type, self.last_played_option_type, self.last_played_card, self.last_played_count = self.curr_player.data.superbot_pick(self.settings, self.is_new_round, self.last_played_option_type, self.last_played_card, self.last_played_count)
            if option_type == 'pass': #count passes in a row
                pass_count += 1
            else:
                pass_count = 0
            if pass_count == 3: #if everyone else passed
                print("Everyone passed!")
                self.is_new_round = True
                pass_count = 0
                option_type = 'pass' #for faster time reset in the not winner if-statement below
                self.last_played_option_type = ''
                self.last_played_card = -1
                self.last_played_count = -1
                print("\n\n\nNEW ROUND\n\n\n")
            else:
                self.is_new_round = False
            for count in self.curr_player.data.hand:############################################################
                if count < 0:###################################################################################
                    print("ERROR: LAST PLAYER'S HAND HAS AT LEAST ONE NEGATIVE INDEX")##########################
                    exit()######################################################################################
            if sum(self.curr_player.data.hand) == 0: #if someone has no cards left in hand
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
                    print(bot + " has won this round.\n")
                print("Here are the number of cards left in each hand from this round:")
                print("You:      " + str(sum(self.player.hand)))
                print("Bot 1:    " + str(sum(self.bot1.hand)))
                print("Bot 2:    " + str(sum(self.bot2.hand)))
                print("Superbot: " + str(sum(self.superbot.hand)) + '\n')
                Game.display_scoreboard(self)
            if not winner:
                self.curr_player = self.curr_player.next
                if option_type != 'pass':
                    time.sleep(6)
                else:
                    time.sleep(3)
        Game.order(self)
        Game.end(self)
        
    def end(self):
        confirmation = 'n'
        while confirmation == 'n':
            ansr = input("Would you like to reset the game, play the next round, or end the game? (reset/next/end) --> ")
            while ansr not in ['next', 'end', 'reset']:
                ansr = input("Please try again. (reset/next/end) --> ")
            confirmation = input("You have selected '" + ansr + "'. Please confirm. (y/n) --> ")
            while confirmation not in ['y', 'n']:
                confirmation = input("Please try again. (y/n) --> ")
        if ansr == 'reset':
            start()
        elif ansr == 'next':
            self.player.hand = [0]*16
            self.bot1.hand = [0]*16
            self.bot2.hand = [0]*16
            self.superbot.hand = [0]*16
            Game.deal(self)
            Game.play_phase(self)
        else:
            print("Thank you for playing!")
            exit()
        
    def display_scoreboard(self):
        print("Here is the overall scoreboard:")
        print("Your Score:       " + str(self.player.score))
        print("Bot 1's Score:    " + str(self.bot1.score))
        print("Bot 2's Score:    " + str(self.bot2.score))
        print("Superbot's Score: " + str(self.superbot.score) + '\n')
    
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
        self.curr_player = self.curr_player.next.next #54 cards in deck so reset curr_player for starting player to play first

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