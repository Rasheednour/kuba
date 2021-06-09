# Author: Rasheed Mohammed
# Date: 09/06/2021
# Description: Write a class named KubaGame that initiates a board game called Kuba.


import copy


class Player:
    """
    Represents a player in the game.
    """
    def __init__(self, player_info):
        """
        Creates a player object, with private data members
        that store the player's name, play color ("W" or "B").
        and captured marbles (both red marbles and the opponent's marbles).
        :param player_info: A tuple with a player's name and play color.
        :return: None
        """
        # Player's name is the first value in the tuple.
        self._name = player_info[0]
        # Player color is the second value in the tuple.
        self._play_color = player_info[1]
        # captured marbles keeps track of captured red marbles and the opponent's-
        # marbles which the player knocked off the board.
        self._captured_marbles = {"R": 0, "OPPONENT": 0}

    def get_name(self):
        """
        Returns the player's name.
        """
        return self._name

    def get_captured_marbles(self):
        """
        Returns a dictionary of the marbles captured by the player
        for both the red marbles and the opponent's marbles.
        """
        return self._captured_marbles

    def get_play_color(self):
        """
        Returns the player's play color defined when a KubaGame is created.
        """
        return self._play_color

    def capture_marble(self, marble_color):
        """
        Adds a marble which was knocked off the board to captured_marbles.
        :param marble_color: Takes the marble color as parameter and increases
                             count of red marbles in captured_marbles if marble is red,
                             or opponent's marbles if marble_color is the opponent's.
        """
        # Add a Marble object to the player's dictionary of captured_marbles.
        if marble_color != self._play_color:
            # If the captured marble is red, add under the "R" key.
            if marble_color == "R":
                self._captured_marbles["R"] += 1
            # if captured marble is the opponent's, add the marble under the "OPPONENT" key.
            else:
                self._captured_marbles["OPPONENT"] += 1

    def __repr__(self):
        """
        Represents a player object by displaying its name.
        """
        return self._name


class Marble:
    """
    Represents a marble in the board.
    """
    def __init__(self, marble_color, coordinates):
        """
        Creates a marble object with private data members
        that store the marble's color, coordinates on the board,
        and status (inside board or captured).
        :param marble_color: The marble's color (red: "R", white: "W", or black: "B")
        :param coordinates: Marble coordinates inside board, a tuple of x,y coordinates.
        """
        self._color = marble_color
        self._coordinates = coordinates

    def get_coordinates(self):
        """
        Returns the marble's coordinates.
        :return: A tuple of x and y coordinates.
        """
        return self._coordinates

    def get_color(self):
        """
        Returns the marble's color.
        :return: Marble's color ('W', 'B', or 'R')
        """
        return self._color

    def set_coordinates(self, new_coordinates):
        """
        Sets new coordinates for the marble according to movement in the board.
        :param new_coordinates: A tuple of x and y coordinates.
        :return: None
        """
        self._coordinates = new_coordinates

    def __repr__(self):
        """
        Represents a Marble object by displaying its name.
        """
        return self._color


