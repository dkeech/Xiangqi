import unittest
import XiangqiGame


class TestOpenMove(unittest.TestCase):
    def test_rook(self):
        x = XiangqiGame.XiangqiGame()
        x.make_move('a1', 'a2')
        self.assertEqual(x.board[('a', '2')], 'R')
        self.assertEqual(x.board[('a', '1')], ' ')
        x.make_move('a10', 'a8')
        self.assertEqual(x.board[('a', '8')], 'r')
        self.assertEqual(x.board[('a', '10')], ' ')
        x.make_move('a2', 'a1')
        self.assertEqual(x.board[('a', '1')], 'R')
        self.assertEqual(x.board[('a', '2')], ' ')
        x.make_move('i10', 'i9')
        self.assertEqual(x.board[('i', '9')], 'r')
        self.assertEqual(x.board[('i', '10')], ' ')
        # test off board coordinates
        x.make_move('a1', 'a0')
        self.assertEqual(x.board[('a', '1')], 'R')
        # self.assertEqual(x.make_move('z11', 'a2'), False)

    def test_cannon(self):
        x = XiangqiGame.XiangqiGame()
        x.make_move('b3', 'g3')
        self.assertEqual(x.board[('g', '3')], 'C')
        self.assertEqual(x.board[('b', '3')], ' ')
        x.make_move('b8', 'b5')
        self.assertEqual(x.board[('b', '5')], 'c')
        self.assertEqual(x.board[('b', '8')], ' ')

    def test_pawn(self):
        x = XiangqiGame.XiangqiGame()
        x.make_move('a4', 'a6')
        self.assertEqual(x.board[('a', '6')], ' ')
        x.make_move('a4', 'a3')
        self.assertEqual(x.board[('a', '4')], 'P')
        x.make_move('a4', 'a5')
        self.assertEqual(x.board[('a', '5')], 'P')
        x.make_move('c7', 'c6')
        self.assertEqual(x.board[('c', '6')], 'p')
        x.make_move('a5', 'b5')
        self.assertEqual(x.board[('b', '5')], ' ')
        x.make_move('a5', 'a6')
        x.make_move('c6', 'c5')
        x.make_move('a6', 'b6')
        self.assertEqual(x.board[('b', '6')], 'P')

    def test_general(self):
        x = XiangqiGame.XiangqiGame()
        x.make_move('e1', 'e2')
        self.assertEqual(x.board[('e', '2')], 'G')
        self.assertEqual(x.board[('e', '1')], ' ')
        x.make_move('e10', 'e9')
        x.make_move('e2', 'e1')
        self.assertEqual(x.board[('e', '1')], 'G')
        x.make_move('e9', 'f8')
        self.assertEqual(x.board[('e', '9')], 'g') # make sure diag doesn't work
        x.make_move('e9', 'd9')
        x.make_move('e1', 'e2')
        x.make_move('d9', 'c9')
        self.assertEqual(x.board[('d', '9')], 'g')
        x.make_move('d9', 'd8')
        x.make_move('e2', 'f2')
        x.make_move('d8', 'd7')
        self.assertEqual(x.board[('d', '7')], ' ')
        self.assertEqual(x.get_game_state(), 'UNFINISHED')

    def test_advisor(self):
        x = XiangqiGame.XiangqiGame()
        x.make_move('d1', 'e2')
        x.make_move('d10', 'c9')  # test out of bounds
        self.assertEqual(x.board[('d', '10')], 'a')
        x.make_move('d10', 'd9') # test straight
        self.assertEqual(x.board[('d', '9')], ' ')
        x.make_move('d10', 'e9')
        self.assertEqual(x.board[('d', '10')], ' ')
        x.make_move('e2', 'd3')
        x.make_move('e9', 'f8')
        x.make_move('d3', 'c2')
        self.assertEqual(x.board[('d', '3')], 'A')
        x.make_move('d3', 'e2')
        x.make_move('f8', 'd10')
        self.assertEqual(x.board[('f', '8')], 'a')

    def test_knight(self):
        x = XiangqiGame.XiangqiGame()
        x.make_move('b1', 'a3')
        self.assertEqual(x.board[('a', '3')], 'K')
        x.make_move('b10', 'c8')
        x.make_move('b3', 'b4')
        x.make_move('c8', 'e9')  # sideways
        self.assertEqual(x.board[('e', '9')], 'k')
        x.make_move('a3', 'c5')  # fail sideways
        self.assertEqual(x.board[('a', '3')], 'K')
        x.make_move('a3', 'c2')
        x.make_move('e9', 'f7')
        self.assertEqual(x.board[('f', '7')], 'k')
        x.make_move('c2', 'd4')  # check
        x.make_move('f7', 'e5')
        x.make_move('d4', 'e6')  # check capture
        x.make_move('e5', 'g4')  # fail
        x.make_move('e6', 'c7')
        x.make_move('g4', 'h2')
        x.make_move('c7', 'a8')
        x.make_move('b8', 'b7')
        x.make_move('a8', 'c9')
        x.make_move('h2', 'f1')


