import random

def play():
    user = input("(r)ock, (p)aper, (s)cissors: ")
    comp = random.choice(['r','p','s'])
    print(f'You chose {user} and the computer chose {comp}.')
    game(user,comp)
    
def game(a,b):
    if a == b:
        print('Tied.')
    if a == 'r' and b == 's':
        print('Player wins. r > s')
    if a == 's' and b == 'p':
        print('Player wins. s > p')
    if a == 'p' and b == 'r':
        print('Player wins. p > r')
    if a == 'r' and b == 'p':
        print('Player loses. r < p')
    if a == 'p' and b == 's':
        print('Player loses. p < s')
    if a == 's' and b == 'r':
        print('Player loses. s < r')
    
play()