import socket
from _thread import *
import sys
import pickle
from FrontEnd.constants import *
from Chess.move import Move

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind(('', PORT))
except socket.error as e:
    str(e)

s.listen(2)
print(SERVER_START)


def threaded_client(conn, playerNum):
    """
    Creates a thread to send/receive data to each player.
    """
    global playerCount, player_data, player_connected, game_start

    # initial message on connection, sends the player #
    conn.send(pickle.dumps("Connected as player " + str(playerNum)))
    player_connected[playerNum] = True

    while True:
        try:
            data = pickle.loads(conn.recv(2048))

            # for some reason, no data was received
            if not data:
                print("Disconnected from player", playerNum)
                break

            # check if opponent has disconnected
            if game_start and playerNum == 0 and not player_connected[1]:
                reply = OPPONENT_DISCONNECTED
                print("Player 0's opponent has disconnected")
            elif game_start and playerNum == 1 and not player_connected[0]:
                reply = OPPONENT_DISCONNECTED
                print("Player 1's opponent has disconnected")

            # successful connection
            else:
                # client is waiting for confirmation that the game has begun
                if data == WAITING_GAME_START:
                    if playerNum == 0:
                        # check if the opponent is connected
                        if player_connected[1] is False:
                            # reply waiting for an opponent
                            reply = WAITING_FOR_OPPONENT
                        else:
                            # game started: waiting for turn player to send move
                            reply = WAITING_FOR_TURN
                    else:
                        if player_connected[0] is False:
                            reply = WAITING_FOR_OPPONENT
                        else:
                            reply = WAITING_FOR_TURN

                # game started: client is waiting to receive move data
                elif data == READY:
                    # check if opponent has data in the data buffer to send
                    if playerNum == 0 and player_data[1]:
                        # reply with opponent's move data, clear data
                        reply = player_data[1]
                        player_data[1] = None
                    elif playerNum == 1 and player_data[0]:
                        reply = player_data[0]
                        player_data[0] = None

                    # turn player did not make a move yet
                    else:
                        reply = WAITING_FOR_TURN

                # game started: received move data from turn player, save to data buffer
                else:
                    print('Received move from player', playerNum)
                    # save move data to corresponding player's data buffer
                    player_data[playerNum] = data
                    reply = WAITING_FOR_TURN

            # print("Received from player " + str(playerNum) + ": ", data)
            # print("Sending to player " + str(playerNum) + ": ", reply)

            conn.sendall(pickle.dumps(reply))

        except:
            print("Lost connection with player", playerNum)
            break

    conn.close()

    # player disconnected, updates playerNum and player_connected variables
    playerCount -= 1
    player_connected[playerNum] = False
    player_data[playerNum] = None

    # no connected players, end game
    if playerCount == 0:
        print("---Ending game---")
        game_start = False
        print("---Waiting for new connections---")


# index 0: white player, index 1: black player
playerCount = 0
player_data = [None, None]          # stores move data received from the turn player
player_connected = [False, False]   # boolean for whether players have connected
game_start = False

while True:
    conn, addr = s.accept()

    # fewer than 2 players and no existing game, start connection
    if playerCount <= 1 and not game_start:
        print("Connected to:", addr, "as player", playerCount)
        start_new_thread(threaded_client, (conn, playerCount))

        # second player connected, start the game
        if playerCount == 1:
            print("---Starting new game---")
            game_start = True

        playerCount += 1

    # more than 2 players, disconnect new connections immediately
    else:
        conn.send(pickle.dumps(ERROR))
        conn.close()
