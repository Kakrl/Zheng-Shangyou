class Player:
    def __init__(self, hand, is_past_winner, score):
        self.hand = hand
        self.is_past_winner = is_past_winner
        self.score = score
    
    def options(self):
        pass
    
    def play(self, option):
        pass

class Game:
    def __init__(self, settings, age, player, bot1, bot2, superbot):
        self.settings = settings
        self.age = age
        self.player = player
        self.bot1 = bot1
        self.bot2 = bot2
        self.superbot = superbot
        
    def get_settings(self):
        ansr = input("Yay! Would you like to play standard or custom rules? (standard/custom)\n")
        while ansr not in ['standard', 'custom']:
            ansr = input("(standard/custom)\n")
        if ansr == 'standard':
            rules = ['y', 'n', 'n', 'y']
            print("Here are your selected rules:")
            Game.display_settings(rules)
        else:
            confirmation = 'n'
            while confirmation == 'n':
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
        self.settings = rules
    
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
    
    def play_phase(self, order):
        winner = False
        while not winner:
            for next in order:
                #turn
                if not next.hand:
                    winner = True
                    next.is_past_winner = True #make other players be False
                    self.age += 1
        Game.end()
        
    def end(self):
        ansr = input("Would you like to reset the game, play the next round, or end the game? (reset/next/end)\n")
        while ansr not in ['next', 'end', 'reset']:
            ansr = input("Please try again. (reset/next/end)\n")
        if ansr == 'reset':
            start()
        elif ansr == 'next':
            play_phase()
        
    def display_scoreboard(self):
        print("Player's Score: {self.player.score}")
        print("Bot 1's Score: {self.bot1.score}")
        print("Bot 2's Score: {self.bot2.score}")
        print("Superbot's Score: {self.superbot.score}")
    
def deal(): #each hand list's index represents cards from 3-of-hearts,3,4,5,6,7,8,9,10,J,Q,K,A,2,BJoker,RJoker
    master = [1, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1]
    hand1 = [0] * 16
    hand2 = [0] * 16
    hand3 = [0] * 16
    hand4 = [0] * 16
    return hand1, hand2, hand3, hand4
    
def order(age, player, bot1, bot2, superbot):
    if age == 1:
        if player.hand[0] == 1:
            play_order = [player, bot1, bot2, superbot]
        elif bot1.hand[0] == 1:
            play_order = [bot1, bot2, superbot, player]
        elif bot2.hand[0] == 1:
            play_order = [bot2, superbot, player, bot1]
        else:
            play_order = [superbot, player, bot1, bot2]
    else:
        if player.is_past_winner == True:
            play_order = [player, bot1, bot2, superbot]
        elif bot1.is_past_winner == True:
            play_order = [bot1, bot2, superbot, player]
        elif bot2.is_past_winner == True:
            play_order = [bot2, superbot, player, bot1]
        else:
            play_order = [superbot, player, bot1, bot2]
    return play_order

def start():
    hand1, hand2, hand3, hand4 = deal()
    player = Player(hand1, False, 0)
    bot1 = Player(hand2, False, 0)
    bot2 = Player(hand3, False, 0)
    superbot = Player(hand4, False, 0)
    game = Game([], 1, player, bot1, bot2, superbot)
    game.get_settings()
    game.play_phase(order(game.age, player, bot1, bot2, superbot))