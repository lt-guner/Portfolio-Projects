# socket connection parameters
SERVER = '192.168.1.16'     # change to ip address of where server is run
PORT = 5555

# server-to-client messages
WAITING_FOR_OPPONENT = 'Waiting for an opponent'
WAITING_FOR_TURN = 'Waiting for turn'
ERROR = 'Error'
OPPONENT_DISCONNECTED = 'Opponent disconnected'

# server terminal messages
SERVER_START = 'Server Started... Waiting for a connections'

# client-to-server messages
WAITING_GAME_START = 'Waiting for game to start'
READY = 'Ready'

# client terminal messages
GAME_FULL = 'Connection Terminated. Game is already full.'
CONN_SUCCESS = 'Connected to server'
LOST_CONN_RECONN = 'Connection lost... reconnecting'
RECONN_SUCCESS = 'Reconnection successful'

# constants for chess game
WHITE = 'w'
BLACK = 'b'
