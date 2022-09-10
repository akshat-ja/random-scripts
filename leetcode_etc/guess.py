import random

def guess(x):
        rando = random.randint(1,x)
        guess = 0
        
        while guess != rando:
            guess = int(input(f'Guess a num between 1 and {x}: '))
            if guess < rando:
                print('aim higher')
            elif guess > rando:
                print('aim lower')
                
        print(f'Congrats, you guessed {rando} right!')

def comp_guess(x):
    low = 1
    high = x
    feedback = ''
    
    print('Answer with (h)igh, (l)ow or (c)orrect:')
    while feedback != 'c':
        if low != high:
            guess = random.randint(low,high)
        else:
            guess = low
        feedback = input(f'Is {guess} too (h)igh, too (l)ow or (c)orrect: ')
        if feedback == 'h':
            high = guess - 1 # random.randint(1,guess-low)
        if feedback == 'l':
            low = guess + 1 # random.randint(1,high-guess)
            
    if low == high:
        print('low == high')
    else:
        print(f'Congrats, you guessed {x} right!')


def main():
    guess(10)
    comp_guess(10)


if __name__ == "__main__":
   main()