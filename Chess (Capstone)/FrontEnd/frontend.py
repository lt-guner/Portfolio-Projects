import pygame
import traceback

from .constants import *
from .board import Board

from Chess.chess_engine import ChessEngine
from Chess.move import Move
from Chess.ai import ChessAI

from .client_network import Network


def get_player_color(data):
    """
    Returns a string of the player color.
    Determined by parsing the initial string message upon connecting with the server.
    """
    if data[-1] == '0':
        print('Player Color: White')
        return WHITE
    else:
        print('Player Color: Black')
        return BLACK


def is_turn(color, engine: ChessEngine):
    """
    Returns True if the inputted string color is the turn player in the game engine.
    Otherwise returns False.
    """
    if color == WHITE and engine.white_turn:
        return True
    if color == BLACK and not engine.white_turn:
        return True
    return False


def init_connect(network):
    """
    Returns a string of the player color. Returns None if connection error.
    Initializes a network connection with the server for online multiplayer.
    """
    # establish connection and receive first message with this client's color
    connect_message = network.connect()

    if connect_message == ERROR:
        print(GAME_FULL)
        return None
    else:
        print(connect_message)

        # initial message: waiting for server to indicate game is ready
        message = WAITING_GAME_START
        network.send(message)

        return get_player_color(connect_message)


def communicate_server(net_conn: Network):
    """
    Returns the data received from the server.
    Receives data from the server.
    Determines appropriate response according to UI and engine states.
    Sends the response to the server.
    """
    try:
        reply = net_conn.receive()

        # opponent disconnected. disconnect from server
        if reply == OPPONENT_DISCONNECTED:
            net_conn.close()

        else:
            # server is waiting for an opponent to connect
            if reply == WAITING_FOR_OPPONENT:
                # continue to wait
                payload = WAITING_GAME_START

            # server is waiting for a move
            elif reply == WAITING_FOR_TURN:
                # UI will only store move data into make_move data buffer if user's turn
                global make_move
                # no move data to send
                if make_move is None:
                    payload = READY

                # has move data to send
                else:
                    print('Sending move to opponent', make_move.get_move_legible())
                    # ready payload with move data, empty move data buffer
                    payload = make_move
                    make_move = None

            # received opponent move data
            else:
                global opponent_move
                print('Received opponent move:', reply.get_move_legible())

                # store opponent move data into buffer for UI and game engine
                opponent_move = reply
                payload = READY

            net_conn.send(payload)

        # print('Sending to server:', payload)
        # print('Received from server:', reply)

        return reply

    except:
        return None


def is_game_over(engine: ChessEngine):
    return engine.checkmate or engine.stalemate


def draw_board(board: Board, engine: ChessEngine, popup=False, popup_text=None):
    """
    Draws the current chess board state and updates the rendered image.
    If a popup window is to be displayed, returns the rectangle object to detect click
    """
    try:
        # Draws the board
        board.draw_squares(WIN)
        board.draw_coords(WIN)
        board.draw_selected(WIN, engine.valid_moves(), engine)
        board.draw_pieces(WIN, engine.get_board())
        board.draw_sidebar(WIN, engine)

        # draw a back button
        font = pygame.font.SysFont('Arial', 20)
        back_text = font.render("Back", True, WHITEISH)
        back_rect = back_text.get_rect(topright=((WIDTH + SIDEBAR_WIDTH), 0))
        WIN.blit(back_text, back_rect)

        if popup:
            popup_rect = draw_popup(popup_text)

        pygame.display.update()

        if popup:
            return popup_rect, back_rect
        return back_rect
    except:
        print("Draw Board Error!")
        raise


def draw_popup(message: str):
    """
    Renders text as a popup message in the center of the screen.
    Returns the window's rectangle object to detect click collision
    """
    font = pygame.font.SysFont('Arial', 24)
    popup_text = font.render(message, True, (0, 0, 0), (255, 255, 255))
    popup_rect = popup_text.get_rect(center=(WIDTH / 2, (0.9 * HEIGHT) / 2))

    WIN.blit(popup_text, popup_rect)

    return popup_rect


