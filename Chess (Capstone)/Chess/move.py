from .constants import *


class Move:
    """
    The init takes the first clicked square and second clicked square and stores the starting and ending coords.
    It then stores the piece that moved and piece that was captured based on that starting and ending coords.
    """

    def __init__(self, startSq, endSq, board, enpassant=False, castle=False):
        self.start_row = startSq[0]
        self.start_col = startSq[1]
        self.end_row = endSq[0]
        self.end_col = endSq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.pawn_promotion = self.is_pawn_promotion()  # call pawn_promotion to determine if a pawn made it to end
        self.enpassant_move = enpassant  # set an enpassant move was made
        self.castling_move = castle  # set a castling move was made
        if enpassant:
            self.piece_captured = self.is_enpassant_capture()  # update piece captured for enpassant
        # creates a unique id like a hash function
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    def __eq__(self, other):
        """
        overriding the equal's method to the method
        """
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        """
        Returns a string of a move's start and end square in chess notation e.g. 'E2 E4'
        To be sent to the server in multiplayer to update opponent
        """
        string = COL_TO_NOTATION[self.start_col] + ROW_TO_NOTATION[self.start_row]  # start square
        string += ''
        string += COL_TO_NOTATION[self.end_col] + ROW_TO_NOTATION[self.end_row]  # end square
        return string

    def get_move_legible(self):
        """
        Returns a human legible move to be used when logging the move in the UI
        """
        # ID: piece Moves From chess n to square
        string = str(self.move_id) + ': '
        string += PIECES[self.piece_moved]
        string += ' Moves From '
        string += COL_TO_NOTATION[self.start_col] + ROW_TO_NOTATION[self.start_row]
        string += ' to '
        string += COL_TO_NOTATION[self.end_col] + ROW_TO_NOTATION[self.end_row]

        # if piece was captured, add it to the string
        if self.piece_captured:
            string += ' Capturing '
            string += PIECES[self.piece_captured]

        return string

    def get_piece_moved(self):
        """
        Returns the piece that moved
        """
        return self.piece_moved

    def get_piece_captured(self):
        """
        Returns the name of the captured piece
        """
        return self.piece_captured

    def is_pawn_promotion(self):
        """
        determines if a piece moved should be a pawn promotion
        """
        if (self.piece_moved == 'wP' and self.end_row == 0) or (self.piece_moved == 'bP' and self.end_row == 7):
            return True
        return False

    def is_enpassant_capture(self):
        """
        return the enpassant piece captured
        """
        if self.piece_moved == 'wP':
            return 'bP'
        return 'wP'
