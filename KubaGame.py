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

    def get_play_color(self):

        return self._play_color

    def capture_marble(self, marble_color):

        if marble_color != self._play_color:
            if marble_color == "R":
                self._captured_marbles["R"] += 1
            else:
                self._captured_marbles["OPPONENT"] +=1

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

    def set_coordinates(self, new_coordinates):
        self._coordinates = new_coordinates

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
        self._past_move = ""

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
        opponent = None

        if player == self._player_1:

            opponent = self._player_2

        else:

            opponent = self._player_1

        if not player:
            return False

        if self._winner:

            return False

        if coordinates[0] > 6 or coordinates[0] < 0 or coordinates[1] > 6 or coordinates[1] < 0:

            return False

        if self._board[coordinates] == "X": # if attempting to push an empty square

            return False

        if self._board[coordinates].get_color() == "R": # if attempting to push a red marble

            return False

        if self._board[coordinates].get_color() == opponent.get_play_color(): # if attempting to push opponent's marble

            return False

        if self._current_turn != player and self._current_turn is not None: # if it's not player's turn to play
            print("here")

            return False

        if push_direction == "F":

            if row_number + 1 == 7:

                return True

            if self._board[(row_number + 1, column_number)] != "X":

                return False

            return True

        if push_direction == "B":

            if row_number - 1 == -1:

                return True

            if self._board[(row_number - 1, column_number)] != "X":

                return False

            return True

        if push_direction == "R":

            if column_number - 1 == -1:
                return True

            if self._board[(row_number, column_number - 1)] != "X":

                return False

            return True

        if push_direction == "L":

            if column_number + 1 == 7:
                return True

            if self._board[(row_number, column_number + 1)] != "X":

                return False

            return True






    def get_marble_set(self, coordinates, push_direction):
        # check case if pushing own marbles off board
        marble_set = []
        # first append first marble in line.
        row_number = coordinates[0]
        column_number = coordinates[1]

        if push_direction == "F":
            if row_number < 0:
                return marble_set
            else:
                while self._board[(row_number, column_number)] != "X":
                    marble_set.append(self._board[(row_number, column_number)])
                    row_number -= 1
                    if row_number < 0:
                        break
                return marble_set

        if push_direction == "B":

            if row_number > 6:
                return marble_set

            else:

                while self._board[(row_number, column_number)] != "X":

                    marble_set.append(self._board[(row_number, column_number)])
                    row_number += 1
                    if row_number > 6:
                        break

                return marble_set

        if push_direction == "R":

            if column_number > 6:
                return marble_set

            else:

                while self._board[(row_number, column_number)] != "X":

                    marble_set.append(self._board[(row_number, column_number)])
                    column_number += 1
                    if column_number > 6:
                        break

                return marble_set

        if push_direction == "L":

            if column_number < 0:
                return marble_set

            else:

                while self._board[(row_number, column_number)] != "X":
                    marble_set.append(self._board[(row_number, column_number)])
                    column_number -= 1
                    if column_number < 0:
                        break

                return marble_set

    def push_marbles(self, marbles_to_push, push_direction, player):

        reversed_list = list(marbles_to_push)
        reversed_list.reverse()
        if push_direction == "F":
            # iterate through reversed list
            for marble in reversed_list:
                #
                current_position = marble.get_coordinates()
                current_row_num = current_position[0]
                current_col_num = current_position[1]
                new_position = (current_row_num - 1, current_col_num)
                if new_position[0] < 0:
                    if marble.get_color() == player.get_play_color():
                        return False
                    player.capture_marble(marble.get_color())
                    if len(marbles_to_push) == 1:
                        self._board[current_position] = "X"

                self._board[new_position] = marble
                marble.set_coordinates(new_position)
                self._board[current_position] = "X"

        if push_direction == "B":
            # iterate through reversed list
            for marble in reversed_list:
                #
                current_position = marble.get_coordinates()
                current_row_num = current_position[0]
                current_col_num = current_position[1]
                new_position = (current_row_num + 1, current_col_num)
                if new_position[0] > 6:
                    if marble.get_color() == player.get_play_color():
                        return False
                    player.capture_marble(marble.get_color())
                    if len(marbles_to_push) == 1:
                        self._board[current_position] = "X"

                self._board[new_position] = marble
                marble.set_coordinates(new_position)
                self._board[current_position] = "X"

        if push_direction == "R":
            # iterate through reversed list
            for marble in reversed_list:
                #
                current_position = marble.get_coordinates()
                current_row_num = current_position[0]
                current_col_num = current_position[1]
                new_position = (current_row_num, current_col_num + 1)
                if new_position[1] > 6:
                    if marble.get_color() == player.get_play_color():
                        return False
                    player.capture_marble(marble.get_color())
                    if len(marbles_to_push) == 1:
                        self._board[current_position] = "X"

                self._board[new_position] = marble
                marble.set_coordinates(new_position)
                self._board[current_position] = "X"

        if push_direction == "L":
            # iterate through reversed list
            for marble in reversed_list:
                #
                current_position = marble.get_coordinates()
                current_row_num = current_position[0]
                current_col_num = current_position[1]
                new_position = (current_row_num, current_col_num - 1)
                if new_position[1] < 0:
                    if marble.get_color() == player.get_play_color():
                        return False
                    player.capture_marble(marble.get_color())
                    if len(marbles_to_push) == 1:
                        self._board[current_position] = "X"

                self._board[new_position] = marble
                marble.set_coordinates(new_position)
                self._board[current_position] = "X"

        if marbles_to_push[-1].get_color() != player.get_play_color():
            self._past_move = self.display_board()

        return True

    def calculate_win(self, player):

        if player.get_captured_marbles()["R"] == 7 or player.get_captured_marbles()["OPPONENT"] == 8:
            self._winner = player

    def make_move(self, player_name, coordinates, push_direction):
        player = self.get_player_from_name(player_name)
        marbles_to_push = []
        if not self.is_move_legal(player, coordinates, push_direction):
            return False
        if self._current_turn is None:

            self._current_turn = player

        marbles_to_push = self.get_marble_set(coordinates, push_direction)

        push_marbles = self.push_marbles(marbles_to_push, push_direction, player)

        if not push_marbles:
            return False

        if self.display_board() == self._past_move:
            return False

        self.calculate_win(player)

        if self._current_turn == self._player_1:

            self._current_turn = self._player_2

        else:
            self._current_turn = self._player_1


        return True

    def get_winner(self):

        return self._winner

    def get_captured(self, player_name):
        player_1 = self._player_1
        player_2 = self._player_2

        if player_1.get_name() == player_name:
            return player_1.get_captured_marbles()

        elif player_2.get_name() == player_name:
            return player_2.get_captured_marbles()

        else:

            return "Player not found!"

    def get_marble(self, cell_coords):

        return self._board[cell_coords]

    def get_marble_count(self):
        white_count = 0
        black_count = 0
        red_count = 0

        for square in self._board:

            if self._board[square] != "X"\
                    and square[0] <= 6\
                    and square[0] >= 0\
                    and square[1] <= 6\
                    and square[1] >= 0:

                if self._board[square].get_color() == "W":
                    white_count += 1
                elif self._board[square].get_color() == "B":
                    black_count += 1
                else:
                    red_count += 1

        return white_count, black_count, red_count

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


game = KubaGame(("Player_1", "W"), ("Player_2", "B"))
print(game.display_board())





game.make_move("Player_1", (6, 5), "F")

print(game.display_board())
game.make_move("Player_2", (6, 0), "F")
print(game.display_board())
print(game.get_current_turn())

game.make_move("Player_1", (5, 5), "F") # PLAYER TURN NOT CHANGING HERE FOR SOME REASON

print(game.display_board())
print(game.get_current_turn())
print(game.make_move("Player_2", (0, 5), "B"))
print(game.display_board())


# game.make_move("Player_2", (5, 0), "F")
# print(game.display_board())
# game.make_move("Player_1", (4, 5), "F")
# print(game.display_board())
# game.make_move("Player_2", (4, 0), "F")
# print(game.display_board())
# game.make_move("Player_1", (3, 5), "F")
# print(game.display_board())
# print(game.get_captured("Player_1"))
# game.make_move("Player_2", (3, 0), "F")
# print(game.display_board())
# game.make_move("Player_1", (2, 5), "F")
# print(game.display_board())
#
# game.make_move("Player_2", (0, 6), "L")
# print(game.display_board())
#
# game.make_move("Player_1", (1, 5), "R")
# print(game.display_board())

































