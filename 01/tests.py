import unittest
import numpy as np
from Exceptions import InputError
from python_homework1 import TicTacGame


class TicTacTest(unittest.TestCase):
    def setUp(self):
        self.game = TicTacGame()

    def test_validate_size(self):
        with self.assertRaises(InputError):
            self.game.validate_size("21")

        with self.assertRaises(InputError):
            self.game.validate_size("2.1")

        with self.assertRaises(InputError):
            self.game.validate_size("2")

        self.game.validate_size("15")
        self.assertEqual(self.game.size, 15)

    def test_validate_input(self):
        with self.assertRaises(InputError):
            self.game.validate_input(["1", " 2"], 1)

        with self.assertRaises(InputError):
            self.game.validate_input(["1.2"], 1)

        with self.assertRaises(InputError):
            self.game.validate_input(["4, 3"], 1)

        with self.assertRaises(InputError):
            self.game.validate_input(["1,1"], 1)

        self.game.validate_input(["3", "3"], 1)
        arr = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 1]])
        for i in range(0, len(self.game.field)):
            for j in range(0, len(self.game.field)):
                self.assertEqual(self.game.field[i][j], arr[i][j])

        with self.assertRaises(InputError):
            self.game.validate_input(["3", "3"], 1)

        self.game = TicTacGame("M", "N", 6)
        with self.assertRaises(InputError):
            self.game.validate_input(["7", "6"], 1)

    def test_check_winner(self):
        # row
        self.game.field = np.array([[1, 1, 1], [2, 1, 2], [1, 2, 2]])
        self.assertEqual(self.game.check_winner(), "player1")
        # column
        self.game.field = np.array([[2, 1, 1], [2, 1, 2], [2, 2, 1]])
        self.assertEqual(self.game.check_winner(), "player2")
        # diagonal
        self.game.field = np.array([[2, 1, 1], [2, 1, 2], [1, 2, 1]])
        self.assertEqual(self.game.check_winner(), "player1")
        # diagonal
        self.game.field = np.array([[2, 1, 1], [1, 2, 2], [1, 1, 2]])
        self.assertEqual(self.game.check_winner(), "player2")
        # end of game
        self.game.field = np.array([[2, 1, 1], [1, 1, 2], [2, 2, 1]])
        self.assertEqual(self.game.check_winner(), "End of game")

    def test_validate_player_names(self):
        self.game = TicTacGame("player", "player")
        self.assertRaises(InputError)


if __name__ == "__main__":
    unittest.main()
