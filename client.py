# client will be multithreaded
import socket
import sys
import json
import threading
from chatui import init_windows, read_command, print_message, end_windows
from packets import *
from tic_tac_toe import *

packet_buffer = b''
THREAD_COUNT = 1

def sending_thread(nickname):
    while True:
        message = read_command(f"{nickname}> ")
        # check if it starts with / then go down further
        if message[0] == "/":
            parts = message.strip().split()
            command = parts[0]

            if command == "/q":
                end_windows()
                #s.close()
                sys.exit()
                return
            
            if command == "/move":
                if len(parts) != 3:
                    print("Usage: /move xCoord yCoord")
                
                else:
                    xCoord = int(parts[1])
                    yCoord = int(parts[2])

                    move = json.dumps({
                        "type": "move",
                        "xCoord": xCoord, 
                        "yCoord": yCoord
                    })

                    move_payload = build_packet(move)
                    s.sendall(move_payload)
                    continue

        chat = json.dumps({
            "type": "chat",
            "message": message
        })

        chat_payload = build_packet(chat)

        s.sendall(chat_payload)

def recieving_thread():
    while True:

        packet = get_next_packet(s, packet_buffer)
        extracted_json = extract_json(packet)
        payload_type = extracted_json["type"]
        name = extracted_json["nick"]

        if payload_type == "join":
            print_message(f"*** {name} has joined the chat")

        if payload_type == "chat":
            message = extracted_json["message"]
            print_message(f"{name}: {message}")

        if payload_type == "leave":
            print_message(f"*** {name} has left the chat")

        if payload_type == "board":
            board = extracted_json["board"]
            print(f"{board}")

# Main
s = socket.socket()

nickname = sys.argv[1]
host = sys.argv[2]
port = int(sys.argv[3])

server = (host, port)

s.connect(server)


init_windows()

hello = json.dumps({
    "type": "hello",
    "nick": nickname
})

hello_payload = build_packet(hello)

s.sendall(hello_payload)

t = threading.Thread(target=recieving_thread, args=(), daemon=True)

t.start()

sending_thread(nickname)