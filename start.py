import mechanics

ansr = input("Hi! Welcome to Zheng Shangyou. Would you like to play a game?\n(y/n)\n")
while ansr not in ['y', 'n']:
    ansr = input("Please try again.\n(y/n)\n")
if ansr == 'n':
    print("Okay, have a nice day!")
    exit()
mechanics.start()