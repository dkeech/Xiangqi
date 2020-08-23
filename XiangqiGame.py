# Author: Dan Keech
# CS 162 Portfolio Project
# This program defines and operates a game of Xiangqi, or Chinese chess.

# Static variables for conversion from letter to number and back
alpha_to_index = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9}
index_to_alpha = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i'}


def no_flying_general(test_board):
    '''Checks to make sure that a move doesn't expose a flying general'''
    # Create a set of generals, find the two generals in the board and insert them.
    generals = []
    gen_set = set()
    # check for flying general
    for key, value in test_board.items():
        if value.lower() == 'g':
            generals.append(key)
    # Order generals in the set by coordinates
    generals.sort(key=lambda x: int(x[1]))
    # If generals are on the same column, make a set of the items between them. If the set only has 1 item (' '),
    # they are flying generals.
    if generals[0][0] == generals[1][0]:
        for i in range(int(generals[0][1]) + 1, int(generals[1][1])):
            gen_set.add(test_board[(generals[0][0], str(i))])
        if len(gen_set) == 1:
            return False
    return True


class XiangqiGame:
    """This class contains all functions in a game of Xiangqi"""

    def __init__(self):
        # Set game state to 'UNFINISHED', initialize dict of pieces, using lower() for red and upper() for black
        # The board is a dict with coords: item, the item is either an empty space, an uppercase
        # letter, or a lowercase letter.
        self._board = {('a', '1'): 'R', ('a', '2'): ' ', ('a', '3'): ' ', ('a', '4'): 'P', ('a', '5'): ' ',
                       ('a', '6'): ' ', ('a', '7'): 'p', ('a', '8'): ' ', ('a', '9'): ' ', ('a', '10'): 'r',
                       ('b', '1'): 'K', ('b', '2'): ' ', ('b', '3'): 'C', ('b', '4'): ' ', ('b', '5'): ' ',
                       ('b', '6'): ' ', ('b', '7'): ' ', ('b', '8'): 'c', ('b', '9'): ' ', ('b', '10'): 'k',
                       ('c', '1'): 'E', ('c', '2'): ' ', ('c', '3'): ' ', ('c', '4'): 'P', ('c', '5'): ' ',
                       ('c', '6'): ' ', ('c', '7'): 'p', ('c', '8'): ' ', ('c', '9'): ' ', ('c', '10'): 'e',
                       ('d', '1'): 'A', ('d', '2'): ' ', ('d', '3'): ' ', ('d', '4'): ' ', ('d', '5'): ' ',
                       ('d', '6'): ' ', ('d', '7'): ' ', ('d', '8'): ' ', ('d', '9'): ' ', ('d', '10'): 'a',
                       ('e', '1'): 'G', ('e', '2'): ' ', ('e', '3'): ' ', ('e', '4'): 'P', ('e', '5'): ' ',
                       ('e', '6'): ' ', ('e', '7'): 'p', ('e', '8'): ' ', ('e', '9'): ' ', ('e', '10'): 'g',
                       ('f', '1'): 'A', ('f', '2'): ' ', ('f', '3'): ' ', ('f', '4'): ' ', ('f', '5'): ' ',
                       ('f', '6'): ' ', ('f', '7'): ' ', ('f', '8'): ' ', ('f', '9'): ' ', ('f', '10'): 'a',
                       ('g', '1'): 'E', ('g', '2'): ' ', ('g', '3'): ' ', ('g', '4'): 'P', ('g', '5'): ' ',
                       ('g', '6'): ' ', ('g', '7'): 'p', ('g', '8'): ' ', ('g', '9'): ' ', ('g', '10'): 'e',
                       ('h', '1'): 'K', ('h', '2'): ' ', ('h', '3'): 'C', ('h', '4'): ' ', ('h', '5'): ' ',
                       ('h', '6'): ' ', ('h', '7'): ' ', ('h', '8'): 'c', ('h', '9'): ' ', ('h', '10'): 'k',
                       ('i', '1'): 'R', ('i', '2'): ' ', ('i', '3'): ' ', ('i', '4'): 'P', ('i', '5'): ' ',
                       ('i', '6'): ' ', ('i', '7'): 'p', ('i', '8'): ' ', ('i', '9'): ' ', ('i', '10'): 'r'}
        self._game_state = 'UNFINISHED'  # RED_WON, BLACK_WON
        self._turn = 0
        self._color = 'red' if self._turn % 2 == 0 else 'black'
        self._test_board = dict
        self._checker = None

    # Getter and setter for the board
    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, d):
        self._board = d

    def print_board(self):
        '''Print the board as it currently stands'''
        board_string = ' '
        for l in 'abcdefghi':
            board_string += f"{l}   "
        board_string += '\n'
        for i in range(1, 11):
            for a in 'abcdefghi':
                board_string += f"[{self._board[(a, str(i))]}]-"
            board_string += f'  {i}\n'
            if i != 5 and i != 10:
                for j in range(1, 10):
                    board_string += ' |  '
            board_string += '\n'
        print(board_string)

    def get_game_state(self):
        """Returns the game state"""
        return self._game_state

    def is_in_check(self, color, check_board=None):
        """Tells you if a piece is in check"""
        general = None
        # Set board either to self._board or a test board to test the next move
        if check_board is None:
            board = self.board
        else:
            board = check_board
        # If red, find upper() G,
        if color.lower() == 'red':
            for key, value in board.items():
                if value == 'G':
                    general = key
                    break
            # if a lowercase piece can move to the general's spot, return True
            for key in self.board:
                if self.board[key].islower():
                    if self.move_helper(key, general, board):
                        return True
        # If black, find lower() g
        if color.lower() == 'black':
            for key, value in board.items():
                if value == 'g':
                    general = key
                    break
            # if an uppercase piece can move to the general's spot, return True
            for key in self.board:
                if self.board[key].isupper():
                    if self.move_helper(key, general, board):
                        return True
        return False

    def opposite_color(self):
        """Returns the opposite color to the active one"""
        if self._color == 'red':
            return 'black'
        else:
            return 'red'

    def count_pieces(self):
        """Returns a tuple of red pieces and black pieces"""
        # This information helps with the simplest stalemate case, where the general is the only piece left.
        red_pieces = 0
        black_pieces = 0
        for key in self.board:
            if self.board[key].isupper():
                red_pieces += 1
            elif self.board[key].islower():
                black_pieces += 1
        return red_pieces, black_pieces

    def locate_generals(self):
        """Find generals' location  for checkmate testing"""
        for key, value in self.board.items():
            if value == 'G':
                self._red_general = key
            if value == 'g':
                self._black_general = key

    def make_move(self, fr, to):
        """Moves pieces as instructed from one space to another, updates board"""
        # Handles universal situations: to an open space, space occupied by opponent, space occupied by same side
        board = self.board
        from_space = (fr[0], fr[1:])
        to_space = (to[0], to[1:])
        # False if space not on board or origin is empty
        if True in [to_space not in board, from_space not in board, board[from_space] == ' ']:
            return False
        # False if wrong color
        if True in [self._turn % 2 == 0 and self._color == 'black', self._turn % 2 != 0 and self._color == 'red']:
            return False
        if self._color == 'red' and self.board[from_space].islower():
            return False
        if self._color == 'black' and self.board[from_space].isupper():
            return False
        # Gets approval from move_helper, which handles individual piece cases
        valid = self.move_helper(from_space, to_space, self._board)
        # if move is not valid, return False
        if not valid:
            return False
        # Handle move: first test to see if it puts piece in check
        else:
            test_board = dict(self.board)
            test_board[to_space] = test_board[from_space]
            test_board[from_space] = ' '
            # Use the test board to see if the move creates a flying general or puts the piece in check
            if no_flying_general(test_board) and not self.is_in_check(self._color, test_board):
                # Add to turn count, put piece in destination, make origin empty
                self._turn += 1
                self._board[to_space] = self._board[from_space]
                self._board[from_space] = ' '
                self.locate_generals()
                self._checker = to_space
                # After deciding that the move is valid, check to see if other color is in check
                # Even if piece is not in check, run checkmate() to see if game is won
                # check to see if solitary General can't move
                if self._color == 'red':
                    if self.is_in_check('black') or self.count_pieces()[1] == 1:
                        if self.checkmate(self._black_general):
                            self._game_state = 'RED_WON'
                else:
                    if self.is_in_check('red') or self.count_pieces()[0] == 1:
                        if self.checkmate(self._red_general):
                            self._game_state = 'BLACK_WON'
                self._color = 'red' if self._turn % 2 == 0 else 'black'
                return True
            return False

    def move_helper(self, fr, to, board=None):
        """Helps the move function by determining if move is valid"""
        # Handles specific piece cases
        if board is None:
            board = self.board
        else:
            board = board
        from_space = fr
        to_space = to
        piece = board[fr]
        knight_count = 0  # this keeps track of the knight's move mid-turn

        # if from is empty, return False. If destination has a piece, validate it as opponent.
        if board[from_space] == ' ':
            return False
        if board[to_space] != ' ':
            # Test capture to see if pieces are on the same team
            if board[from_space].islower() == board[to_space].islower():
                return False

        # Test Rook, that the move is on the same row or column.
        if piece.lower() == 'r':
            if to_space[0] == from_space[0] or to_space[1] == from_space[1]:
                # Check to ensure there are no pieces between start and finish
                if self.check_between_orthogonal(from_space, to_space) > 0:
                    return False
                else:
                    return True
            return False
        # Test Cannon
        if piece.lower() == 'c':
            if to_space[0] == from_space[0] or to_space[1] == from_space[1]:
                # If capturing, ensure that there is exactly one piece between.
                if board[to_space] is not ' ':
                    if self.check_between_orthogonal(from_space, to_space) != 1:
                        return False
                    elif self.check_between_orthogonal(from_space, to_space) == 1:
                        return True
                if self.check_between_orthogonal(from_space, to_space) > 0:
                    return False
                return True
            return False

        # Test Pawn
        if piece.lower() == 'p':
            # Move only forward until past the river, then forward or sideways.
            if piece.isupper():
                if int(to_space[1]) == int(from_space[1]) + 1:
                    return True
                if int(to_space[1]) == int(from_space[1]) - 1:
                    return False
                if int(from_space[1]) >= 6 and board[to_space] == ' ' and to_space in \
                        [(index_to_alpha.get(alpha_to_index[fr[0]] + 1), fr[1]),
                         (index_to_alpha.get(alpha_to_index[fr[0]] - 1), fr[1])]:
                    return True
            if piece.islower():
                if int(to_space[1]) == int(from_space[1]) - 1:
                    return True
                if int(to_space[1]) == int(from_space[1]) + 1:
                    return False

                if int(from_space[1]) <= 5 and board[to_space] == ' ' and to_space in \
                        [(index_to_alpha.get(alpha_to_index[fr[0]] + 1), fr[1]),
                         (index_to_alpha.get(alpha_to_index[fr[0]] - 1), fr[1])]:
                    return True
            return False

        # General/Advisor boundary: make sure General and Advisor only move within their area.
        if piece.lower() == 'g' or piece.lower() == 'a':
            if piece.isupper():
                # set boundary
                if False in [alpha_to_index[to_space[0]] <= 6, alpha_to_index[to_space[0]] >= 4,
                             int(to_space[1]) <= 3]:
                    return False
            if piece.islower():
                if False in [alpha_to_index[to_space[0]] <= 6, alpha_to_index[to_space[0]] >= 4,
                             int(to_space[1]) >= 8]:
                    return False

        # Test General: 1 space forward or one sideways
        if piece.lower() == 'g':
            if True not in [to_space[0] == from_space[0], to_space[1] == from_space[1]]:
                return False
            if True not in [alpha_to_index.get(to_space[0]) == alpha_to_index.get(from_space[0]) + 1,
                            int(to_space[1]) == int(from_space[1]) + 1,
                            alpha_to_index.get(to_space[0]) == alpha_to_index.get(from_space[0]) - 1,
                            int(to_space[1]) == int(from_space[1]) - 1]:
                return False
            return True

        # Test Advisor: one space diagonal
        if piece.lower() == 'a':
            if True in [to_space[0] == from_space[0], to_space[1] == from_space[1],
                        abs(int(to_space[1]) - int(from_space[1])) != 1]:
                return False

        # Test Elephant: two spaces diagonal, only on its side of the river.
        if piece.lower() == 'e':
            if True in [piece.isupper() and int(to_space[1]) > 5, piece.islower() and int(to_space[1]) < 6]:
                return False
            if True in [to_space[0] == from_space[0], to_space[1] == from_space[1],
                        abs(int(to_space[1]) - int(from_space[1])) != 2,
                        abs(alpha_to_index[to_space[0]] - alpha_to_index[from_space[0]]) != 2]:
                return False
            middle_piece = (index_to_alpha[int((int(alpha_to_index[from_space[0]]) +
                                                int(alpha_to_index[to_space[0]])) / 2)],
                            str(int((int(from_space[1]) + int(to_space[1])) / 2)))
            if board[middle_piece] != ' ':
                return False

        # Test knight: check that there is no piece on the orthogonal leg or the diagonal leg of the move.
        if piece.lower() == 'k' and knight_count == 0:
            forward_gap = int(to_space[1]) - int(from_space[1])
            side_gap = alpha_to_index[to_space[0]] - alpha_to_index[from_space[0]]
            if abs(forward_gap) == 2 and abs(side_gap) == 1:
                first_step = (from_space[0], str(int(from_space[1]) + int(forward_gap / 2)))
                if board[first_step] == ' ':
                    return True
                return False
            elif abs(side_gap) == 2 and abs(forward_gap) == 1:
                first_step = (
                index_to_alpha[alpha_to_index[from_space[0]] + int(side_gap / 2)], from_space[1])
                if board[first_step] == ' ':
                    return True
            return False
        return True

    def check_between_orthogonal(self, fr, to):
        '''Counts pieces between start and destination on a row or column'''
        fr0, fr1, to0, to1 = alpha_to_index[fr[0]], int(fr[1]), alpha_to_index[to[0]], int(to[1])
        occupied_spaces = set()
        if fr0 == to0:
            if fr1 < to1:
                for i in range(fr1 + 1, to1):
                    if self._board[index_to_alpha[fr0], str(i)] != ' ':
                        occupied_spaces.add((index_to_alpha[fr0], str(i)))
            else:
                for i in range(to1 + 1, fr1):
                    if self._board[index_to_alpha[fr0], str(i)] != ' ':
                        occupied_spaces.add((index_to_alpha[fr0], str(i)))
        if fr1 == to1:
            if fr0 < to0:
                for i in range(fr0 + 1, to0):
                    if self._board[index_to_alpha[i], str(fr1)] != ' ':
                        occupied_spaces.add((index_to_alpha[i], str(fr1)))
            else:
                for i in range(to0 + 1, fr0):
                    if self._board[index_to_alpha[i], str(fr1)] != ' ':
                        occupied_spaces.add((index_to_alpha[i], str(fr1)))
        return len(occupied_spaces)

    def fake_move(self, fr, to):
        """Moves pieces as instructed from one space to another, updates board"""
        # Makes the move on a test board so that it can be checked for checkmate, flying general, stalemate
        board = self._test_board
        from_space = fr
        to_space = to

        # False if space not on board or origin is empty
        if True in [to_space not in board, from_space not in board, board[from_space] == ' ']:
            return False

        # Gets approval from move_helper, which handles individual piece cases
        valid = self.move_helper(from_space, to_space, board)

        # Use the test board to see if the move creates a flying general or puts the piece in check
        if valid and no_flying_general(board):
            # Add to turn count, put piece in destination, make origin empty
            self._turn += 1
            board[to_space] = board[from_space]
            board[from_space] = ' '
            if not self.is_in_check(self._color, board):
                return True
        return False

    def test_prospective_move(self, fr, to, color):
        """Tests a move before it is made"""
        # Copy current state of board to the test board
        self._test_board = dict(self.board)
        # Validate in move_helper()
        if self.move_helper(fr, to, self._test_board):
            self.fake_move(fr, to)
        # If the move takes piece out of check
        if not self.is_in_check(color, self._test_board):
            return True
        return False

    def checkmate(self, position):
        """Test to see if a position is in checkmate"""
        looking = True
        # Convert position to numbers so General moves can be calculated
        convert_position = (alpha_to_index[position[0]], int(position[1]))
        a, i = convert_position[0], convert_position[1]
        valid_moves = []
        color = 'black' if self.board[position].islower() else 'red'
        # Count theoretically possible moves, including off board
        moves = [(a + 1, i), (a - 1, i), (a, i + 1), (a, i - 1)]
        # Cull on-board moves
        culled_moves = [move for move in moves if 9 >= move[0] > 0 and 10 >= move[1] > 0]
        # Convert back to str tuple
        moves_str = [(index_to_alpha[move[0]], str(move[1]))for move in culled_moves]

        # see if king can move out of check
        while looking:
            for move in moves_str:
                try:
                    if self.test_prospective_move(position, move, color):
                        valid_moves.append(move)
                except:
                    pass
            looking = False
        # If there is at least one valid move, it's not checkmate.
        if len(valid_moves) > 0:
            return False
        return True


def main():
    pass

if __name__ == '__main__':
    main()