class TestCapture(unittest.TestCase):
    def test_rook(self):
        x = XiangqiGame.XiangqiGame()
        x.make_move('a1', 'a2')
        x.make_move('i10', 'i9')
        x.make_move('a2', 'd2')
        x.make_move('i9', 'd9')
        x.make_move('d2', 'd9')
        self.assertEqual(x.board[('d', '9')], 'R')
        black_rooks = sum(value == 'r' for value in x.board.values())
        self.assertEqual(black_rooks, 1)

    def test_cannon(self):
        x = XiangqiGame.XiangqiGame()
        x.make_move('h3', 'h10')
        self.assertEqual(x.board[('h', '10')], 'C')
        x.make_move('b8', 'b2')
        self.assertEqual(x.board[('b', '8')], 'c')
        x.make_move('b8', 'b7')
        x.make_move('a1', 'a2')
        x.make_move('b7', 'e7')
        self.assertEqual(x.board[('b', '7')], 'c')
        self.assertEqual(x.get_game_state(), 'UNFINISHED')

    def test_pawn(self):
        x = XiangqiGame.XiangqiGame()
        x.make_move('a4', 'a5')
        x.make_move('c7', 'c6')
        x.make_move('a5', 'a6')
        x.make_move('c6', 'c5')
        x.make_move('a6', 'a7')
        self.assertEqual(x.board[('a', '7')], 'P')
        x.make_move('c5', 'd5')
        x.make_move('a7', 'b7')
        x.make_move('d5', 'd4')
        x.make_move('b7', 'b8')
        self.assertEqual(x.board[('b', '8')], 'P')
        x.make_move('d4', 'e4')
        self.assertEqual(x.board['d', '4'], 'p')


class TestOccupiedBySameTeam(unittest.TestCase):
    def test_rook(self):
        y = XiangqiGame.XiangqiGame()
        y.make_move('a1', 'a4')
        self.assertEqual(y.board[('a', '1')], 'R')
        self.assertEqual(y.board[('a', '4')], 'P')
        y.make_move('a1', 'a2')
        y.make_move('a10', 'b10')
        self.assertEqual(y.board[('a', '10')], 'r')
        self.assertEqual(y.board[('b', '10')], 'k')


class TestMoveOverPiece(unittest.TestCase):
    def test_rook(self):
        x = XiangqiGame.XiangqiGame()
        x.make_move('a1', 'a9')
        self.assertEqual(x.board[('a', '1')], 'R')
        self.assertEqual(x.board[('a', '9')], ' ')

    def test_cannon(self):
        x = XiangqiGame.XiangqiGame()
        x.make_move('b3', 'b4')
        x.make_move('b8', 'c8')
        x.make_move('b4', 'd4')
        self.assertEqual(x.board[('b', '4')], 'C')

    def test_elephant(self):
        """This tests move, capture, and attempt to jump a piece"""
        x = XiangqiGame.XiangqiGame()
        x.make_move('c1', 'e3')
        x.make_move('c10', 'a8')
        self.assertEqual(x.board[('a', '8')], 'e')
        x.make_move('e3', 'g3')  # fail sideways
        self.assertEqual(x.board[('g', '3')], ' ')
        x.make_move('e3', 'f5')  # fail diag + orth
        self.assertEqual(x.board[('e', '3')], 'E')
        x.make_move('e3', 'c5')  # check
        self.assertEqual(x.board[('c', '5')], 'E')
        x.make_move('e7', 'e6')
        x.make_move('c5', 'a7')  # check over river
        self.assertEqual(x.board[('a', '7')], 'p')
        x.make_move('b3', 'b7')
        x.make_move('a8', 'c6')  # assert c6 = ' '
        self.assertEqual(x.board[('c', '6')], ' ')
        x.make_move('g10', 'e8')
        x.make_move('b7', 'b10')
        x.make_move('e10', 'e9')
        x.make_move('c5', 'e7')  # assert e7 = ' '
        self.assertEqual(x.board[('e', '7')], ' ')
        x.make_move('g1', 'e3')
        x.make_move('e8', 'g6')
        x.make_move('e4', 'e5')
        x.make_move('g6', 'e4')  # assert e4 = ' '
        self.assertEqual(x.board[('e', '4')], ' ')


