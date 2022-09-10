from player import HumanPlayer, RandomComputerPlayer

class TicTacToe:
    
    def __init__(self):
        # Single list to represent 3x3 board
        self.board = [' ' for _ in range(9)]
        self.current_winner = None # for now
    
    def print_board(self):
        # This is just getting the rows
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        # | 1 | 2 | 3 |
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')
    
    def available_moves(self):
        # return [i for i, spot in enumerate(self.board) if spot == ' ']
        moves = []
        for i,spot in enumerate(self.board):
            if spot == ' ':
                moves.append[i]
        return moves
        # Shortened output
        # return [i for i,spot in enumerate(self.board) if spot == ' ']
    
    def empty_squares(self):
        return ' ' in self.board # Boolean output
    
    def num_empty_squares(self):
        # return len(self.available_moves())
        return self.board.count(' ')
    
    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square,letter):
                self.current_winner = letter
            return True
        return False
    
    def winner(self, square, letter):
        # Check row winner
        row_ind = square // 3
        row = self.board[row_ind * 3 : (row_ind+1) * 3]
        if all([spot == letter for spot in row]):
            return True

        # Check column winner
        col_ind = square % 3
        col = [self.board[col_ind + i * 3] for i in range(3)]
        if all([spot == letter for spot in col]):
            return True

        # Check diag winner
        if square % 2 == 0:
            diag1 = [self.board[i] for i in [0,4,8]]
            if all([spot == letter for spot in diag1]):
                return True
            diag2 = [self.board[i] for i in [2,4,6]]
            if all([spot == letter for spot in diag2]):
                return True

        # If all checks fail
        return False

        # If 3 in a row anywhere, row, column, diagonal
        # Target winning trio sets
        # target_sets = [
        #     # Horizontal
        #     [1,2,3],
        #     [4,5,6],
        #     [7,8,9],
        #     # Vertical
        #     [1,4,7],
        #     [2,5,8],
        #     [7,8,9],
        #     # Diagonal
        #     [1,5,9],
        #     [3,5,7]
        # ]
        # print(target_sets)

    # def next_attack(self):
    #     pass
    # def next_defense(self):
    #     pass
    
def play(game, x_player, o_player, print_game = True):
    # returns the winner (letter X or O), or None if it is a tie
    if print_game:
        game.print_board_nums()
    
    letter =  'X' # starting letter
    
    while game.empty_squares():
        # Get the move from the active player
        if letter == 'O':
            square = o_player.get_move()
        else:
            square = x_player.get_move()
        
        if game.make_move(square, letter):
            if print_game:
                print(letter + ' makes a move to square ' + square)
                game.print_board()
                print('')
            
            if game.current_winner:
                if print_game:
                    print(letter + ' wins!')
                return letter
            
            letter = 'O' if letter == 'X' else 'X'
            
            if print_game:
                print('It\'s a tie!')

if __name__ == '__main__':
    x_player = HumanPlayer('X')
    o_player = RandomComputerPlayer('O')
    t = TicTacToe()
    play(t,
         x_player,
         o_player,
         print_game=True
         )
    
    ### Work in progress ###