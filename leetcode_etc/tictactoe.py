import math
import random

class Player:
    def __init__(self, letter):
        # Letter being X or O
        self.letter = letter
    
    def get_move(self, game):
        pass

class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)
    
    def get_move(self, game):
        square = random.choice(game.available_moves())

class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)
    
    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            # Check for valid integer val input
            square = input(self.letter + '\'s. Input move (0-9)')
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except:
                print('Invalid square. Try again.')
        return val
    
    ### Work in progress ###
