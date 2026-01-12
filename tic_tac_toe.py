# game functionlity

# use curses, termbox, or rich for terminal idea. Leanning more towards rich

# use pytest for testing

board = [
    [" ", " ", " "],
    [" ", " ", " "],
    [" ", " ", " "]
]

def player_move(board, player):
    while True: 
        xCord = int(input("Input x coordinate Move: "))
        yCord = int(input("Input y coordinate Move: "))
        if valid_move(board, xCord, yCord) == True:
            board[yCord][xCord] = player
            return
        else:
            print("Invalid Move, Space Occupied")

def valid_move(board, xCord, yCord):
    if board[yCord][xCord] == " ":
        return True
    else: 
        return False

# valid_move(board, 0, 0)
# board[0][0] = "O"
# valid_move(board, 0, 0)

while True:
    print(board)
    player_move(board, "X")
    print(board)
    player_move(board, "O")


