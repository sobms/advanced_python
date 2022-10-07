import random
from Exceptions import InputError


class TicTacGame:
    d = {1: "X", 2: "O", 0: " "}

    def __init__(self, player1="player1", player2="player2", size=3):
        self.player1 = player1
        self.player2 = player2
        self.size = size
        self.markers = {1: self.player1, 2: self.player2}
        self.field = [[0 for _ in range(self.size)] for _ in range(self.size)]

    def show_board(self):
        print("+---" * len(self.field) + "+")
        for i in range(len(self.field)):
            for j in range(len(self.field)):
                print(f"| {self.d[self.field[i][j]]} ", end="")
            print("|")
            print("+---" * len(self.field) + "+")

    def players_move(self, player):
        print(f"Make your move {player}")
        while True:
            values = input().split(" ")
            marker = 2 if player == self.player2 else 1
            try:
                self.validate_input(values, marker)
                break
            except InputError as input_err:
                print(input_err)

    def validate_size(self, size):  # test
        if not size.isdigit():
            raise InputError("Wrong input!")
        if int(size) > 20 or int(size) < 3:
            raise InputError("Wrong input! Size more or less than acceptable value!")
        else:
            self.size = int(size)
            self.field = [[0 for _ in range(self.size)] for _ in range(self.size)]

    def validate_input(self, values, marker):  # test
        if len(values) != 2:
            raise InputError("Wrong input! Incorrect number of coordinates!")
        for i in values:
            if not i.isdigit() or int(i) > len(self.field) or int(i) < 1:
                raise InputError("Wrong input! Incorrect values.")

        x, y = values
        if self.field[int(y) - 1][int(x) - 1] != 0:
            raise InputError("Wrong input! Cell is already filled!")
        self.field[int(y) - 1][int(x) - 1] = marker

    def validate_player_names(self):
        if self.player1 == self.player2:
            raise InputError("Wrong input! Player names should be different!")

    def start_game_p_vs_p(self):
        while True:
            print("Please, type player1 name")
            self.player1 = input()
            print("Please, type player2 name")
            self.player2 = input()
            try:
                self.validate_player_names()
            except InputError as input_err:
                print(input_err)
            else:
                break
        self.markers = {1: self.player1, 2: self.player2}
        print("Please, enter size of field")
        while True:
            size = input()
            try:
                self.validate_size(size)
            except InputError as input_err:
                print(input_err)
            else:
                break

        player = self.player1 if random.randint(1, 2) == 1 else self.player2
        winner = False
        while not winner:
            self.players_move(player)
            self.show_board()
            player = self.player1 if player == self.player2 else self.player2
            winner = self.check_winner()
        if winner != "End of game":
            print(winner + " is WINNER!")
        else:
            print(winner)

    def check_winner(self):  # test
        winner = False
        dim = len(self.field)
        if all(all(row) for row in self.field):
            winner = "End of game"
        if (
            all(self.field[i][i] == self.field[0][0] for i in range(dim))
            and self.field[0][0] != 0
        ):
            winner = self.markers[self.field[0][0]]
        if (
            all(
                self.field[dim - 1 - i][i] == self.field[dim - 1][0] for i in range(dim)
            )
            and self.field[dim - 1][0] != 0
        ):
            winner = self.markers[self.field[dim - 1][0]]
        for i in range(dim):
            if (
                all(self.field[i][j] == self.field[i][0] for j in range(dim))
                and self.field[i][0] != 0
            ):  # i-masая строка
                winner = self.markers[self.field[i][0]]
            if (
                all(self.field[j][i] == self.field[0][i] for j in range(dim))
                and self.field[0][i] != 0
            ):  # i-ый столбец
                winner = self.markers[self.field[0][i]]
        return winner


if __name__ == "__main__":
    game = TicTacGame()
    game.start_game_p_vs_p()
