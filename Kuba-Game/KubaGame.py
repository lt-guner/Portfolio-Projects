# Author: Timur Guner
# Date: 2021-06-09
# Description: The portfolio project is a Kuba game. The game runs like the rules of a regular Kuba game but the player
#              only gets one turn even when a red marble is captured.

import copy

class KubaGame():
    """
    The KubaGame() class creates an object based on the rules of Kuba. It first creates a game board by using a list
    within a list to mimic the layout of Kuba. In order to initialize the setup, player names and marble color need to
    be passed as tuples. Once the players and colors are assigned, any player can make the first move. All moves are
    made in the method make_move and that method has three sudmethods; first_move, player_one_move, and player_two_move.
    If it’s the first move in the game, then any player can initial it. After that it rotates between player_one_move
    and player_two_move based on whose turn it is. There are five get methods for this class, get_current_turn,
    get_winner, get_captured, get_marble, and get_marble_count. Each of those methods have individual docstrings
    """

    def __init__(self, tuple_a, tuple_b):
        """
        The init method takes two parameters; two tuples, each containing the player’s name and the marble color.It has
        private data members _player_one, _player_two, _player_one_color, _player_two_color, _player_one_captures,
        _player_two_captures, _winner, _player_turn, _kuba_board, _kuba_board_previous, _kuba_board_attempted_move and
        _move_count. The data members _player_one, _player_two, _player_one_color, _player_two_color are assigned by
        the tuples that are passed. _player_one_captures and _player_two_captures are counts of the red marbles each
        player has captured._winner is populated with the player name based on capturing 7 red marbles, the opponent has
        no valid moves, or the opponent has no marbles left._kuba_board sets up the board based on the Kuba design.
        _kuba_board_previous is a deepcopy of the previous board's marble position, while _kuba_board_attempted_move is
        a temporary deepcopy of _kuba_board to see if the move is valid compared to _kuba_board_previous. Finally,
        _move_count keeps track of the number of moves.
        """

        self._player_one = tuple_a[0]
        self._player_two = tuple_b[0]
        self._player_one_color = tuple_a[1]
        self._player_two_color = tuple_b[1]
        self._player_one_captures = 0
        self._player_two_captures = 0
        self._winner = None
        self._player_turn = None
        self._kuba_board = [['W','W','X','X','X','B','B'],
                            ['W','W','X','R','X','B','B'],
                            ['X','X','R','R','R','X','X'],
                            ['X','R','R','R','R','R','X'],
                            ['X','X','R','R','R','X','X'],
                            ['B','B','X','R','X','W','W'],
                            ['B','B','X','X','X','W','W']]
        self._kuba_board_previous = copy.deepcopy(self._kuba_board)
        self._kuba_board_move_attempt = copy.deepcopy(self._kuba_board)
        self._move_count = 0

    def make_move(self, player, coord, direction):
        """
        The make_move method takes three parameters; player is the player’s name, coord which is the location of the
        marble as a tuple, and the direction of the move. There are three submethods for this method; first_move,
        move_player_one, and move_player_two. The first_move method only triggers if no player has made a move yet.
        Once the first move is made then the other two submethods are triggered based on the player turn. Finally, the
        method checks if the player is the winner if it captured its 7 red marbles, if it knocked out the last of the
        opponent's marbles, or gave the opponent no
        valid moves.
        """
        # if there is a winner, no move moves can be made
        if self._winner is not None:
            return False

        # -----------------------------FIRST MOVE----------------------------------------------------------------------
        # first move
        if self._move_count == 0:
            firstmove = self.first_move(player, coord, direction)
            if firstmove == True:
                self._move_count += 1
            return firstmove

        # ----------------------------PLAYER ONE TURN------------------------------------------------------------------
        # call move_player_one
        if player == self._player_turn and player == self._player_one:
            player_one = self.move_player_one(coord, direction)

            # add move count
            if player_one == True:
                self._move_count += 1

            # check if player one won by getting 7 red marbles
            if self._player_one_captures == 7:
                self._winner = self._player_one

            # check if player one won by removing all opponent's marbles
            player_two_marbles = 0

            for x in range(0, 7):
                for y in range(0, 7):
                    if self._kuba_board[x][y] == self._player_two_color:
                        player_two_marbles += 1

            if player_two_marbles == 0:
                self._winner = self._player_one

            # check if player one won by giving the opponent no options to move
            edge_marbles_player_two = 0

            # check if any are in the first row
            for x in range(0,7):
                if self._kuba_board[0][x] == self._player_two_color:
                    edge_marbles_player_two += 1

            # check if any are in the first column
            for x in range(0,7):
                if self._kuba_board[x][0] == self._player_two_color:
                    edge_marbles_player_two += 1

            # check if any are in the last row
            for x in range(0,7):
                if self._kuba_board[6][x] == self._player_two_color:
                    edge_marbles_player_two += 1

            # check if any are in the last column
            for x in range(0,7):
                if self._kuba_board[x][6] == self._player_two_color:
                    edge_marbles_player_two += 1

            player_two_free_marbles = 1

            # if no marbles are on the edges then we used this portion to make check if all marbles are trapped
            if edge_marbles_player_two == 0:
                player_two_free_marbles = 0        # used to declare outside the loop
                for r in range(1,6):
                    for c in range(1,6):
                        if self._kuba_board == self._player_two_color:
                            if self._kuba_board[r+1][c] == 'X' or self._kuba_board[r][c+1] == 'X' or self._kuba_board[r-1][c] == 'X' or self._kuba_board[r][c-1] == 'X':
                                player_two_free_marbles += 1

            # declare winner if all marbles are trapped
            if player_two_free_marbles == 0:
                self._winner = self._player_one

            return player_one

        # -----------------------------------PLAYER TWO TURN-----------------------------------------------------------
        # call move_player_two
        if player == self._player_turn and player == self._player_two:
            player_two = self.move_player_two(coord, direction)

            # add move count
            if player_two == True:
                self._move_count += 1

            # check if player two won by getting 7 red marbles
            if self._player_two_captures == 7:
                self._winner = self._player_two

            # check if player one won by removing all opponent's marbles
            player_one_marbles = 0

            for x in range(0, 7):
                for y in range(0, 7):
                    if self._kuba_board[x][y] == self._player_one_color:
                        player_one_marbles += 1

            if player_one_marbles == 0:
                self._winner = self._player_two

            # check if player one won by giving the opponent no options to move
            edge_marbles_player_one = 0

            # check if any are in the first row
            for x in range(0,7):
                if self._kuba_board[0][x] == self._player_one_color:
                    edge_marbles_player_one += 1

            # check if any are in the first column
            for x in range(0,7):
                if self._kuba_board[x][0] == self._player_one_color:
                    edge_marbles_player_one += 1

            # check if any are in the last row
            for x in range(0,7):
                if self._kuba_board[6][x] == self._player_one_color:
                    edge_marbles_player_one += 1

            # check if any are in the last column
            for x in range(0,7):
                if self._kuba_board[x][6] == self._player_one_color:
                    edge_marbles_player_one += 1

            player_one_free_marbles = 1  # used to declare outside the loop

            # if no marbles are on the edges then we used this portion to make check if all marbles are trapped
            if edge_marbles_player_one == 0:
                player_one_free_marbles = 0    # assume no marbles are free
                for r in range(1,6):
                    for c in range(1,6):
                        if self._kuba_board == self._player_one_color:
                            if self._kuba_board[r+1][c] == 'X' or self._kuba_board[r][c+1] == 'X' or self._kuba_board[r-1][c] == 'X' or self._kuba_board[r][c-1] == 'X':
                                player_one_free_marbles += 1

            # declare winner if all marbles are trapped
            if player_one_free_marbles == 0:
                self._winner = self._player_two

            return player_two

        return False

    def first_move(self, player, coord, direction):
        """
        The first_move method is triggered when a player makes the first move in the game. It first sets the
        _kuba_board_previous as deepcopy of the current_kuba_board. Once that is complete, the player can make the first
        move based on the limited amount of first moves allowed. Once complete, _player_turn is set to the next player.
        Since the first move is limited to only moves pieces on the edges and no possible way to win, the move checks
        are hardcoded and no checks are made to see if there is a winner. For the first move a player can only make a
        move from pieces on the edges.
        """

        # start by creating a deep copy of the current board to save as the previous board
        self._kuba_board_previous = copy.deepcopy(self._kuba_board)

        # assign the coordinates that was passed
        row_coord = coord[0]
        column_coord = coord[1]

        # return false if the coords are out of range
        if row_coord < 0 or row_coord > 6 or column_coord < 0 or column_coord > 6:
            return False

        # if the move is forward and the row the piece is moving from is 6
        if row_coord == 6:
            if direction == 'F' and (row_coord-1) != -1 and (row_coord-2) != -1 and self._kuba_board[row_coord][column_coord] == 'W' and self._player_one == player:
                self._kuba_board[row_coord][column_coord] = 'X'
                self._kuba_board[row_coord-1][column_coord] = 'W'
                self._kuba_board[row_coord-2][column_coord] = 'W'
                if player == self._player_one:
                    self._player_turn = self._player_two
                else:
                    self._player_turn = self._player_one
                return True
            elif direction == 'F' and (row_coord-1) != -1 and (row_coord-2) != -1 and self._kuba_board[row_coord][column_coord] == 'B' and self._player_two == player:
                self._kuba_board[row_coord][column_coord] = 'X'
                self._kuba_board[row_coord - 1][column_coord] = 'B'
                self._kuba_board[row_coord - 2][column_coord] = 'B'
                if player == self._player_one:
                    self._player_turn = self._player_two
                else:
                    self._player_turn = self._player_one
                return True

        # if move is right and the column the piece is moving from is 0
        if column_coord == 0:
            if direction == 'R' and (column_coord+1) != 7 and (column_coord+2) != 7 and self._kuba_board[row_coord][column_coord] == 'W' and self._player_one == player:
                self._kuba_board[row_coord][column_coord] = 'X'
                self._kuba_board[row_coord][column_coord+1] = 'W'
                self._kuba_board[row_coord][column_coord+2] = 'W'
                if player == self._player_one:
                    self._player_turn = self._player_two
                else:
                    self._player_turn = self._player_one
                return True
            elif direction == 'R' and (column_coord+1) != 7 and (column_coord+2) != 7 and self._kuba_board[row_coord][column_coord] == 'B' and self._player_two == player:
                self._kuba_board[row_coord][column_coord] = 'X'
                self._kuba_board[row_coord][column_coord+1] = 'B'
                self._kuba_board[row_coord][column_coord+2] = 'B'
                if player == self._player_one:
                    self._player_turn = self._player_two
                else:
                    self._player_turn = self._player_one
                return True

        # if move is backwards and the row the piece is moving from is 0
        if row_coord == 0:
            if direction == 'B' and (row_coord+1) != 7 and (row_coord+2) != 7 and self._kuba_board[row_coord][column_coord] == 'W' and self._player_one == player:
                self._kuba_board[row_coord][column_coord] = 'X'
                self._kuba_board[row_coord+1][column_coord] = 'W'
                self._kuba_board[row_coord+2][column_coord] = 'W'
                if player == self._player_one:
                    self._player_turn = self._player_two
                else:
                    self._player_turn = self._player_one
                return True
            elif direction == 'B' and (row_coord+1) != 7 and (row_coord+2) != 7 and self._kuba_board[row_coord][column_coord] == 'B' and self._player_two == player:
                self._kuba_board[row_coord][column_coord] = ''
                self._kuba_board[row_coord+1][column_coord] = 'B'
                self._kuba_board[row_coord+2][column_coord] = 'B'
                if player == self._player_one:
                    self._player_turn = self._player_two
                else:
                    self._player_turn = self._player_one
                return True

        # if move is left and the column the piece is moving from is 6
        if column_coord == 6:
            if direction == 'L' and (column_coord-1) != -1 and (column_coord-2) != -1 and self._kuba_board[row_coord][column_coord] == 'W' and self._player_one == player:
                self._kuba_board[row_coord][column_coord] = 'X'
                self._kuba_board[row_coord][column_coord-1] = 'W'
                self._kuba_board[row_coord][column_coord-2] = 'W'
                if player == self._player_one:
                    self._player_turn = self._player_two
                else:
                    self._player_turn = self._player_one
                return True
            elif direction == 'L' and (column_coord-1) != -1 and (column_coord-2) != -1 and self._kuba_board[row_coord][column_coord] == 'B' and self._player_two == player:
                self._kuba_board[row_coord][column_coord] = 'X'
                self._kuba_board[row_coord][column_coord-1] = 'B'
                self._kuba_board[row_coord][column_coord-2] = 'B'
                if player == self._player_one:
                    self._player_turn = self._player_two
                else:
                    self._player_turn = self._player_one
                return True
        return False

    def move_player_one(self, coord, direction):
        """
        The move_player_one method takes parameters, coord and direction, inherited from the make_move. It then
        determines if the given coords match the color of the marbles for player_one.The method then does a series of
        checks to make sure the move is valid based on the rules of Kuba.This is done by using a deepcopy of _kuba_board
        as _kuba_board_move_attempt, which allows the program to move the pieces to check if it is a valid move without
        changing the actual _kuba_board.If everything passes, _kuba_board_previous is a deepcopy of _kubaboard and
        _kuba_board is a deepcopy of _kuba_board_attempt_move. It then sets the _player_turn to _player_two
        """

        # deepcopy playboard of current board into attempted moves
        self._kuba_board_move_attempt = copy.deepcopy(self._kuba_board)

        # assign the tuples to row and column coordinates
        row_coord = coord[0]
        column_coord = coord[1]

        # used to keep track of valid move and captured red marble
        exit_tracker = 0
        red_marble = 0

        # return false if the coords are out of range
        if row_coord < 0 or row_coord > 6 or column_coord < 0 or column_coord > 6:
            return False

        # move sure that this the correct players turn
        if self._kuba_board_move_attempt[row_coord][column_coord] == self._player_one_color:

            # ----------------------------------------Right Move-------------------------------------------------------

            # process and validate move right
            if direction == 'R':

                # see if the players ball would be pushed off by own ball, if so move is invalid
                break_counter = False
                if self._kuba_board_move_attempt[row_coord][6] == self._player_one_color:
                    for c in range(column_coord,7):
                        if self._kuba_board_move_attempt[row_coord][c] == 'X':
                            break_counter = True
                    if break_counter == False:
                        return False

                # if the last ball is not player_one and cannot be pushed off find out if any blanks to the right of t
                # he move
                column_tracker = 7
                for c in range(column_coord,7):
                    if self._kuba_board_move_attempt[row_coord][c] == 'X':
                        column_tracker = c
                        break

                # first see if the ball is at the edge and if so treat it like it has X behind it
                if column_coord == 0:

                    # set the current position and next position to begin pushing
                    current_marble = self._kuba_board_move_attempt[row_coord][column_coord]
                    place_holder = self._kuba_board_move_attempt[row_coord][column_coord+1]

                    # for loop updates all the spots by pushing the current spot into the next slot and so for
                    # it also keeps track if a red marble is pushed off
                    for c in range (column_coord, column_tracker):
                        try:
                            if self._kuba_board_move_attempt[row_coord][c+1] == 'R' and c == 5:
                                red_marble = 1
                            self._kuba_board_move_attempt[row_coord][c+1] = current_marble
                            current_marble = place_holder
                        except:
                            continue
                        try:
                            place_holder = self._kuba_board_move_attempt[row_coord][c+2]
                        except:
                            continue

                    # assign X to the original spot
                    self._kuba_board_move_attempt[row_coord][column_coord] = 'X'

                    # used to alert tha all possible moves were made to the copied board
                    exit_tracker = 1

                # if its not on the edge check to make sure that the opposite direction of the move is X
                elif self._kuba_board_move_attempt[row_coord][column_coord-1] == 'X':

                    # set the current position and next position to begin pushing
                    current_marble = self._kuba_board_move_attempt[row_coord][column_coord]
                    place_holder = self._kuba_board_move_attempt[row_coord][column_coord+1]

                    # for loop updates all the spots by pushing the current spot into the next slot and so for
                    # it also keeps track if a red marble is pushed off
                    for c in range(column_coord, column_tracker):
                        try:
                            if self._kuba_board_move_attempt[row_coord][c+1] == 'R' and c == 5:
                                red_marble = 1
                            self._kuba_board_move_attempt[row_coord][c + 1] = current_marble
                            current_marble = place_holder
                        except:
                            continue
                        try:
                            place_holder = self._kuba_board_move_attempt[row_coord][c + 2]
                        except:
                            continue

                    # assign X to the original spot
                    self._kuba_board_move_attempt[row_coord][column_coord] = 'X'

                    # used to alert tha all possible moves were made to the copied board
                    exit_tracker = 1

                # check if the move is not undoing the previous move and if its not, update captures if needed and
                # change the copied boards and players turn
                if self._kuba_board_previous != self._kuba_board_move_attempt and exit_tracker == 1:
                    if red_marble == 1:
                        self._player_one_captures += 1
                    self._kuba_board_previous = copy.deepcopy(self._kuba_board)
                    self._kuba_board = copy.deepcopy(self._kuba_board_move_attempt)
                    self._player_turn = self._player_two
                    return True

            #-----------------------------------Forward Move------------------------------------------------------------

            # process and validate move forward
            if direction == 'F':

                # see if the players ball would be pushed off by own ball, if so move is invalid
                break_counter = False
                if self._kuba_board_move_attempt[0][column_coord] == self._player_one_color:
                    for r in range(row_coord, -1, -1):
                        if self._kuba_board_move_attempt[r][column_coord] == 'X':
                            break_counter = True
                    if break_counter == False:
                        return False

                # if the last ball is not player_one and cannot be pushed off find out if any blanks to the front of
                # the move
                row_tracker = -1
                for r in range(row_coord, -1, -1):
                    if self._kuba_board_move_attempt[r][column_coord] == 'X':
                        row_tracker = r
                        break

                # first see if the ball is at the edge and if so treat it like it has X behind it
                if row_coord == 6:

                    # set the current position and next position to begin pushing
                    current_marble = self._kuba_board_move_attempt[row_coord][column_coord]
                    place_holder = self._kuba_board_move_attempt[row_coord-1][column_coord]

                    # for loop updates all the spots by pushing the current spot into the next slot and so for
                    # it also keeps track if a red marble is pushed off
                    for r in range(row_coord, row_tracker, -1):
                        try:
                            if self._kuba_board_move_attempt[r-1][column_coord] == 'R' and r == 1:
                                red_marble = 1
                            if r > 0:       # list can have -1 so we don't want to overwrite what is in position 6
                                self._kuba_board_move_attempt[r-1][column_coord] = current_marble
                                current_marble = place_holder
                        except:
                            continue
                        try:
                            if r > 0:       # list can have -1 so we don't want to overwrite what is in position 6
                                place_holder = self._kuba_board_move_attempt[r-2][column_coord]
                        except:
                            continue

                    # assign X to the original spot
                    self._kuba_board_move_attempt[row_coord][column_coord] = 'X'

                    # used to alert tha all possible moves were made to the copied board
                    exit_tracker = 1

                # if its not on the edge check to make sure that the opposite direction of the move is X
                elif self._kuba_board_move_attempt[row_coord+1][column_coord] == 'X':

                    # set the current position and next position to begin pushing
                    current_marble = self._kuba_board_move_attempt[row_coord][column_coord]
                    place_holder = self._kuba_board_move_attempt[row_coord-1][column_coord]

                    # for loop updates all the spots by pushing the current spot into the next slot and so for
                    # it also keeps track if a red marble is pushed off
                    for r in range(row_coord, row_tracker, -1):
                        try:
                            if self._kuba_board_move_attempt[r-1][column_coord] == 'R' and r == 1:
                                red_marble = 1
                            if r > 0:       # list can have -1 so we don't want to overwrite what is in position 6
                                self._kuba_board_move_attempt[r-1][column_coord] = current_marble
                                current_marble = place_holder
                        except:
                            continue
                        try:
                            if r > 0:       # list can have -1 so we don't want to overwrite what is in position 6
                                place_holder = self._kuba_board_move_attempt[r-2][column_coord]
                        except:
                            continue

                    # assign X to the original spot
                    self._kuba_board_move_attempt[row_coord][column_coord] = 'X'

                    # used to alert tha all possible moves were made to the copied board
                    exit_tracker = 1

                # check if the move is not undoing the previous move and if its not update captures if needed and change
                # the copied boards
                if self._kuba_board_previous != self._kuba_board_move_attempt and exit_tracker == 1:
                    if red_marble == 1:
                        self._player_one_captures += 1
                    self._kuba_board_previous = copy.deepcopy(self._kuba_board)
                    self._kuba_board = copy.deepcopy(self._kuba_board_move_attempt)
                    self._player_turn = self._player_two
                    return True

            # ---------------------------------LEFT MOVE---------------------------------------------------------------

            # process and validate move Left
            if direction == 'L':

                # see if the players ball would be pushed off by own ball, if so move is invalid
                break_counter = False
                if self._kuba_board_move_attempt[row_coord][0] == self._player_one_color:
                    for c in range(column_coord, -1, -1):
                        if self._kuba_board_move_attempt[row_coord][c] == 'X':
                            break_counter = True
                    if break_counter == False:
                        return False

                # if the last ball is not player_one and cannot be pushed off find out if any X are to the left
                column_tracker = -1
                for c in range(column_coord, -1, -1):
                    if self._kuba_board_move_attempt[row_coord][c] == 'X':
                        column_tracker = c
                        break

                # first see if the ball is at the edge and if so treat back like its empty
                if column_coord == 6:

                    # set the current position and next position to begin pushing
                    current_marble = self._kuba_board_move_attempt[row_coord][column_coord]
                    place_holder = self._kuba_board_move_attempt[row_coord][column_coord-1]

                    # for loop updates all the spots by pushing the current spot into the next slot and so for
                    # it also keeps track if a red marble is pushed off
                    for c in range (column_coord, column_tracker, -1):
                        try:
                            if self._kuba_board_move_attempt[row_coord][c-1] == 'R' and c == 1:
                                red_marble = 1
                            if c > 0:       # list can have -1 so we don't want to overwrite what is in position 6
                                self._kuba_board_move_attempt[row_coord][c-1] = current_marble
                                current_marble = place_holder
                        except:
                            continue
                        try:
                            if c > 0:       # list can have -1 so we don't want to overwrite what is in position 6
                                place_holder = self._kuba_board_move_attempt[row_coord][c-2]
                        except:
                            continue

                    # assign X to the original spot
                    self._kuba_board_move_attempt[row_coord][column_coord] = 'X'

                    # used to alert tha all possible moves were made to the copied board
                    exit_tracker = 1

                # if its not on the edge check to make sure that the opposite direction of the move is X
                elif self._kuba_board_move_attempt[row_coord][column_coord+1] == 'X':

                    # set the current position and next position to begin pushing
                    current_marble = self._kuba_board_move_attempt[row_coord][column_coord]
                    place_holder = self._kuba_board_move_attempt[row_coord][column_coord-1]

                    # for loop updates all the spots by pushing the current spot into the next slot and so for
                    # it also keeps track if a red marble is pushed off
                    for c in range(column_coord, column_tracker, -1):
                        try:
                            if self._kuba_board_move_attempt[row_coord][c-1] == 'R' and c == 1:
                                red_marble = 1
                            if c > 0:          # list can have -1 so we don't want to overwrite what is in position 6
                                self._kuba_board_move_attempt[row_coord][c-1] = current_marble
                                current_marble = place_holder
                        except:
                            continue
                        try:
                            if c > 0:          # list can have -1 so we don't want to overwrite what is in position 6
                                place_holder = self._kuba_board_move_attempt[row_coord][c-2]
                        except:
                            continue

                    # assign X to the original spot
                    self._kuba_board_move_attempt[row_coord][column_coord] = 'X'

                    # used to alert tha all possible moves were made to the copied board
                    exit_tracker = 1

                # check if the move is not undoing the previous move and if its not update captures if needed and change
                # the copied boards and update player turn
                if self._kuba_board_previous != self._kuba_board_move_attempt and exit_tracker == 1:
                    if red_marble == 1:
                        self._player_one_captures += 1
                    self._kuba_board_previous = copy.deepcopy(self._kuba_board)
                    self._kuba_board = copy.deepcopy(self._kuba_board_move_attempt)
                    self._player_turn = self._player_two
                    return True

            #--------------------------------------BACKWARDS MOVE-------------------------------------------------------

            # process and validate move backwards
            if direction == 'B':

                # see if the players ball would be pushed off by own ball, if so move is invalid
                break_counter = False
                if self._kuba_board_move_attempt[6][column_coord] == self._player_one_color:
                    for r in range(row_coord,7):
                        if self._kuba_board_move_attempt[r][column_coord] == 'X':
                            break_counter = True
                    if break_counter == False:
                        return False

                # if the last ball is not player_one and cannot be pushed off find out if any blanks to the right of the
                # of the move
                row_tracker = 7
                for r in range(row_coord, 7):
                    if self._kuba_board_move_attempt[r][column_coord] == 'X':
                        row_tracker = r
                        break

                # first see if the ball is at the edge and if so treat back like its empty
                if row_coord == 0:

                    # set the current position and next position to begin pushing
                    current_marble = self._kuba_board_move_attempt[row_coord][column_coord]
                    place_holder = self._kuba_board_move_attempt[row_coord+1][column_coord]

                    # for loop updates all the spots by pushing the current spot into the next slot and so for
                    # it also keeps track if a red marble is pushed off
                    for r in range(row_coord, row_tracker):
                        try:
                            if self._kuba_board_move_attempt[r+1][column_coord] == 'R' and r == 5:
                                red_marble = 1
                            self._kuba_board_move_attempt[r+1][column_coord] = current_marble
                            current_marble = place_holder
                        except:
                            continue
                        try:
                            place_holder = self._kuba_board_move_attempt[r+2][column_coord]
                        except:
                            continue

                    # assign X to the original spot
                    self._kuba_board_move_attempt[row_coord][column_coord] = 'X'

                    # used to alert tha all possible moves were made to the copied board
                    exit_tracker = 1

                # if its not on the edge check to make sure that the opposite direction of the move is X
                elif self._kuba_board_move_attempt[row_coord-1][column_coord] == 'X':

                    # set the current position and next position to begin pushing
                    current_marble = self._kuba_board_move_attempt[row_coord][column_coord]
                    place_holder = self._kuba_board_move_attempt[row_coord+1][column_coord]

                    # for loop updates all the spots by pushing the current spot into the next slot and so for
                    # it also keeps track if a red marble is pushed off
                    for r in range(row_coord, row_tracker):
                        try:
                            if self._kuba_board_move_attempt[r+1][column_coord] == 'R' and r == 5:
                                red_marble = 1
                            self._kuba_board_move_attempt[r+1][column_coord] = current_marble
                            current_marble = place_holder
                        except:
                            continue
                        try:
                            place_holder = self._kuba_board_move_attempt[r+2][column_coord]
                        except:
                            continue

                    # assign X to the original spot
                    self._kuba_board_move_attempt[row_coord][column_coord] = 'X'

                    # used to alert tha all possible moves were made to the copied board
                    exit_tracker = 1

                # check if the move is not undoing the previous move and if its not update captures if needed and change
                # the copied boards
                if self._kuba_board_previous != self._kuba_board_move_attempt and exit_tracker == 1:
                    if red_marble == 1:
                        self._player_one_captures += 1
                    self._kuba_board_previous = copy.deepcopy(self._kuba_board)
                    self._kuba_board = copy.deepcopy(self._kuba_board_move_attempt)
                    self._player_turn = self._player_two
                    return True

        return False

    def move_player_two(self, coord, direction):
        """
        The move_player_two method takes parameters, coord and direction, inherited from the make_move. It then
        determines if the given coords match the color of the marbles for player_two.The method then does a series of
        checks to make sure the move is valid based on the rules of Kuba.This is done by using a deepcopy of _kuba_board
        as _kuba_board_move_attempt, which allows the program to move the pieces to check if it is a valid move without
        changing the actual _kuba_board.If everything passes, _kuba_board_previous is a deepcopy of _kubaboard and
        _kuba_board is a deepcopy of _kuba_board_attempt_move. It then sets the _player_turn to _player_one
        """


        # deepcopy playboard of current board into attempted moves
        self._kuba_board_move_attempt = copy.deepcopy(self._kuba_board)

        # assign the tuples to row and column coordinates
        row_coord = coord[0]
        column_coord = coord[1]

        # used to keep track of valid move and captured red marble
        exit_tracker = 0
        red_marble = 0

        # return false if the coords are out of range
        if row_coord < 0 or row_coord > 6 or column_coord < 0 or column_coord > 6:
            return False

        # move sure that this the correct players turn
        if self._kuba_board_move_attempt[row_coord][column_coord] == self._player_two_color:

            # ----------------------------------------Right Move-------------------------------------------------------

            # process and validate move right
            if direction == 'R':

                # see if the players ball would be pushed off by own ball, if so move is invalid
                break_counter = False
                if self._kuba_board_move_attempt[row_coord][6] == self._player_two_color:
                    for c in range(column_coord,7):
                        if self._kuba_board_move_attempt[row_coord][c] == 'X':
                            break_counter = True
                    if break_counter == False:
                        return False

                # if the last ball is not player_two and cannot be pushed off find out if any blanks to the right of t
                # he move
                column_tracker = 7
                for c in range(column_coord,7):
                    if self._kuba_board_move_attempt[row_coord][c] == 'X':
                        column_tracker = c
                        break

                # first see if the ball is at the edge and if so treat it like it has X behind it
                if column_coord == 0:

                    # set the current position and next position to begin pushing
                    current_marble = self._kuba_board_move_attempt[row_coord][column_coord]
                    place_holder = self._kuba_board_move_attempt[row_coord][column_coord+1]

                    # for loop updates all the spots by pushing the current spot into the next slot and so for
                    # it also keeps track if a red marble is pushed off
                    for c in range (column_coord, column_tracker):
                        try:
                            if self._kuba_board_move_attempt[row_coord][c+1] == 'R' and c == 5:
                                red_marble = 1
                            self._kuba_board_move_attempt[row_coord][c+1] = current_marble
                            current_marble = place_holder
                        except:
                            continue
                        try:
                            place_holder = self._kuba_board_move_attempt[row_coord][c+2]
                        except:
                            continue

                    # assign X to the original spot
                    self._kuba_board_move_attempt[row_coord][column_coord] = 'X'

                    # used to alert tha all possible moves were made to the copied board
                    exit_tracker = 1

                # if its not on the edge check to make sure that the opposite direction of the move is X
                elif self._kuba_board_move_attempt[row_coord][column_coord-1] == 'X':

                    # set the current position and next position to begin pushing
                    current_marble = self._kuba_board_move_attempt[row_coord][column_coord]
                    place_holder = self._kuba_board_move_attempt[row_coord][column_coord+1]

                    # for loop updates all the spots by pushing the current spot into the next slot and so for
                    # it also keeps track if a red marble is pushed off
                    for c in range(column_coord, column_tracker):
                        try:
                            if self._kuba_board_move_attempt[row_coord][c+1] == 'R' and c == 5:
                                red_marble = 1
                            self._kuba_board_move_attempt[row_coord][c + 1] = current_marble
                            current_marble = place_holder
                        except:
                            continue
                        try:
                            place_holder = self._kuba_board_move_attempt[row_coord][c + 2]
                        except:
                            continue

                    # assign X to the original spot
                    self._kuba_board_move_attempt[row_coord][column_coord] = 'X'

                    # used to alert tha all possible moves were made to the copied board
                    exit_tracker = 1

                # check if the move is not undoing the previous move and if its not, update captures if needed and
                # change the copied boards and players turn
                if self._kuba_board_previous != self._kuba_board_move_attempt and exit_tracker == 1:
                    if red_marble == 1:
                        self._player_two_captures += 1
                    self._kuba_board_previous = copy.deepcopy(self._kuba_board)
                    self._kuba_board = copy.deepcopy(self._kuba_board_move_attempt)
                    self._player_turn = self._player_one
                    return True

            #-----------------------------------Forward Move------------------------------------------------------------

            # process and validate move forward
            if direction == 'F':

                # see if the players ball would be pushed off by own ball, if so move is invalid
                break_counter = False
                if self._kuba_board_move_attempt[0][column_coord] == self._player_two_color:
                    for r in range(row_coord, -1, -1):
                        if self._kuba_board_move_attempt[r][column_coord] == 'X':
                            break_counter = True
                    if break_counter == False:
                        return False

                # if the last ball is not player_two and cannot be pushed off find out if any blanks to the front of
                # the move
                row_tracker = -1
                for r in range(row_coord, -1, -1):
                    if self._kuba_board_move_attempt[r][column_coord] == 'X':
                        row_tracker = r
                        break

                # first see if the ball is at the edge and if so treat it like it has X behind it
                if row_coord == 6:

                    # set the current position and next position to begin pushing
                    current_marble = self._kuba_board_move_attempt[row_coord][column_coord]
                    place_holder = self._kuba_board_move_attempt[row_coord-1][column_coord]

                    # for loop updates all the spots by pushing the current spot into the next slot and so for
                    # it also keeps track if a red marble is pushed off
                    for r in range(row_coord, row_tracker, -1):
                        try:
                            if self._kuba_board_move_attempt[r-1][column_coord] == 'R' and r == 1:
                                red_marble = 1
                            if r > 0:         # list can have -1 so we don't want to overwrite what is in position 6
                                self._kuba_board_move_attempt[r-1][column_coord] = current_marble
                                current_marble = place_holder
                        except:
                            continue
                        try:
                            if r > 0:         # list can have -1 so we don't want to overwrite what is in position 6
                                place_holder = self._kuba_board_move_attempt[r-2][column_coord]
                        except:
                            continue

                    # assign X to the original spot
                    self._kuba_board_move_attempt[row_coord][column_coord] = 'X'

                    # used to alert tha all possible moves were made to the copied board
                    exit_tracker = 1

                # if its not on the edge check to make sure that the opposite direction of the move is X
                elif self._kuba_board_move_attempt[row_coord+1][column_coord] == 'X':

                    # set the current position and next position to begin pushing
                    current_marble = self._kuba_board_move_attempt[row_coord][column_coord]
                    place_holder = self._kuba_board_move_attempt[row_coord-1][column_coord]

                    # for loop updates all the spots by pushing the current spot into the next slot and so for
                    # it also keeps track if a red marble is pushed off
                    for r in range(row_coord, row_tracker, -1):
                        try:
                            if self._kuba_board_move_attempt[r-1][column_coord] == 'R' and r == 1:
                                red_marble = 1
                            if r > 0:         # list can have -1 so we don't want to overwrite what is in position 6
                                self._kuba_board_move_attempt[r-1][column_coord] = current_marble
                                current_marble = place_holder
                        except:
                            continue
                        try:
                            if r > 0:         # list can have -1 so we don't want to overwrite what is in position 6
                                place_holder = self._kuba_board_move_attempt[r-2][column_coord]
                        except:
                            continue

                    # assign X to the original spot
                    self._kuba_board_move_attempt[row_coord][column_coord] = 'X'

                    # used to alert tha all possible moves were made to the copied board
                    exit_tracker = 1

                # check if the move is not undoing the previous move and if its not update captures if needed and change
                # the copied boards
                if self._kuba_board_previous != self._kuba_board_move_attempt and exit_tracker == 1:
                    if red_marble == 1:
                        self._player_two_captures += 1
                    self._kuba_board_previous = copy.deepcopy(self._kuba_board)
                    self._kuba_board = copy.deepcopy(self._kuba_board_move_attempt)
                    self._player_turn = self._player_one
                    return True

            # ---------------------------------LEFT MOVE---------------------------------------------------------------

            # process and validate move Left
            if direction == 'L':

                # see if the players ball would be pushed off by own ball, if so move is invalid
                break_counter = False
                if self._kuba_board_move_attempt[row_coord][0] == self._player_two_color:
                    for c in range(column_coord, -1, -1):
                        if self._kuba_board_move_attempt[row_coord][c] == 'X':
                            break_counter = True
                    if break_counter == False:
                        return False

                # if the last ball is not player_two and cannot be pushed off find out if any X are to the left
                column_tracker = -1
                for c in range(column_coord, -1, -1):
                    if self._kuba_board_move_attempt[row_coord][c] == 'X':
                        column_tracker = c
                        break

                # first see if the ball is at the edge and if so treat back like its empty
                if column_coord == 6:

                    # set the current position and next position to begin pushing
                    current_marble = self._kuba_board_move_attempt[row_coord][column_coord]
                    place_holder = self._kuba_board_move_attempt[row_coord][column_coord-1]

                    # for loop updates all the spots by pushing the current spot into the next slot and so for
                    # it also keeps track if a red marble is pushed off
                    for c in range (column_coord, column_tracker, -1):
                        try:
                            if self._kuba_board_move_attempt[row_coord][c-1] == 'R' and c == 1:
                                red_marble = 1
                            if c > 0:         # list can have -1 so we don't want to overwrite what is in position 6
                                self._kuba_board_move_attempt[row_coord][c-1] = current_marble
                                current_marble = place_holder
                        except:
                            continue
                        try:
                            if c > 0:         # list can have -1 so we don't want to overwrite what is in position 6
                                place_holder = self._kuba_board_move_attempt[row_coord][c-2]
                        except:
                            continue

                    # assign X to the original spot
                    self._kuba_board_move_attempt[row_coord][column_coord] = 'X'

                    # used to alert tha all possible moves were made to the copied board
                    exit_tracker = 1

                # if its not on the edge check to make sure that the opposite direction of the move is X
                elif self._kuba_board_move_attempt[row_coord][column_coord+1] == 'X':

                    # set the current position and next position to begin pushing
                    current_marble = self._kuba_board_move_attempt[row_coord][column_coord]
                    place_holder = self._kuba_board_move_attempt[row_coord][column_coord-1]

                    # for loop updates all the spots by pushing the current spot into the next slot and so for
                    # it also keeps track if a red marble is pushed off
                    for c in range(column_coord, column_tracker, -1):
                        try:
                            if self._kuba_board_move_attempt[row_coord][c-1] == 'R' and c == 1:
                                red_marble = 1
                            if c > 0:         # list can have -1 so we don't want to overwrite what is in position 6
                                self._kuba_board_move_attempt[row_coord][c-1] = current_marble
                                current_marble = place_holder
                        except:
                            continue
                        try:
                            if c > 0:         # list can have -1 so we don't want to overwrite what is in position 6
                                place_holder = self._kuba_board_move_attempt[row_coord][c-2]
                        except:
                            continue

                    # assign X to the original spot
                    self._kuba_board_move_attempt[row_coord][column_coord] = 'X'

                    # used to alert tha all possible moves were made to the copied board
                    exit_tracker = 1

                # check if the move is not undoing the previous move and if its not update captures if needed and change
                # the copied boards and update player turn
                if self._kuba_board_previous != self._kuba_board_move_attempt and exit_tracker == 1:
                    if red_marble == 1:
                        self._player_two_captures += 1
                    self._kuba_board_previous = copy.deepcopy(self._kuba_board)
                    self._kuba_board = copy.deepcopy(self._kuba_board_move_attempt)
                    self._player_turn = self._player_one
                    return True

            #--------------------------------------BACKWARDS MOVE-------------------------------------------------------

            # process and validate move backwards
            if direction == 'B':

                # see if the players ball would be pushed off by own ball, if so move is invalid
                break_counter = False
                if self._kuba_board_move_attempt[6][column_coord] == self._player_two_color:
                    for r in range(row_coord,7):
                        if self._kuba_board_move_attempt[r][column_coord] == 'X':
                            break_counter = True
                    if break_counter == False:
                        return False

                # if the last ball is not player_two and cannot be pushed off find out if any blanks to the right of the
                # of the move
                row_tracker = 7
                for r in range(row_coord, 7):
                    if self._kuba_board_move_attempt[r][column_coord] == 'X':
                        row_tracker = r
                        break

                # first see if the ball is at the edge and if so treat back like its empty
                if row_coord == 0:

                    # set the current position and next position to begin pushing
                    current_marble = self._kuba_board_move_attempt[row_coord][column_coord]
                    place_holder = self._kuba_board_move_attempt[row_coord+1][column_coord]

                    # for loop updates all the spots by pushing the current spot into the next slot and so for
                    # it also keeps track if a red marble is pushed off
                    for r in range(row_coord, row_tracker):
                        try:
                            if self._kuba_board_move_attempt[r+1][column_coord] == 'R' and r == 5:
                                red_marble = 1
                            self._kuba_board_move_attempt[r+1][column_coord] = current_marble
                            current_marble = place_holder
                        except:
                            continue
                        try:
                            place_holder = self._kuba_board_move_attempt[r+2][column_coord]
                        except:
                            continue

                    # assign X to the original spot
                    self._kuba_board_move_attempt[row_coord][column_coord] = 'X'

                    # used to alert tha all possible moves were made to the copied board
                    exit_tracker = 1

                # if its not on the edge check to make sure that the opposite direction of the move is X
                elif self._kuba_board_move_attempt[row_coord-1][column_coord] == 'X':

                    # set the current position and next position to begin pushing
                    current_marble = self._kuba_board_move_attempt[row_coord][column_coord]
                    place_holder = self._kuba_board_move_attempt[row_coord+1][column_coord]

                    # for loop updates all the spots by pushing the current spot into the next slot and so for
                    # it also keeps track if a red marble is pushed off
                    for r in range(row_coord, row_tracker):
                        try:
                            if self._kuba_board_move_attempt[r+1][column_coord] == 'R' and r == 5:
                                red_marble = 1
                            self._kuba_board_move_attempt[r+1][column_coord] = current_marble
                            current_marble = place_holder
                        except:
                            continue
                        try:
                            place_holder = self._kuba_board_move_attempt[r+2][column_coord]
                        except:
                            continue

                    # assign X to the original spot
                    self._kuba_board_move_attempt[row_coord][column_coord] = 'X'

                    # used to alert tha all possible moves were made to the copied board
                    exit_tracker = 1

                # check if the move is not undoing the previous move and if its not update captures if needed and change
                # the copied boards
                if self._kuba_board_previous != self._kuba_board_move_attempt and exit_tracker == 1:
                    if red_marble == 1:
                        self._player_two_captures += 1
                    self._kuba_board_previous = copy.deepcopy(self._kuba_board)
                    self._kuba_board = copy.deepcopy(self._kuba_board_move_attempt)
                    self._player_turn = self._player_one
                    return True

        return False

    def get_current_turn(self):
        """
        returns the player turn
        """
        return self._player_turn

    def get_winner(self):
        """
        returns the winner
        """
        return self._winner

    def get_captured(self, player_name):
        """
        returns number of captured marbles
        """
        if player_name == self._player_one:
            return self._player_one_captures
        elif player_name == self._player_two:
            return self._player_two_captures

    def get_marble(self, coords):
        """
        returns the marble that is located at that position or X if there is no marble
        """
        return self._kuba_board[coords[0]][coords[1]]

    def get_marble_count(self):
        """
        returns the number of marbles of each color that are still on the board
        """

        # variables used to count the marbles left
        white_count = 0
        black_count = 0
        red_count = 0

        # nested for loops to count iterate thought the board and count the number of marbles
        for x in range(0,7):
            for y in range(0,7):
                if self._kuba_board[x][y] == "W":
                    white_count += 1
                if self._kuba_board[x][y] == "B":
                    black_count += 1
                if self._kuba_board[x][y] == "R":
                    red_count += 1

        # return a tuple
        return (white_count, black_count, red_count)

    def get_kuba_board(self):
        """
        returns the kuba_board
        """
        return self._kuba_board

def main():
    game = KubaGame(('PlayerA', 'W'), ('PlayerB', 'B'))
    print(game.get_marble_count())  # returns (8,8,13)
    print(game.get_captured('PlayerA'))  # returns 0
    print(game.get_current_turn())  # returns None
    print(game.get_winner())  # returns None

    print(game.make_move('PlayerA', (6, 6), 'F'))
    print(game.get_kuba_board())
    print(game.get_marble_count())
    print(game.make_move('PlayerB', (0, 6), 'B'))
    print(game.get_kuba_board())
    print(game.get_marble_count())

    print(game.make_move('PlayerA', (6, 5), 'F'))
    print(game.get_winner())
    print(game.get_kuba_board())
    print(game.get_marble_count())

if __name__ == '__main__':
    main()