class KubaGame:
    """
    Represents a Kuba game.
    """

    def __init__(self, player_1, player_2):
        """
        Creates a new Kuba game, with private data members-
        that store the board, initiate the board, store the current turn,
        the winner, the players, and each player's last move.
        :param player_1: player 1 information, a tuple of the player's name and play color.
        :param player_2: player 2 information, a tuple of the player's name and play color.
        """
        # The game board, a dictionary with keys that represent x/y coordinates (tuples)
        # and values that store Marble objects on those coordinates, or empty spaces "X"
        self._board = {}
        # Call the initiate_board method that builds the board when a new game is created.
        self.initiate_board()
        # initiate current player turn to None.
        self._current_turn = None
        # initiate the winner to None.
        self._winner = None
        # create the Player objects from player information provided when KubaGame is created.
        self._player_1 = Player(player_1)
        self._player_2 = Player(player_2)
        # store deep copies of self._board that represent the latest board state before a player makes a move.
        self._board_history = copy.deepcopy(self._board)

    def initiate_board(self):
        """
        Initiates the game board before the game starts,
        by placing 8 white marbles, 8 black marbles, and 13 red marbles
        into their designated starting locations on the board.
        :return: None
        """
        # the outer for loop iterates through rows.
        for row_number in range(0, 7):
            # the inner for loop iterates through columns.
            for column_number in range(0, 7):
                # position represents the x/y coordinate of a square in the board.
                position = (row_number, column_number)
                # zones where red, white, and black marbles reside, are hardcoded below.
                white_zone = [(0, 0), (0, 1), (1, 0), (1, 1), (5, 5), (5, 6), (6, 5), (6, 6)]
                black_zone = [(0, 5), (0, 6), (1, 5), (1, 6), (5, 0), (5, 1), (6, 0), (6, 1)]
                red_zone = [(1, 3), (2, 2), (2, 3), (2, 4), (3, 1), (3, 2), (3, 3), (3, 4),
                            (3, 5), (4, 2), (4, 3), (4, 4), (5, 3)]

                # add a new Marble objects in their designated zones in the board,
                # otherwise, add empty spaces represented by an "X".
                if position in white_zone:
                    self._board[position] = Marble("W", position)
                elif position in black_zone:
                    self._board[position] = Marble("B", position)
                elif position in red_zone:
                    self._board[position] = Marble("R", position)
                else:
                    self._board[position] = "X"

    def get_current_turn(self):
        """
        Returns a Player object for the player who's going to play next.
        :return: A player object.
        """

        if self._current_turn is None:
            return None
        else:
            return str(self._current_turn)

    def get_player_from_name(self, player_name):
        """
        Returns the player object with the provided name.
        :param player_name: A player's name to be provided in return for the Player
                            object associated with that name, or None otherwise.
        :return: A player object.
        """
        player_1 = self._player_1
        player_2 = self._player_2

        if player_1.get_name() == player_name:

            return player_1

        elif player_2.get_name() == player_name:

            return player_2

        return None

    def is_move_legal(self, player, coordinates, push_direction):
        """
        Checks  if the player is making a valid play.
        Returns False in the following cases:
        1. It's not the player's turn to play.
        2. The player name does not match the players on record.
        3. The game has already been won.
        4. The coordinates are invalid (outside the board).
        5. The player is attempting to push an empty space.
        6. The player is attempting to push the opponent's marble.
        7. The player is attempting to directly push a red marble.
        8. The player is attempting to push their own marble but it's
           blocked from behind by another marble in the same pushing direction.
        :param player: The Player object who's playing now.
        :param coordinates: The pushing coordinates.
        :param push_direction: Direction of pushing ("F", "B", "R", or "L")
        :return: False if the player's game is invalid, or True otherwise.
        """
        # extract row and column numbers from the provided coordinates.
        row_number = coordinates[0]
        column_number = coordinates[1]

        # initiate the opponent to player as None.
        opponent = None

        # Calculate the opponent Player object to be used later in validation.
        if player == self._player_1:

            opponent = self._player_2

        else:

            opponent = self._player_1

        # Return False if the player is not a valid player.
        if not player:

            return False

        # return False if game is already won.
        if self._winner:

            return False

        # return False if the provided moving coordinates are outside the board's bounds.
        if coordinates[0] > 6 or coordinates[0] < 0 or coordinates[1] > 6 or coordinates[1] < 0:

            return False

        # return False if the player is attempting to push an empty space.
        if self._board[coordinates] == "X":

            return False

        # return False if the player is attempting to directly push a red marble.
        if self._board[coordinates].get_color() == "R":

            return False

        # return False if the player is attempting to push the opponent's marble.
        if self._board[coordinates].get_color() == opponent.get_play_color():

            return False

        # return false if it's not the player's turn to play and it's not the start of the game.
        if self._current_turn != player and self._current_turn is not None:

            return False

        # if all the above conditions are passed, proceed to validate the player's move below.
        # validate "forward" moving plays.
        if push_direction == "F":

            # if the player is pushing a marble from the bottom most edge of the board forward, the play is valid.
            if row_number + 1 == 7:

                return True

            # the move is invalid if the marble the player is moving is preceded-
            # by another marble in the same direction.
            if self._board[(row_number + 1, column_number)] != "X":

                return False

            return True

        # validate "downward or bottom" moving plays.
        if push_direction == "B":

            # if the player is pushing a marble from the top most edge of the board downward, the play is valid.
            if row_number - 1 == -1:

                return True

            # the move is invalid if the marble the player is moving is preceded-
            # by another marble in the same direction, instead of an empty space.
            if self._board[(row_number - 1, column_number)] != "X":

                return False

            # otherwise, the play is valid.
            return True

        # validate plays moving marbles to the right side.
        if push_direction == "R":

            # if the player is pushing a marble from the right most edge of the board to the left, the play is valid.
            if column_number - 1 == -1:
                return True

            # the move is invalid if the marble the player is moving is preceded-
            # by another marble in the same direction, instead of an empty space.
            if self._board[(row_number, column_number - 1)] != "X":

                return False

            # otherwise, the play is valid.
            return True

        # validate plays moving marbles to the left side.
        if push_direction == "L":

            # if the player is pushing a marble from the left most edge of the board to the right, the play is valid.
            if column_number + 1 == 7:
                return True

            # the move is invalid if the marble the player is moving is preceded-
            # by another marble in the same direction, instead of an empty space.
            if self._board[(row_number, column_number + 1)] != "X":

                return False

            # otherwise, the play is valid.
            return True

    def get_marble_set(self, coordinates, push_direction):
        """
        Returns the row of marbles the player is attempting to push.
        The function reads the pushing coordinates and direction, and
        iterates through the board starting from the pushing coordinates
        and in the specified direction, saving all consecutive marbles in the row
        in a list.
        :param coordinates: Pushing coordinates
        :param push_direction: Pushing direction.
        :return: The list of marbles the player is attempting to push.
        """

        # create a list to store the list of consecutive marbles affected by the move.
        marble_set = []

        # extract row and column number information from the provided coordinates.
        row_number = coordinates[0]
        column_number = coordinates[1]

        if push_direction == "F":

            # if moving from outside the board, return an empty list.
            if row_number < 0:
                return marble_set

            else:
                # keep adding Marble objects to the list starting from the marble at
                # the provided coordinates, until an empty space is encountered or we've reached
                # the end of the line.
                while self._board[(row_number, column_number)] != "X":
                    marble_set.append(self._board[(row_number, column_number)])
                    row_number -= 1

                    if row_number < 0:
                        break

                # return the created list of marbles, which were stored consecutively in the provided direction.
                return marble_set

        # use the same logic above for the other directions below.

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

    def push_marbles(self, marbles_to_push, push_direction, player, board):
        """
        Pushes a list of consecutive marbles across the board in a the specified direction
        by the player by incrementing/decrementing each marble's x or y coordinates according
        to the pushing direction. Also saves the board's state before and after push in history,
        to check if the player is attempting to undo the last player's move.
        :param marbles_to_push: The list of marbles to pushed in the specified direction.
        :param push_direction: The pushing direction ("F": Forward, "B": Backward, "R": Right, "L": Left)
        :param player: The player object whose playing now.
        :param board: The board object (dictionary) to be modified.
        :return: False if a push results in the player knocking their own marbles off board,
                 or True if the move is successful.
        """
        # create a deep copy of the list of marbles_to_push.
        # reverse the new list, this way we move marbles starting from the marble at the end.
        reversed_list = copy.deepcopy(marbles_to_push)
        reversed_list.reverse()

        if push_direction == "F":

            # iterate through reversed list of marbles.
            for marble in reversed_list:

                # get each marble's current position on the board.
                current_position = marble.get_coordinates()

                # get each marble's current row and column numbers.
                current_row_num = current_position[0]
                current_col_num = current_position[1]

                # decrement/increment the marble's row or column number depending on the direction
                # in order to shift the marble's position (forward, bottom, right side or left side).
                new_position = (current_row_num - 1, current_col_num)

                # detect if the marble's new position is outside the board.
                if new_position[0] < 0:

                    # detect if the player is attempting to push their own marble off board, return False if they are.
                    if marble.get_color() == player.get_play_color():
                        return False

                    # otherwise, add the marble the player's list of captured marble,
                    player.capture_marble(marble.get_color())

                    # after a marble's position is shifted, replace its older location with an empty space.
                    if len(marbles_to_push) == 1:
                        board[current_position] = "X"

                # add the marble to the new position and set the moved marble's coordinates
                # to the new position coordinated and replace the older position with an empty space.
                board[new_position] = marble
                marble.set_coordinates(new_position)
                board[current_position] = "X"

        # the same logic above applies to the rest of the directions below.

        if push_direction == "B":

            for marble in reversed_list:

                current_position = marble.get_coordinates()
                current_row_num = current_position[0]
                current_col_num = current_position[1]
                new_position = (current_row_num + 1, current_col_num)
                if new_position[0] > 6:

                    if marble.get_color() == player.get_play_color():
                        return False

                    player.capture_marble(marble.get_color())

                    if len(marbles_to_push) == 1:
                        board[current_position] = "X"

                board[new_position] = marble
                marble.set_coordinates(new_position)
                board[current_position] = "X"

        if push_direction == "R":

            for marble in reversed_list:

                current_position = marble.get_coordinates()
                current_row_num = current_position[0]
                current_col_num = current_position[1]
                new_position = (current_row_num, current_col_num + 1)

                if new_position[1] > 6:

                    if marble.get_color() == player.get_play_color():
                        return False

                    player.capture_marble(marble.get_color())

                    if len(marbles_to_push) == 1:
                        board[current_position] = "X"

                board[new_position] = marble
                marble.set_coordinates(new_position)
                board[current_position] = "X"

        if push_direction == "L":

            for marble in reversed_list:

                current_position = marble.get_coordinates()
                current_row_num = current_position[0]
                current_col_num = current_position[1]
                new_position = (current_row_num, current_col_num - 1)

                if new_position[1] < 0:

                    if marble.get_color() == player.get_play_color():
                        return False

                    player.capture_marble(marble.get_color())

                    if len(marbles_to_push) == 1:
                        board[current_position] = "X"

                board[new_position] = marble
                marble.set_coordinates(new_position)
                board[current_position] = "X"

        return True

    def calculate_win(self, player):
        """
        Calculates if a player's move results in a win in one of two scenarios:
        1. The player captured 7 of the 13 red marbles.
        2. The player knocked all opponent's 8 marbles off board.
        :param player: A player object whose currently playing.
        :return: Sets self._winner to player if player has won the game.
        """

        # iterate through player's list of captured marble to find out
        # if they captured enough red or opponent marbles to win the game.
        if player.get_captured_marbles()["R"] == 7 or player.get_captured_marbles()["OPPONENT"] == 8:
            self._winner = player

    def check_undo(self, marbles_to_push, push_direction, player):
        """
        Performs a test push on a duplicate board and checks if the player is attempting
        to undo the opponent's previous move in that test board, resulting in a repeated board state.
        :param marbles_to_push: set of marbles to be pushed
        :param push_direction: pushing direction
        :param player: the player object attempting to push the marbles.
        :return: False if the player's move is undoing the opponent's move and True otherwise.
        """

        # first create deep copies of the player object and the current board.
        test_player = copy.deepcopy(player)
        test_board = copy.deepcopy(self._board)

        # second, perform a test push on the test board to see if the board
        # matches the last board we have in history (meaning the previous player's move was undone).
        test_push = self.push_marbles(marbles_to_push, push_direction, test_player, test_board)

        # if the test push is unsuccessful, return False.
        if not test_push:
            return False

        # create two lists to consecutively store the marbles in the two boards we're trying to compare.
        # the two boards we're trying to see if they match are the test board we modified above,
        # and the last board we have in history which represents the board state before the previous
        # player made their move.

        marble_list_1 = []
        marble_list_2 = []

        # because we're comparing two boards (dictionaries) which are deep copies of self._board,
        # then even if they completely match each other, they wont be equal if we use the == operator
        # on them, because the key values inside each dictionary store Marble objects rather than
        # primitive data types like strings.
        # therefore, a for loop is implemented below to extract string data of each marble object
        # in each board, representing each marble's color, and storing these strings in the designated lists above.

        # extract string data from the test board we modified above.
        for coordinate in test_board:

            if test_board[coordinate] == "X":
                marble_list_1.append("X")
            else:
                marble_list_1.append(test_board[coordinate].get_color())

        # extract string data from the latest board we have in history.
        for coordinate in self._board_history:
            if self._board_history[coordinate] == "X":
                marble_list_2.append("X")
            else:
                marble_list_2.append(self._board_history[coordinate].get_color())

        # now perform the equality check to see if the player's move will be
        # undoing the previous player's move resulting in a repeated board state.
        # if so return False.
        if marble_list_1 == marble_list_2:
            return False

        # at this point, the player's move is completely valid
        # and the method returns True to allow make_move to implement the actual move,
        # and change the original board of KubaGame.
        return True

    def make_move(self, player_name, coordinates, push_direction):
        """
        -Checks if the player's move is valid by calling is_move_legal, returns False if it isn't and proceeds otherwise
        - checks if the player is undoing the opponent's previous move, by calling check_undo.
        -If it's the first move in the game, sets current_turn to the player.
        -Obtains the row of marbles the player is attempting to push by calling get_marble_set
        -Returns false if the player is undoing the last player's move, proceeds otherwise.
        -Pushes the marbles.
        -Calculates a winning play by calling calculate_win
        -If the move is successful, Switches the turn to the next player and returns True.
        :param player_name: Name of the playing making the move.
        :param coordinates: Pushing coordinates (a tuple of x and y coordinates on the board).
        :param push_direction: The direction the player is attempting to push the marbles towards.
        :return: True if the move is successful, False otherwise.
        """

        # get the Player object from the provided player name.
        player = self.get_player_from_name(player_name)

        # call is_move_legal to perform validation tests.
        # return False if is_move_legal returns false.
        if not self.is_move_legal(player, coordinates, push_direction):
            return False

        # detect if this is the first move of the game, and set the current turn to the current player.
        if self._current_turn is None:
            self._current_turn = player

        # get the consecutive marble list that will be affected by the move.
        marbles_to_push = self.get_marble_set(coordinates, push_direction)

        # create a deep copy of the marble list above, to be used
        # in a test board move to validate if the player is not
        # undoing the previous player's move.
        test_marbles = copy.deepcopy(marbles_to_push)
        # if the player is indeed undoing the last player's move, return False.

        if not self.check_undo(test_marbles, push_direction, player):
            return False

        # at this point, all validation tests are passed,
        # and the player is allowed to make the actual move on the board.
        # but first, a deep copy of the current board will be added to board history
        # to be used in future validation tests to check if the next player
        # will be undoing the current player's move.
        self._board_history = copy.deepcopy(self._board)

        # now start moving the marbles at the provided coordinates towards the provided direction,
        # by calling push_marbles.
        push_marbles = self.push_marbles(marbles_to_push, push_direction, player, self._board)

        # if the attempted move cause an error in push_marbles, return False.
        if not push_marbles:
            return False

        # at this point, the move is successful and the main board is modified.
        # end make_move by first detecting if the move above cause the player to win.

        # call calculate_move.
        self.calculate_win(player)

        # change the current turn to refer to the next player.
        if self._current_turn == self._player_1:
            self._current_turn = self._player_2

        else:
            self._current_turn = self._player_1

        # return True signaling that make_move is successful.
        return True

    def get_winner(self):
        """
        Returns the player who won the game, returns None otherwise.
        :return: The player that won the game, None otherwise.
        """
        if self._winner is None:
            return None

        else:
            return str(self._winner)

    def get_captured(self, player_name):
        """
        Takes a player's name and returns the count of red marbles captured by that player.
        :param player_name: Player's name.
        :return: A count of red marbles captured by the player. Returns "Player not found"
                 is the inputted name is not a valid player.
        """
        player_1 = self._player_1
        player_2 = self._player_2

        if player_1.get_name() == player_name:
            return player_1.get_captured_marbles()["R"]

        elif player_2.get_name() == player_name:
            return player_2.get_captured_marbles()["R"]

        # if the provided player name is invalid.
        else:

            return "Player not found!"

    def get_marble(self, cell_coords):
        """
        Returns a marble object from the board based on the coordinates in the parameter cell_coords
        The player object is returned as "R", "W", "B" according to the marble's color, or "X" if the space is empty.
        :param cell_coords: Board's cell coordinates to receive marble information from.
        :return: The marble in the specified coordinates on the board.
        """
        return str(self._board[cell_coords])

    def get_marble_count(self):
        """
        Returns the count of marbles currently inside the board, arranged by color. ("W", "B", "R")
        :return: a tuple of three counts for the count of white, black, and red marbles in this order.
        """

        # initialize three counters for the count of white,black, and red marbles.
        white_count = 0
        black_count = 0
        red_count = 0

        # iterate through squares in the board and increment the above counters whenever
        # a marble is encountered.
        for square in self._board:

            # if a square isn't empty and its coordinates are within the board bounds.
            if self._board[square] != "X"\
                    and square[0] <= 6\
                    and square[0] >= 0\
                    and square[1] <= 6\
                    and square[1] >= 0:

                # increment the counters according to the color of the encountered marble.
                if self._board[square].get_color() == "W":
                    white_count += 1
                elif self._board[square].get_color() == "B":
                    black_count += 1
                else:
                    red_count += 1

        # return the three counters as a tuple.
        return white_count, black_count, red_count

    def display_board(self):
        """
        Returns a string that resembles and the self._board dictionary.
        The string provides a proper representation for how the board looks like and helps with debugging.
        :return: A string that resembles a board shape with marbles inside, the data is taken from self._board
        """

        # initialize the string object as a empty string.
        board = ""

        # iterate through the self._board dictionary and start building the string object above.
        # squares are represented by brackets ([]) and the data inside each coordinate tuple in the
        # board dictionary is added inside the brackets.
        for row_number in range(0, 7):
            for column_number in range(0, 7):
                position = (row_number, column_number)
                if self._board[position] == "X":
                    board += "[ ]"
                else:
                    board += "[" + self._board[position].get_color() + "]"
                if column_number == 6:
                    board += "\n"

        # the end result is a string object that looks like a board with marbles/empty spaces inside.
        return board
