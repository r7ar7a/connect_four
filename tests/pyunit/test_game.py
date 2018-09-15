import unittest

from connect_four.game import ConnectFourGame, InvalidMove, GameStates


class TestGame(unittest.TestCase):
    def test(self):
        with self.assertRaises(ValueError):
            ConnectFourGame(0, 6, 'p1', 'p2')
        with self.assertRaises(ValueError):
            ConnectFourGame(-2, 7, 'p1', 'p2')
        with self.assertRaises(ValueError):
            ConnectFourGame(2, 0, 'p1', 'p2')

        game = ConnectFourGame(7, 6, 'p1', 'p2')
        assert game.current_player() == 'p1'
        with self.assertRaises(InvalidMove):
            game.move(-1)
        assert game.occupied_by(0, 0) is None
        for _ in range(6):
            game.move(0)
        assert game.occupied_by(0, 0) == 'p1'
        assert game.occupied_by(0, 1) == 'p2'
        assert game.current_player() == 'p1'
        with self.assertRaises(InvalidMove):
            game.move(0)

        for i in range(1, 3):
            game.move(i)  # p1
            game.move(i)  # p2
        game.move(3)
        assert game.get_state() == GameStates.PLAYER_1_WIN
        with self.assertRaises(InvalidMove):
            game.undo()
        with self.assertRaises(InvalidMove):
            game.move(3)
        assert game.get_winning_row() == [(i, 0) for i in range(4)]

    def test_draw(self):
        game = ConnectFourGame(1, 1, 'p1', 'p2')
        with self.assertRaises(InvalidMove):
            game.move(0, player='p2')
        assert game.get_state() == GameStates.OPEN
        game.move(0)
        assert game.get_state() == GameStates.DRAW
        with self.assertRaises(InvalidMove):
            game.move(0)

    def test_undo(self):
        game = ConnectFourGame(7, 6, 'p1', 'p2')
        with self.assertRaises(InvalidMove):
            game.undo()
        assert game.occupied_by(0, 0) is None
        game.move(0, player='p1')
        assert game.occupied_by(0, 0) == 'p1'
        with self.assertRaises(InvalidMove):
            game.undo(player='p2')
        game.undo(player='p1')
        assert game.occupied_by(0, 0) is None
