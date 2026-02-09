# game functionlity

# use curses, termbox, or rich for terminal idea. Leanning more towards rich

# use pytest for testing

board = [
    [" ", " ", " "],
    [" ", " ", " "],
    [" ", " ", " "]
]

def player_move(board, player, xCoord, yCoord):
        board[yCoord][xCoord] = player
        return

def valid_move(board, xCoord, yCoord):
    if board[yCoord][xCoord] == " ":
        return True
    else: 
        return False

def check_board(board):
    # check rows
    for row in board:
        if row[0] != " " and row[0] == row[1] == row[2]:
            return row[0]

    # check columns
    for col in range(3):
        if board[0][col] != " " and board[0][col] == board[1][col] == board[2][col]:
            return board[0][col]
    
    # check diagonals
    if board[0][0] != " " and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]

    if board[0][2] != " " and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]

    # no winner
    return None

def print_board(board):
    for i, row in enumerate(board):
        print(" | ".join(row))
        if i < 2:
            print("--+---+--")