def draw_sel_menu(clock):
    """
    Draws the menu for the user to select single player or multiplayer
    """
    render_ai_difficulty = False
    global ai_difficulty, game_state

    while game_state == SEL_MENU:
        clock.tick(FPS)

        font = pygame.font.SysFont('Arial', 30, bold=True)

        WIN.fill((255, 255, 255))  # blanks out the screen. can replace with a background image

        # load the background
        background_chess = pygame.image.load('./FrontEnd/Assets/chessbackground.jpg')
        WIN.blit(background_chess, (0, 0))

        welcome_font = pygame.font.SysFont('Arial', 50, bold=True)
        welcome_text = welcome_font.render('Welcome', True, DARK_BROWN)
        welcome_rect = welcome_text.get_rect(center=(290, 175))
        WIN.blit(welcome_text, welcome_rect)
        chess_text = welcome_font.render('Chess', True, DARK_BROWN)
        chess_rect = chess_text.get_rect(center=(290, 275))
        WIN.blit(chess_text, chess_rect)
        player_text = welcome_font.render('Player', True, DARK_BROWN)
        player_rect = player_text.get_rect(center=(290, 375))
        WIN.blit(player_text, player_rect)

        # draw select AI difficulty options
        if render_ai_difficulty:
            easy_diff_text = font.render(EAS_DIFF, True, DARK_BROWN)
            easy_diff_rect = easy_diff_text.get_rect(center=((WINDOW_WIDTH - 150), HEIGHT / 3))

            med_diff_text = font.render(MED_DIFF, True, DARK_BROWN)
            med_diff_rect = med_diff_text.get_rect(center=((WINDOW_WIDTH - 150), (1.5 * HEIGHT) / 3))

            hard_diff_text = font.render(HAR_DIFF, True, DARK_BROWN)
            hard_diff_rect = hard_diff_text.get_rect(center=((WINDOW_WIDTH - 150), (2 * HEIGHT) / 3))

            WIN.blit(easy_diff_text, easy_diff_rect)
            WIN.blit(med_diff_text, med_diff_rect)
            WIN.blit(hard_diff_text, hard_diff_rect)

            # draw a back button
            back_text = font.render("Back", True, BLACKISH)
            back_rect = back_text.get_rect(topright=((WIDTH + SIDEBAR_WIDTH), 0))
            WIN.blit(back_text, back_rect)

        # draw single player vs AI / online vs player options
        else:
            single_play_text = font.render(SINGLE_PLAY, True, DARK_BROWN)
            single_play_rect = single_play_text.get_rect(center=((WINDOW_WIDTH - 150), HEIGHT / 3))

            multi_play_text = font.render(ONLINE_PLAY, True, DARK_BROWN)
            multi_play_rect = multi_play_text.get_rect(center=((WINDOW_WIDTH - 150), (2 * HEIGHT) / 3))

            WIN.blit(single_play_text, single_play_rect)
            WIN.blit(multi_play_text, multi_play_rect)

        # update display
        pygame.display.update()

        for event in pygame.event.get():
            # Allows the user to quit the game when they hit the exit button
            if event.type == pygame.QUIT:
                global run
                run = False
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                # detect mouse click to select AI difficulty
                if render_ai_difficulty:
                    if back_rect.collidepoint(pygame.mouse.get_pos()):
                        render_ai_difficulty = False
                    elif easy_diff_rect.collidepoint(pygame.mouse.get_pos()):
                        ai_difficulty = EAS_DIFF
                        game_state = SINGLE_PLAY
                    elif med_diff_rect.collidepoint(pygame.mouse.get_pos()):
                        ai_difficulty = MED_DIFF
                        game_state = SINGLE_PLAY
                    elif hard_diff_rect.collidepoint(pygame.mouse.get_pos()):
                        ai_difficulty = HAR_DIFF
                        game_state = SINGLE_PLAY

                # detect mouse click to select single vs online play
                else:
                    if single_play_rect.collidepoint(pygame.mouse.get_pos()):
                        render_ai_difficulty = True

                    elif multi_play_rect.collidepoint(pygame.mouse.get_pos()):
                        game_state = ONLINE_PLAY


