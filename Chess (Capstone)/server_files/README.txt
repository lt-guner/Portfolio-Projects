Chess / Boardgame: Server Description


upon initial connection:
    - sends a string "Connected as player #" (can be changed)
    - player number will be 0 (white) or 1 (black
    - client can decode the last char of this initial connection string to set its color

during connection / gameplay:
    - sends data from client 0 to client 1
    - sends data from client 1 to client 0
    - (our design) no data validation, so assumes the data is a string that will enable the receiving client to execute the move
    - test client currently sends 'Waiting...' when no data is being sent

rejects additional connection requests

things to consider or handle later:
    - client disconnect? (e.g. allow the same client to rejoin; need to game state on server)


CURRENT TEST_GAME.PY SETUP:
- don't forget to change the ip address of the server variable to your own
- run server

- run first client (player 0, white)
    sends data: 'SEND FROM WHITE'
    receives: 'Waiting...'
    prints: 'WHITE' and 'Waiting...'

- run second client (player 1, black)
    sends data: 'SEND FROM BLACK'
    receives: 'SEND FROM WHITE'
    prints: 'BLACK' and 'SEND FROM WHITE'

- when second client connects, first client begins printing 'WHITE' and 'SEND FROM BLACK'