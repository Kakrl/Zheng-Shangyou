import random
import copy

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
    
    def update_options(self, rules, is_new_round, play_type, last_played_card, last_played_count):
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
            for key in self.playable_moves.keys():
                self.playable_moves[key] = False
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
            elif rules[1] == 'y' and play_type != 'quad bomb' and play_type != 'joker bomb':
                for card, count in enumerate(self.hand):
                    if play_type != 'triple bomb' and count >= 3:
                        self.playable_moves['triple bomb'] = True
                    if play_type == 'triple bomb' and card > last_played_card:
                        self.playable_moves[play_type] = True
            elif play_type != 'joker bomb':
                for card, count in enumerate(self.hand):
                    if play_type != 'quad bomb' and count == 4:
                        self.playable_moves['quad bomb'] = True
                    if play_type == 'quad bomb' and card > last_played_card:
                        self.playable_moves[play_type] = True
            if rules[3] == 'y' and self.hand[14] == 1 and self.hand[15] == 1: #joker bomb
                self.playable_moves['joker bomb'] = True
        return [moves for moves, is_allowed in self.playable_moves.items() if is_allowed]
    
    def pick_possible_start_cards(self, rules, is_new_round, play_type, last_played_card, last_played_count):
        length = -1
        ansr = ''
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
                if len(lengths) > 1:
                    msg = '(' + str(lengths[0])
                    for num in lengths[1:]:
                        msg += '/' + str(num)
                    msg += ')\n'
                    length = input("What length of single run would you like to play? " + msg)
                    while int(length) not in lengths:
                        length = input("Please try again. " + msg)
                    length = int(length)
                else:
                    length = lengths[0]
            else:
                length = last_played_count
            options = []
            for card in range(length, 13):
                in_a_row = 0
                for prev_card in range(length,-1,-1):
                    if self.hand[card-prev_card] != 0:
                        in_a_row += 1
                    else:
                        in_a_row = 0
                if in_a_row == length:
                    options.append([num for num in range(card-length, card)])
        elif play_type == 'pair':
            options = [[card, card] for card, count in enumerate(self.hand) if count >= 2 and card > last_played_card]
        elif play_type == 'pair run':
            lengths = []
            if is_new_round:
                if rules[0] == 'y':
                    threshold = 2
                else:
                    threshold = 3
                in_a_row = 1
                for num in range(1,13):
                    if self.hand[num] >= 2:
                        in_a_row += 1
                    else:
                        in_a_row = 1
                    if in_a_row >= threshold and in_a_row not in lengths:
                        lengths.append(in_a_row)
                if len(lengths) > 1:
                    msg = '(' + str(lengths[0])
                    for num in lengths[1:]:
                        msg += '/' + str(num)
                    msg += ')\n'
                    length = input("What length of pair run would you like to play? " + msg)
                    while length not in lengths:
                        length = input("Please try again. " + msg)
                else:
                    length = lengths[0]
            else:
                length = last_played_count
            options = []
            for card in range(length, 13):
                in_a_row = 1
                for prev_card in range(length,-1,-1):
                    if self.hand[card-prev_card] != 0:
                        in_a_row += 1
                    else:
                        in_a_row = 1
                if in_a_row == length:
                    temp = []
                    for num in range(card-length, card):
                        temp.append(num)
                        temp.append(num)
                    options.append(temp)
        elif play_type == 'triple no-carry' or play_type == 'triple single-carry' or play_type == 'triple pair-carry' or play_type == 'triple bomb':
            options = [[card, card, card] for card, count in enumerate(self.hand) if count >= 3 and card > last_played_card]
        elif play_type == 'quad bomb':
            options = [[card, card, card, card] for card, count in enumerate(self.hand) if count == 4 and card > last_played_card]
        elif play_type == 'joker bomb':
            options = [[14, 15]]
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
            choices_msg = choices_msg[:-1] + ')\n'
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
                carry_options = [[card] for card, count in enumerate(self.hand) if count >= 2 and card > last_played_card]
                pairing = 'pair'
            if len(options) > 1:
                choices = [str(num+1) for num in range(len(options))]
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
                choices_msg = choices_msg[:-1] + ')\n'
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
        print("Here is what you have selected:")
        hand = ''
        for card in option:
            hand += self.card_dict[card] + ', '
        print(hand[:-2] + '\n')
        print("Here is your hand if you were to play your selection:")
        Player.display_hand(self)
        confirmation = input('Confirm if this is the wanted play. (y/n)\n')
        while confirmation not in ['y', 'n']:
            confirmation = input('Please try again. (y/n)\n')
        if confirmation == 'n':
            print("Okay, what would you like to do instead?")
            self.hand = copy.deepcopy(orig_hand)
            last_played_card, last_played_count = Player.pick_possible_start_cards(self, rules, is_new_round, play_type, last_played_card, last_played_count)
            return last_played_card, last_played_count
        return option[0], len(option)
    
    def pick_option(self, rules, is_new_round, option_type, last_played_card, last_played_count):
        print("It's your turn! Here is your hand:")
        Player.display_hand(self)
        play_types = Player.update_options(self, rules, is_new_round, option_type, last_played_card, last_played_count)
        print(play_types)
        options = '('
        for option in play_types:
            options += option + ', '
        options = options[:-2] + ')\n'
        if is_new_round:
            msg = 'Out of these options, which would you like to play? '
            play_type = input(msg + options)
            while play_type not in play_types:
                play_type = input("Please try again. " + options)
        else: #confirm if player can play or not
            if play_types:
                play_type = input("Would you like to play or pass? (play/pass)\n")
                while play_type not in ['play', 'pass']:
                    play_type = input("Please try again. (play/pass)\n")
                if play_type == 'pass':
                    print("You passed.")
                else:
                    play_type = input("Alright! Which of these options would you like to play? " + options)
                    while play_type not in play_types:
                        play_type = input("Please try again. " + options)
            else:
                print("No playable moves! Auto-passing.")
                play_type = 'pass'
        if play_type != 'pass':
            last_played_card, last_played_count = Player.pick_possible_start_cards(self, rules, is_new_round, play_type, last_played_card, last_played_count)
        else:
            play_type = option_type
        return play_type, last_played_card, last_played_count
    
    def bot1_pick(self, rules, is_new_round, option_type, last_played_card, last_played_count): #play random type but force lowest run and pick highest
        play_types = Player.update_options(self, rules, is_new_round, option_type, last_played_card, last_played_count)
        if len(play_types) > 1:
            rand = random.randint(0, len(play_types)-1)
        else:
            rand = 0
        play_type = play_types[rand]
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
            options = []
            for card in range(length, 13):
                in_a_row = 0
                for prev_card in range(length,-1,-1):
                    if self.hand[card-prev_card] != 0:
                        in_a_row += 1
                    else:
                        in_a_row = 0
                if in_a_row == length:
                    options.append([num for num in range(card-length, card)])
        elif play_type == 'pair':
            options = [[card, card] for card, count in enumerate(self.hand) if count >= 2 and card > last_played_card]
        elif play_type == 'pair run':
            if is_new_round:
                if rules[0] == 'y':
                    threshold = 2
                else:
                    threshold = 3
                length = threshold
            else:
                length = last_played_count
            options = []
            for card in range(length, 13):
                in_a_row = 1
                for prev_card in range(length,-1,-1):
                    if self.hand[card-prev_card] != 0:
                        in_a_row += 1
                    else:
                        in_a_row = 1
                if in_a_row == length:
                    temp = []
                    for num in range(card-length, card):
                        temp.append(num)
                        temp.append(num)
                    options.append(temp)
        elif play_type == 'triple no-carry' or play_type == 'triple single-carry' or play_type == 'triple pair-carry' or play_type == 'triple bomb':
            options = [[card, card, card] for card, count in enumerate(self.hand) if count >= 3 and card > last_played_card]
        elif play_type == 'quad bomb':
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
                carry_options = [[card] for card, count in enumerate(self.hand) if count >= 2 and card > last_played_card]
            carry_option = carry_options[-1]
            for card in carry_option:
                self.hand[card] -= 1
                option.append(card)
        print("It's Bot 1's turn. Here is what it played:")
        hand = ''
        for card in option:
            hand += self.card_dict[card] + ', '
        print(hand[:-2] + '\n')
        return play_type, option[0], len(option)
    
    def bot2_pick(self, rules, is_new_round, option_type, last_played_card, last_played_count): #play random type, length, and selection
        play_types = Player.update_options(self, rules, is_new_round, option_type, last_played_card, last_played_count)
        print(play_types)
        if len(play_types) > 1:
            rand = random.randint(0, len(play_types)-1)
        else:
            rand = 0
        play_type = play_types[rand]
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
            options = []
            for card in range(length, 13):
                in_a_row = 0
                for prev_card in range(length,-1,-1):
                    if self.hand[card-prev_card] != 0:
                        in_a_row += 1
                    else:
                        in_a_row = 0
                if in_a_row == length:
                    options.append([num for num in range(card-length, card)])
        elif play_type == 'pair':
            options = [[card, card] for card, count in enumerate(self.hand) if count >= 2 and card > last_played_card]
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
            options = []
            for card in range(length, 13):
                in_a_row = 1
                for prev_card in range(length,-1,-1):
                    if self.hand[card-prev_card] != 0:
                        in_a_row += 1
                    else:
                        in_a_row = 1
                if in_a_row == length:
                    temp = []
                    for num in range(card-length, card):
                        temp.append(num)
                        temp.append(num)
                    options.append(temp)
        elif play_type == 'triple no-carry' or play_type == 'triple single-carry' or play_type == 'triple pair-carry' or play_type == 'triple bomb':
            options = [[card, card, card] for card, count in enumerate(self.hand) if count >= 3 and card > last_played_card]
        elif play_type == 'quad bomb':
            options = [[card, card, card, card] for card, count in enumerate(self.hand) if count == 4 and card > last_played_card]
        elif play_type == 'joker bomb':
            options = [[14, 15]]
        rand = random.randint(0, len(options)-1)
        option = options[rand]
        for card in option:
            self.hand[card] -= 1
        if play_type == 'triple single-carry' or play_type == 'triple pair-carry':
            if play_type == 'triple single-carry':
                carry_options = [[card] for card, count in enumerate(self.hand) if count != 0 and card > last_played_card]
            elif play_type == 'triple pair-carry':
                carry_options = [[card] for card, count in enumerate(self.hand) if count >= 2 and card > last_played_card]
            rand = random.randint(0, len(lengths)-1)
            carry_option = carry_options[rand]
            for card in carry_option:
                self.hand[card] -= 1
                option.append(card)
        print("It's Bot 2's turn. Here is what it played:")
        hand = ''
        for card in option:
            hand += self.card_dict[card] + ', '
        print(hand[:-2] + '\n')
        return play_type, option[0], len(option)
    
    def superbot_pick(self, rules, is_new_round, option_type, last_played_card, last_played_count): #CURR: play random type, pick longest length, select lowest possible   FUTURE: don't allow to break bombs and play them after a certain number of rounds
        play_types = Player.update_options(self, rules, is_new_round, option_type, last_played_card, last_played_count)
        if len(play_types) > 1:
            rand = random.randint(0, len(play_types)-1)
        else:
            rand = 0
        play_type = play_types[rand]
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
            options = []
            for card in range(length, 13):
                in_a_row = 0
                for prev_card in range(length,-1,-1):
                    if self.hand[card-prev_card] != 0:
                        in_a_row += 1
                    else:
                        in_a_row = 0
                if in_a_row == length:
                    options.append([num for num in range(card-length, card)])
        elif play_type == 'pair':
            options = [[card, card] for card, count in enumerate(self.hand) if count >= 2 and card > last_played_card]
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
            options = []
            for card in range(length, 13):
                in_a_row = 1
                for prev_card in range(length,-1,-1):
                    if self.hand[card-prev_card] != 0:
                        in_a_row += 1
                    else:
                        in_a_row = 1
                if in_a_row == length:
                    temp = []
                    for num in range(card-length, card):
                        temp.append(num)
                        temp.append(num)
                    options.append(temp)
        elif play_type == 'triple no-carry' or play_type == 'triple single-carry' or play_type == 'triple pair-carry' or play_type == 'triple bomb':
            options = [[card, card, card] for card, count in enumerate(self.hand) if count >= 3 and card > last_played_card]
        elif play_type == 'quad bomb':
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
                carry_options = [[card] for card, count in enumerate(self.hand) if count >= 2 and card > last_played_card]
            carry_option = carry_options[0]
            for card in carry_option:
                self.hand[card] -= 1
                option.append(card)
        print("It's Superbot's turn. Here is what it played:")
        hand = ''
        for card in option:
            hand += self.card_dict[card] + ', '
        print(hand[:-2] + '\n')
        return play_type, option[0], len(option)

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
        print("The round has started.")
        for _ in range(4): #combine the three of hearts into the threes
            if self.curr_player.data.hand[0] == 1:
                self.curr_player.data.hand[1] += 1
                self.curr_player.data.hand[0] = 0
            self.curr_player = self.curr_player.next
        winner = False
        self.is_new_round = True
        pass_count = 0
        option_type = ''
        self.last_played_card = -1
        self.last_played_count = -1
        while not winner:
            if self.curr_player.data == self.player: #let player play
                option_type, self.last_played_card, self.last_played_count = self.curr_player.data.pick_option(self.settings, self.is_new_round, option_type, self.last_played_card, self.last_played_count)
            elif self.curr_player.data == self.bot1: #bot1 algorithm
                option_type, self.last_played_card, self.last_played_count = self.curr_player.data.bot1_pick(self.settings, self.is_new_round, option_type, self.last_played_card, self.last_played_count)
            elif self.curr_player.data == self.bot2: #bot2 algorithm
                option_type, self.last_played_card, self.last_played_count = self.curr_player.data.bot2_pick(self.settings, self.is_new_round, option_type, self.last_played_card, self.last_played_count)
            else: #superbot play algorithm
                option_type, self.last_played_card, self.last_played_count = self.curr_player.data.superbot_pick(self.settings, self.is_new_round, option_type, self.last_played_card, self.last_played_count)
            if option_type == 'pass': #count passes in a row
                pass_count += 1
            else:
                pass_count = 0
            if pass_count == 3: #if everyone else passed
                print("Everyone passed!")
                self.is_new_round = True
                pass_count = 0
                self.last_played_card = -1
                self.last_played_count = -1
            else:
                self.is_new_round = False
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
                print("Here are the number of cards left in each hand from this round:")
                print("You:      " + sum(self.player.hand))
                print("Bot 1:    " + sum(self.bot1.hand))
                print("Bot 2:    " + sum(self.bot2.hand))
                print("Superbot: " + sum(self.superbot.hand))
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
        print("Your Score:       {self.player.score}")
        print("Bot 1's Score:    {self.bot1.score}")
        print("Bot 2's Score:    {self.bot2.score}")
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