def play_singleplayer(clock, difficulty):
    """
    Executes a game of chess against a computer AI
    """
    player_color = WHITE  # do we want to implement a color selection? (display after select difficult in draw_sel_menu)
    engine = ChessEngine()
    board = Board(player_color)
    ai = ChessAI()

    display_popup = False
    popup_text = None
    popup_win = None

    # get valid moves to start and move_made to False
    valid_moves = engine.valid_moves()
    move_made = False

    global game_state
    while game_state == SINGLE_PLAY:
        clock.tick(FPS)

        # render display
        if display_popup:
            popup_win, back_rect = draw_board(board, engine, display_popup, popup_text)
        else:
            back_rect = draw_board(board, engine)

        # What coordinates the mouse is in
        mouse_square = board.get_mouse_square()

        # game is over, return to select menu
        if is_game_over(engine):
            display_popup = True
            if engine.get_player_turn() == 'Black' and engine.get_status()[0]:
                popup_text = "WHITE WINS!!!!! Click here to return to menu"
            elif engine.get_player_turn() == 'White' and engine.get_status()[0]:
                popup_text = "BLACK WINS!!!!! Click here to return to menu"
            else:
                popup_text = "STALEMATE!!!!! Click here to return to menu"

        for event in pygame.event.get():
            # Allows the user to quit the game when they hit the exit button
            if event.type == pygame.QUIT:
                global run
                run = False
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(pygame.mouse.get_pos()):
                    game_state = SEL_MENU

            # game is not over
            if not is_game_over(engine):
                if is_turn(player_color, engine):
                    # user clicks on the board
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # second click: placing a selected piece on the board
                        if board.piece_chosen:
                            move = Move(board.piece_chosen, mouse_square, engine.board)

                            # make a move if it is a valid move and set move_made to true
                            if move in valid_moves:
                                if move.piece_moved[1] == 'P' and abs(move.start_col - move.end_col) == 1 \
                                        and move.piece_captured is None:
                                    move = Move(board.piece_chosen, mouse_square, engine.board, castle=False,
                                                enpassant=True)
                                elif move.piece_moved[1] == 'K' and abs(move.start_col - move.end_col) == 2:
                                    move = Move(board.piece_chosen, mouse_square, engine.board, castle=True,
                                                enpassant=False)
                                else:
                                    move = Move(board.piece_chosen, mouse_square, engine.board, castle=False,
                                                enpassant=False)

                                engine.make_move(move)
                                move_made = True

                                # store Move object into data buffer to send to server
                                global make_move
                                make_move = move
                            board.piece_chosen = None

                        # first click: selecting a piece to move
                        else:
                            row, col = mouse_square
                            # Won't allow a user to click on empty square
                            if not engine.is_empty_square(row, col):
                                board.piece_chosen = mouse_square
                # AI executes turn
                else:
                    # AI makes a move
                    if difficulty == EAS_DIFF:
                        ai_move = ai.random_ai(valid_moves)
                    elif difficulty == MED_DIFF:
                        ai_move = ai.greedy_ai(valid_moves, engine)
                    else:
                        ai_move = ai.negamax_alphabeta_ai(valid_moves, engine)
                    engine.make_move(ai_move)
                    move_made = True

                # get the next set of valid moves and reset move_made
                if move_made:
                    valid_moves = engine.valid_moves()
                    move_made = False

            # look for click on popup window to return to select menu
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if popup_win.collidepoint(pygame.mouse.get_pos()):
                        game_state = SEL_MENU


