# Use select, no default port always specify with command line

import sys
import socket
import select
import json
from packets import *
from tic_tac_toe import *

def broadcast(setsocket, listener, packet):
    for client in setsocket:
        if client != listener:  # Don't send to listener or sender
            try:
                client.sendall(packet)
            except:
                pass  # Handle client disconnect during send

# select loop
def run_server(port):
    port = int(sys.argv[1])

    s1 = socket.socket()

    s1.bind(('', port))
    s1.listen()
    setsocket = set()

    setsocket.add(s1)

    client_buffers = {}
    client_info = {}  

    players = []
    current_turn = None
    initial_board = board

    while True:
        sockets, _, _ = select.select(setsocket, {}, {})
        # if listener
        for s in sockets:
            # if s is listener, accept new connection
            if s is s1:
                conn, addr = s.accept()
                setsocket.add(conn)
                client_buffers[conn] = b''
                print(f"{addr}: connected")

            # if normal socket, receive data
            else:
                data = get_next_packet(s, client_buffers[s])

                # if there is no data, disconnect from server
                if not data:
                    leave = json.dumps({
                            "type": "leave",
                            "nick": client_info[s]["name"]
                        })
                    leave_payload = build_packet(leave)
                    broadcast(setsocket, s1, leave_payload)
                    setsocket.remove(s)
                    s.close()

                # if there is data, print data
                else:
                    # Handle the received data here
                    extracted_data = extract_json(data)

                    # welcomes new users, and assigns players
                    if extracted_data["type"] == "hello":
                        client_info[s] = { "name": extracted_data["nick"]}

                        if len(players) < 2:
                            players.append(s)

                            if len(players) == 1:
                                current_turn = s

                        join = json.dumps({
                            "type": "join",
                            "nick": client_info[s]["name"]
                        })

                        join_payload = build_packet(join)
                        broadcast(setsocket, s1, join_payload)

                    # handle chats
                    elif extracted_data["type"] == "chat":
                        chat = json.dumps({
                            "type": "chat",
                            "nick": client_info[s]["name"],
                            "message": extracted_data["message"]
                        })
                    
                        chat_payload = build_packet(chat)
                        broadcast(setsocket, s1, chat_payload)

                    # handle moves
                    elif extracted_data["type"] == "move":
                        # spectators do not play
                        if s not in players:
                            spectator_rejection = json.dumps({
                                "type": "rejection",
                                "nick": client_info[s]["name"],
                                "message": "Only players can make a move"
                            })
                            spectator_rejection_payload = build_packet(spectator_rejection)
                            s.sendall(spectator_rejection_payload)
                            
                        # can't play if its not your turn
                        elif s != current_turn:
                            player_rejection = json.dumps({
                                "type": "rejection",
                                "nick": client_info[s]["name"],
                                "message": "Not your turn"
                            })
                            player_rejection_payload = build_packet(player_rejection)
                            s.sendall(player_rejection_payload)
                        
                        else:
                            xCoord = extracted_data["xCoord"]
                            yCoord = extracted_data["yCoord"]

                            if valid_move(board, xCoord, yCoord) is False:
                                invalid_move = json.dumps({
                                    "type": "rejection",
                                    "nick": client_info[s]["name"],
                                    "message": "Invalid Move, Space Occupied"
                                })
                                invlaid_move_payload = build_packet(invalid_move)
                                s.sendall(invlaid_move_payload)
                            
                            else:
                                symbol = "X" if players[0] == s else "O"

                                player_move(board, symbol, xCoord, yCoord)

                                # Switch turn
                                current_turn = players[1] if current_turn == players[0] else players[0]

                                board_update = json.dumps({
                                    "type": "board",
                                    "nick": client_info[s]["name"],
                                    "board": board
                                })

                                board_update_payload = build_packet(board_update)
                                broadcast(setsocket, s1, board_update_payload)

def usage():
    print("usage: select_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))



