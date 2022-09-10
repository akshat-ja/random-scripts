import random
import string
from hangmanwords import words
from hangmandraw import lives_visual_dict

# print(words)

def randomword():
    w = ' '
    while '-' in w or ' ' in w:
        w = random.choice(words)
    return w
    
def hangman():
    word = randomword().upper()
    wlist = list(word)
    wset = set(word)
    alphabet = set(string.ascii_uppercase)
    used_inputs = set()
    good_inputs = set()
    tries = 7
    
    while tries != 0 and len(wset) != 0:
        # print(word)
        # print(wlist)
        # print(wset)
        # print(used_inputs, tries)
        # print(alphabet)
        
        print('WORD:',end=' ')
        for x in wlist:
            if x in good_inputs:
                print(x,end=' ')
            else:
                print('_',end=' ')
        print()
        
        print('USED:',end=' ')
        for x in used_inputs:
            print(x,end=' ')
        print()
        
        user_input = input('Guess a letter: ').upper()
        if user_input in alphabet - used_inputs:
            if user_input in wset:
                wset.remove(user_input)
                used_inputs.add(user_input)
                good_inputs.add(user_input)
                print(f'Good guess {user_input}.')
            elif user_input in used_inputs:
                print(f'You have already used {user_input}. Try again.')
            else:
                tries -= 1
                used_inputs.add(user_input)
                print(f'Bad choice {user_input}. Try again.')
        else:
            print(f'Invalid choice. Try again.')
        
        print(lives_visual_dict[tries])
        

    if tries == 0:
        print(f'YOU DED. Word was {word}.')
    else:
        print('YOU WIN.')

def main():
    hangman()

if __name__ == "__main__":
   main()