def play_multiplayer(clock):
    """
    Executes a game of chess against another player online
    """
    global game_state
    # connect to server and get player color
    n = Network()
    player_color = init_connect(n)

    display_popup = False
    popup_text = None
    popup_win = None

    # connection error, return to select menu
    if player_color is None:
        game_state = SEL_MENU
        return

    engine = ChessEngine()
    board = Board(player_color)

    # get valid moves to start and move_made to False
    valid_moves = engine.valid_moves()
    move_made = False

    while game_state == ONLINE_PLAY:
        clock.tick(FPS)

        # render display
        if display_popup:
            popup_win, back_rect = draw_board(board, engine, display_popup, popup_text)
        else:
            back_rect = draw_board(board, engine)

        try:
            # get message from server regarding game state
            server_state = communicate_server(n)

            # opponent disconnected, return to select menu
            if server_state == OPPONENT_DISCONNECTED:
                display_popup = True
                popup_text = "Opponent disconnected. Click here to return to menu"

            # game is over, return to select menu
            elif is_game_over(engine):
                display_popup = True
                if engine.get_player_turn() == 'Black' and engine.get_status()[0]:
                    popup_text = "WHITE WINS!!!!! Click here to return to menu"
                elif engine.get_player_turn() == 'White' and engine.get_status()[0]:
                    popup_text = "BLACK WINS!!!!! Click here to return to menu"
                else:
                    popup_text = "STALEMATE!!!!! Click here to return to menu"

            # What coordinates the mouse is in
            mouse_square = board.get_mouse_square()

            for event in pygame.event.get():
                # Allows the user to quit the game when they hit the exit button
                if event.type == pygame.QUIT:
                    global run
                    run = False
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_rect.collidepoint(pygame.mouse.get_pos()):
                        n.close()
                        game_state = SEL_MENU

                # game is going as normal (no popup displayed for error/game over)
                if not display_popup:
                    # server is waiting for move to be sent/received
                    if server_state == WAITING_FOR_TURN:
                        # this player's turn, look for user interaction to make a move
                        if is_turn(player_color, engine):
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                # second click: placing a selected piece on the board
                                if board.piece_chosen:
                                    move = Move(board.piece_chosen, mouse_square, engine.board)

                                    # make a move if it is a valid move and set move_made to true
                                    if move in valid_moves:
                                        if move.piece_moved[1] == 'P' and abs(move.start_col - move.end_col) == 1 \
                                                and move.piece_captured is None:
                                            move = Move(board.piece_chosen, mouse_square, engine.board, castle=False,
                                                        enpassant=True)
                                        elif move.piece_moved[1] == 'K' and abs(move.start_col - move.end_col) == 2:
                                            move = Move(board.piece_chosen, mouse_square, engine.board, castle=True,
                                                        enpassant=False)
                                        else:
                                            move = Move(board.piece_chosen, mouse_square, engine.board, castle=False,
                                                        enpassant=False)

                                        engine.make_move(move)
                                        move_made = True

                                        # store Move object into data buffer to send to server
                                        global make_move
                                        make_move = move
                                        print('UI/Engine: Storing move to send. END TURN.')
                                    board.piece_chosen = None

                                # first click: selecting a piece to move
                                else:
                                    row, col = mouse_square
                                    # Won't allow a user to click on empty square
                                    if not engine.is_empty_square(row, col):
                                        board.piece_chosen = mouse_square

                        # opponent's turn, look for move data in the buffer to execute
                        else:
                            global opponent_move
                            # opponent's move data buffer contains data (Move object)
                            if opponent_move is not None:
                                print('UI/Engine: Making opponent move. START TURN.')
                                move_made = True
                                # make the move in the engine and clear the data buffer
                                engine.make_move(opponent_move)
                                opponent_move = None

                        # get the next set of valid moves and reset move_made
                        if move_made:
                            valid_moves = engine.valid_moves()
                            move_made = False

                # look for click on popup window to return to select menu
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if popup_win.collidepoint(pygame.mouse.get_pos()):
                            game_state = SEL_MENU

        # error occurred, return to select menu
        except:
            traceback.print_exc()
            game_state = SEL_MENU


# set window parameters and caption name
WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(WIN_NAME)

# buffer to store move data
make_move = None  # this client has made a move to send to opponent
opponent_move = None  # received move made by opponent

run = True
game_state = SEL_MENU  # change to SEL_MENU when implemented
ai_difficulty = None


def main():
    clock = pygame.time.Clock()
    pygame.init()  # create the game window

    while run:
        if game_state == SEL_MENU:
            draw_sel_menu(clock)
        elif game_state == SINGLE_PLAY:
            play_singleplayer(clock, ai_difficulty)
        elif game_state == ONLINE_PLAY:
            play_multiplayer(clock)

    pygame.quit