class test_check(unittest.TestCase):
    def test_check(self):
        x = XiangqiGame.XiangqiGame()
        x.make_move('a1', 'a2')
        x.board = {('a', '1'): 'R', ('a', '2'): ' ', ('a', '3'): ' ', ('a', '4'): ' ', ('a', '5'): 'P', ('a', '6'): ' ', ('a', '7'): 'p', ('a', '8'): ' ', ('a', '9'): ' ', ('a', '10'): 'r', ('b', '1'): ' ', ('b', '2'): ' ', ('b', '3'): ' ', ('b', '4'): ' ', ('b', '5'): ' ', ('b', '6'): ' ', ('b', '7'): 'C', ('b', '8'): 'c', ('b', '9'): ' ', ('b', '10'): ' ', ('c', '1'): ' ', ('c', '2'): ' ', ('c', '3'): ' ', ('c', '4'): ' ', ('c', '5'): ' ', ('c', '6'): ' ', ('c', '7'): ' ', ('c', '8'): ' ', ('c', '9'): ' ', ('c', '10'): 'e', ('d', '1'): 'A', ('d', '2'): ' ', ('d', '3'): ' ', ('d', '4'): ' ', ('d', '5'): ' ', ('d', '6'): 'k', ('d', '7'): ' ', ('d', '8'): ' ', ('d', '9'): ' ', ('d', '10'): ' ', ('e', '1'): 'G', ('e', '2'): ' ', ('e', '3'): 'E', ('e', '4'): 'P', ('e', '5'): ' ', ('e', '6'): 'p', ('e', '7'): 'k', ('e', '8'): ' ', ('e', '9'): 'a', ('e', '10'): 'g', ('f', '1'): 'A', ('f', '2'): ' ', ('f', '3'): ' ', ('f', '4'): ' ', ('f', '5'): ' ', ('f', '6'): ' ', ('f', '7'): ' ', ('f', '8'): ' ', ('f', '9'): ' ', ('f', '10'): 'a', ('g', '1'): 'E', ('g', '2'): ' ', ('g', '3'): ' ', ('g', '4'): 'P', ('g', '5'): ' ', ('g', '6'): 'p', ('g', '7'): ' ', ('g', '8'): ' ', ('g', '9'): 'K', ('g', '10'): ' ', ('h', '1'): 'K', ('h', '2'): ' ', ('h', '3'): 'C', ('h', '4'): ' ', ('h', '5'): ' ', ('h', '6'): ' ', ('h', '7'): 'c', ('h', '8'): ' ', ('h', '9'): ' ', ('h', '10'): ' ', ('i', '1'): 'R', ('i', '2'): ' ', ('i', '3'): ' ', ('i', '4'): ' ', ('i', '5'): 'P', ('i', '6'): ' ', ('i', '7'): 'p', ('i', '8'): ' ', ('i', '9'): ' ', ('i', '10'): 'r'}
        self.assertEqual(x.is_in_check('black'), True)
        self.assertEqual(x.get_game_state(), 'UNFINISHED')

        x.make_move('e10', 'd10')
        x.make_move('g1', 'i3')
        x.make_move('h7', 'h1')
        self.assertEqual(x.is_in_check('red'), True)
        self.assertEqual(x.get_game_state(), 'UNFINISHED')
        x.print_board()


class test_flying_general(unittest.TestCase):
    def test_fg(self):
        x = XiangqiGame.XiangqiGame()
        x._turn = 1
        x.board = {('a', '1'): 'R', ('a', '2'): ' ', ('a', '3'): ' ', ('a', '4'): ' ', ('a', '5'): 'P', ('a', '6'): ' ',
                   ('a', '7'): 'p', ('a', '8'): ' ', ('a', '9'): ' ', ('a', '10'): 'r', ('b', '1'): ' ',
                   ('b', '2'): ' ',
                   ('b', '3'): ' ', ('b', '4'): ' ', ('b', '5'): ' ', ('b', '6'): ' ', ('b', '7'): ' ', ('b', '8'): 'c',
                   ('b', '9'): ' ', ('b', '10'): ' ', ('c', '1'): ' ', ('c', '2'): ' ', ('c', '3'): 'k',
                   ('c', '4'): ' ',
                   ('c', '5'): ' ', ('c', '6'): ' ', ('c', '7'): ' ', ('c', '8'): ' ', ('c', '9'): ' ',
                   ('c', '10'): 'e',
                   ('d', '1'): 'A', ('d', '2'): ' ', ('d', '3'): ' ', ('d', '4'): ' ', ('d', '5'): ' ', ('d', '6'): ' ',
                   ('d', '7'): ' ', ('d', '8'): ' ', ('d', '9'): ' ', ('d', '10'): 'g', ('e', '1'): ' ',
                   ('e', '2'): ' ',
                   ('e', '3'): 'E', ('e', '4'): ' ', ('e', '5'): ' ', ('e', '6'): 'p', ('e', '7'): 'k', ('e', '8'): ' ',
                   ('e', '9'): 'a', ('e', '10'): ' ', ('f', '1'): 'A', ('f', '2'): 'G', ('f', '3'): ' ',
                   ('f', '4'): ' ',
                   ('f', '5'): ' ', ('f', '6'): ' ', ('f', '7'): ' ', ('f', '8'): ' ', ('f', '9'): ' ',
                   ('f', '10'): 'a',
                   ('g', '1'): ' ', ('g', '2'): ' ', ('g', '3'): ' ', ('g', '4'): 'P', ('g', '5'): ' ', ('g', '6'): 'p',
                   ('g', '7'): ' ', ('g', '8'): ' ', ('g', '9'): 'K', ('g', '10'): ' ', ('h', '1'): 'c',
                   ('h', '2'): ' ',
                   ('h', '3'): 'C', ('h', '4'): ' ', ('h', '5'): ' ', ('h', '6'): ' ', ('h', '7'): ' ', ('h', '8'): ' ',
                   ('h', '9'): ' ', ('h', '10'): ' ', ('i', '1'): 'R', ('i', '2'): ' ', ('i', '3'): 'E',
                   ('i', '4'): ' ',
                   ('i', '5'): 'P', ('i', '6'): ' ', ('i', '7'): 'C', ('i', '8'): ' ', ('i', '9'): ' ',
                   ('i', '10'): 'r'}
        x._color = 'black'
        x.make_move('c3', 'd1')
        x.make_move('i10', 'i7')
        self.assertEqual(x.make_move('e2', 'd2'), False)


