import copy

WHITE = 'w'
BLACK = 'b'
KING = 'K'

PIECES = {
    'wP': "White Pawn",
    'wR': 'White Rook',
    'wN': 'White Knight',
    'wB': 'White Bishop',
    'wQ': 'White Queen',
    'wK': 'White King',
    'bP': "Black Pawn",
    'bR': 'Black Rook',
    'bN': 'Black Knight',
    'bB': 'Black Bishop',
    'bQ': 'Black Queen',
    'bK': 'Black King'
}

COL_TO_NOTATION = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'}
ROW_TO_NOTATION = {0: '8', 1: '7', 2: '6', 3: '5', 4: '4', 5: '3', 6: '2', 7: '1'}

MOVE_DIRECTIONS = {
    'Q': [[0, 1], [0, -1], [-1, 0], [1, 0], [1, 1], [1, -1], [-1, -1], [-1, 1]],
    'B': [[1, 1], [1, -1], [-1, -1], [-1, 1]],
    'R': [[0, 1], [0, -1], [-1, 0], [1, 0]],
    "N": [[-2, 1], [-2, -1], [-1, -2], [-1, 2], [1, 2], [1, -2], [2, 1], [2, -1]],
    "K": [[0, 1], [0, -1], [-1, 0], [1, 0], [1, 1], [1, -1], [-1, -1], [-1, 1]]
}

CHECKMATE = 1000
CHECK = 100
STALEMATE = 0
DEPTH = 2

PIECE_STRENGTH = {
    'P': 1,
    'N': 3,
    'B': 3,
    'R': 5,
    'Q': 9,
    'K': 0
}

WHITE_PAWN_POS = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
                  [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
                  [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
                  [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
                  [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
                  [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
                  [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
                  [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

WHITE_KNIGHT_POS = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                    [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                    [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                    [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                    [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                    [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                    [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                    [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

WHITE_BISHOP_POS = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                    [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                    [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                    [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                    [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                    [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                    [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                    [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

WHITE_ROOK_POS = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                  [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
                  [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                  [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                  [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                  [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                  [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                  [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

WHITE_QUEEN_POS = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                   [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                   [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                   [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                   [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                   [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                   [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                   [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

BLACK_PAWN_POS = copy.deepcopy(WHITE_PAWN_POS)
BLACK_PAWN_POS.reverse()

BLACK_KNIGHT_POS = copy.deepcopy(WHITE_KNIGHT_POS)
BLACK_KNIGHT_POS.reverse()

BLACK_BISHOP_POS = copy.deepcopy(WHITE_BISHOP_POS)
BLACK_BISHOP_POS.reverse()

BLACK_ROOK_POS = copy.deepcopy(WHITE_ROOK_POS)
BLACK_ROOK_POS.reverse()

BLACK_QUEEN_POS = copy.deepcopy(WHITE_QUEEN_POS)
BLACK_QUEEN_POS.reverse()

PIECE_POSITIONAL_SCORE = {
    'wP': WHITE_PAWN_POS,
    'wR': WHITE_ROOK_POS,
    'wN': WHITE_KNIGHT_POS,
    'wB': WHITE_BISHOP_POS,
    'wQ': WHITE_QUEEN_POS,
    'bP': BLACK_PAWN_POS,
    'bR': BLACK_ROOK_POS,
    'bN': BLACK_KNIGHT_POS,
    'bB': BLACK_BISHOP_POS,
    'bQ': BLACK_QUEEN_POS,
}

BOARD_PIECE = ['wP', 'wR', 'wN', 'wB', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bQ']


def is_in_bounds(row, col):
    """
    Returns a boolean for whether a space coordinate is on the 8x8 board
    """
    # board is 8x8, stored as 2D list with indexes 0-7
    return 0 <= row <= 7 and 0 <= col <= 7
