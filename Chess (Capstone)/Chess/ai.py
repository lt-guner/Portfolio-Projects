import random
from Chess.constants import *

# some sources
# https://www.freecodecamp.org/news/simple-chess-ai-step-by-step-1d55a9266977/
# https://www.chessprogramming.org/Simplified_Evaluation_Function
# https://en.wikipedia.org/wiki/Negamax


class ChessAI:

    def __init__(self):
        self.garbage = False

    def random_ai(self, moves):
        """
        takes a random number from 0 to last index of valid moves and returns an int to be used in choosing a move
        with the index of the returned int
        """
        return moves[random.randint(0, len(moves)-1)]

    def greedy_ai(self, moves, engine):
        """
        This AI will determine if a piece to capture should be made based on the value of the piece. It doesn't use in
        depth branching to valid if the move was the best choice, just determines the best possible move of the current
        state.
        """

        # set checkmate at best_score which is 1000 worst for black, black will score is best when negative
        best_score = CHECKMATE
        best_move = None

        # shuffle list so same move doesnt repeat if no captures
        random.shuffle(moves)

        # loop through list to determine the best move that can make
        for move in moves:

            # make the move and score the board based on the move
            engine.make_move(move)
            score = engine.get_material_score()

            if engine.is_in_check("WHITE", castling_row=engine.get_king_location()[0][0], 
                                  castling_col=engine.get_king_location()[0][1], castling=True):
                score = -CHECK

            # if neither checkmate, stalemate, check then make if score will get better for black
            if score < best_score:
                best_score = score
                best_move = move

            # undo the move
            engine.undo_move()
            
        # choose random if move is none
        if best_move is None:
            best_move = self.random_ai(moves)

        return best_move

    # ------------------------
    def negamax_alphabeta_ai(self, moves, engine):
        """
        This method uses the negamax algorithm and calls a helper function recursively. Negamax_ai takes the list of
        valid moves and the engine and calls the helper with moves, the engine, the depth for the amount of recursive
        calls, and turn_base multiplier 1 for white and -1 for black. The white player wants to get the most positive
        score while the black player tries to get the most negative score.
        """

        # create a global variable to be used between this and helper function and set to none
        global next_move
        next_move = None

        # shuffle the moves before making the negamax decision
        random.shuffle(moves)

        # call negamax
        self.negamax_alphabeta_helper(moves, engine, DEPTH, -CHECKMATE, CHECKMATE, -1)

        # if move is still none call random
        if next_move is None:
            next_move = self.random_ai(moves)

        return next_move

    def negamax_alphabeta_helper(self, moves, engine, depth, alpha, beta, turn_base):

        # let the negamax function know that the global variable is being used
        global next_move

        # base case which is to return the piece values by the turn_base multiplier
        if depth == 0:
            return turn_base * engine.get_material_score(hard_mode=True)

        # set max_score to -CHECKMATE, since using this we will be using a multiplier that will change the score to
        # all positives regardless of black or white turn
        max_score = -CHECKMATE

        # Iterate through the move list and make the move. Get the next set of valid moves for the other player and
        # call recursively to get the score of the opponent and score the move. This will end once the depth is reached
        # in all branches and the final score is returned tied to the global next_move. When alpha and beta meet, there
        # is no need to continue down that branch because we already found it
        for move in moves:
            engine.make_move(move)
            next_moves = engine.valid_moves()
            score = -self.negamax_alphabeta_helper(next_moves, engine, depth-1, -beta, -alpha, -turn_base)
            if score > max_score:
                max_score = score
                if depth == DEPTH:
                    next_move = move
            engine.undo_move()
            if max_score > alpha:
                alpha = max_score
            if alpha >= beta:
                break
        return max_score
    