class test_checkmate(unittest.TestCase):
    def test_cm(self):
        x = XiangqiGame.XiangqiGame()
        x.board = {('a', '1'): 'r', ('a', '2'): ' ', ('a', '3'): ' ', ('a', '4'): ' ', ('a', '5'): ' ', ('a', '6'): ' ', ('a', '7'): ' ', ('a', '8'): ' ', ('a', '9'): ' ', ('a', '10'): ' ', ('b', '1'): ' ', ('b', '2'): ' ', ('b', '3'): ' ', ('b', '4'): ' ', ('b', '5'): ' ', ('b', '6'): ' ', ('b', '7'): ' ', ('b', '8'): ' ', ('b', '9'): ' ', ('b', '10'): ' ', ('c', '1'): ' ', ('c', '2'): ' ', ('c', '3'): ' ', ('c', '4'): ' ', ('c', '5'): ' ', ('c', '6'): ' ', ('c', '7'): ' ', ('c', '8'): ' ', ('c', '9'): ' ', ('c', '10'): 'e', ('d', '1'): ' ', ('d', '2'): ' ', ('d', '3'): 'C', ('d', '4'): ' ', ('d', '5'): ' ', ('d', '6'): ' ', ('d', '7'): ' ', ('d', '8'): 'a', ('d', '9'): ' ', ('d', '10'): ' ', ('e', '1'): ' ', ('e', '2'): ' ', ('e', '3'): 'E', ('e', '4'): ' ', ('e', '5'): ' ', ('e', '6'): 'p', ('e', '7'): 'k', ('e', '8'): 'c', ('e', '9'): 'a', ('e', '10'): 'g', ('f', '1'): 'A', ('f', '2'): 'G', ('f', '3'): ' ', ('f', '4'): ' ', ('f', '5'): ' ', ('f', '6'): ' ', ('f', '7'): ' ', ('f', '8'): ' ', ('f', '9'): ' ', ('f', '10'): ' ', ('g', '1'): ' ', ('g', '2'): ' ', ('g', '3'): ' ', ('g', '4'): 'P', ('g', '5'): ' ', ('g', '6'): 'p', ('g', '7'): ' ', ('g', '8'): ' ', ('g', '9'): ' ', ('g', '10'): ' ', ('h', '1'): 'R', ('h', '2'): ' ', ('h', '3'): ' ', ('h', '4'): ' ', ('h', '5'): ' ', ('h', '6'): ' ', ('h', '7'): ' ', ('h', '8'): ' ', ('h', '9'): ' ', ('h', '10'): ' ', ('i', '1'): ' ', ('i', '2'): ' ', ('i', '3'): 'E', ('i', '4'): ' ', ('i', '5'): 'P', ('i', '6'): ' ', ('i', '7'): 'r', ('i', '8'): ' ', ('i', '9'): ' ', ('i', '10'): ' '}

        x.make_move('h1', 'h10')
        self.assertEqual(x.get_game_state(), 'RED_WON')

class test_162(unittest.TestCase):
    def test_test(self):
        game = XiangqiGame.XiangqiGame()
        move_result = game.make_move('c1', 'e3')
        black_in_check = game.is_in_check('black')
        self.assertEqual(black_in_check, False)
        game.make_move('e7', 'e6')
        state = game.get_game_state()
        self.assertEqual(state, 'UNFINISHED')

if __name__ == '__main__':
    unittest.main()
