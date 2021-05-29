# Author: Rasheed Mohammed
# Date: 05/30/2021
# Description: Write a Kuba board game.

class Player:
    def __init__(self, player_info):
        self._name = player_info[0]
        self._play_color = player_info[1]
        self._captured_marbles = {"R": 0, "OPPONENT": 0}

    def get_name(self):
        return self._name

    def get_captured_marbles(self):
        return self._captured_marbles


    def __repr__(self):
        return self._name


class Marble:

    def __init__(self, marble_color, coordinates):
        self._color = marble_color
        self._coordinates = coordinates
        self._owner = None
        self._captor = None

    def get_coordinates(self):
        return self._coordinates

    def set_owner(self, player):
        self._owner = player

    def set_captor(self, player):
        self._captor = player

    def get_color(self):
        return self._color

    def __repr__(self):
        return self._color


class KubaGame:

    def __init__(self, player_1, player_2):
        self._board = {}
        self.initiate_board()
        self._current_turn = None
        self._winner = None
        self._player_1 = Player(player_1)
        self._player_2 = Player(player_2)

    def initiate_board(self):
        for row_number in range(0, 7):
            for column_number in range(0, 7):
                position = (row_number, column_number)
                white_zone = [(0, 0), (0, 1), (1, 0), (1, 1), (5, 5), (5, 6), (6, 5), (6, 6)]
                black_zone = [(0, 5), (0, 6), (1, 5), (1, 6), (5, 0), (5, 1), (6, 0), (6, 1)]
                red_zone = [(1, 3), (2, 2), (2, 3), (2, 4), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (4, 2), (4, 3), (4, 4), (5, 3)]
                if position in white_zone:
                    self._board[position] = Marble("W", position)
                elif position in black_zone:
                    self._board[position] = Marble("B", position)
                elif position in red_zone:
                    self._board[position] = Marble("R", position)
                else:
                    self._board[position] = "X"

    def get_current_turn(self):
        return self._current_turn

    def get_player_from_name(self, player_name):

        player_1 = self._player_1
        player_2 = self._player_2

        if player_1.get_name() == player_name:

            return player_1

        elif player_2.get_name() == player_name:

            return player_2

        return None

    def is_move_legal(self, player, coordinates, push_direction):

        row_number = coordinates[0]
        column_number = coordinates[1]

        if self._winner:

            return "Game is already won"

        if self._current_turn != player and self._current_turn is not None:

            return False

        if push_direction == "F":

            if self._board[(row_number + 1, column_number)]:

                return False

            return True

        elif push_direction == "B":

            if self._board[(row_number - 1, column_number)]:
                return False

            return True

        elif push_direction == "R":

            if self._board[(row_number, column_number - 1)]:
                return False

            return True
        elif push_direction == "L":

            if self._board[(row_number, column_number + 1)]:
                return False

            return True

        else:
            return "Invalid move!"

    def update_board(self, coordinates, push_direction):

        row_number = coordinates[0]
        column_number = coordinates[1]



    def update_winner(self):



    def make_move(self, player_name, coordinates, push_direction):

        player = self.get_player_from_name(player_name)

        if not player:

            return "Player is not found."

        if not self.is_move_legal(player, coordinates, push_direction):

            return "Invalid move!"

        if self._current_turn is None:

            self._current_turn = player












        else:
            if self._current_turn == self._player_1:
                self._current_turn = self._player_2

            else:
                self._current_turn = self._player_1








    def get_winner(self):
        return self._winner

    def get_captured(self, player_name):
        player_1 = self._player_1
        player_2 = self._player_2

        if player_1.get_name() == player_name:
            return player_1.get_captured_marbles()["R"]

        elif player_2.get_name() == player_name:
            return player_2.get_captured_marbles()["R"]

        else:

            return "Player not found!"

    def get_marble(self, cell_coords):
        pass

    def get_marble_count(self):

        count = [0, 0, 0]

        for square in self._board:

            if self._board[square] != "X":
                if self._board[square].get_color() == "W":
                    count[0] += 1
                elif self._board[square].get_color() == "B":
                    count[1] += 1
                else:
                    count[2] += 1
        return count[0], count[1], count[2]

    def display_board(self):
        board = ""
        for row_number in range(0, 7):
            for column_number in range(0, 7):
                position = (row_number, column_number)
                if self._board[position] == "X":
                    board += "[ ]"
                else:
                    board += "[" + self._board[position].get_color() + "]"
                if column_number == 6:
                    board += "\n"
        return board



game = KubaGame(("PLayer_1", "W"), ("Player_2", "B"))
print(game.display_board())
print(game.get_marble_count())
print(game.get_captured("Player_3"))