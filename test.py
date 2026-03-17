from pc_selection import place_computer_ships

import random
import time
import json

# CONSTANTS
ROW_LETTERS = "ABCDEFGHIJ"
WATER = "~"
SHIP = "S"
HIT = "X"
MISS = "o"


# CREATE BOARD
def create_board():
    board = []

    for row in range(10):
        current_row = []

        for column in range(10):
            current_row.append(WATER)

        board.append(current_row)

    return board


# PRINT BOARDS
def print_boards(player_board, computer_board):

    print("Your Board                              Opponent Board (fog-of-war)")
    print("    1 2 3 4 5 6 7 8 9 10                 1 2 3 4 5 6 7 8 9 10")

    for i in range(10):

        letter = ROW_LETTERS[i]

        player_row_string = " ".join(player_board[i])

        computer_row_display = []

        for cell in computer_board[i]:
            if cell == SHIP:
                computer_row_display.append(WATER)
            else:
                computer_row_display.append(cell)

        computer_row_string = " ".join(computer_row_display)

        print(f'{letter} | {player_row_string}              {letter} | {computer_row_string}')


# -----------------------------
# NEW CODE STARTS HERE
# -----------------------------

# PARSE USER INPUT
def parse_guess(guess):

    guess = guess.upper()

    if len(guess) < 2:
        return None

    if guess[0] not in ROW_LETTERS:
        return None

    try:
        col = int(guess[1:]) - 1
    except:
        return None

    row = ROW_LETTERS.index(guess[0])

    if col < 0 or col > 9:
        return None

    return row, col


# HANDLE SHOT
def take_shot(board, row, col):

    if board[row][col] == SHIP:
        print("Hit!")
        board[row][col] = HIT

    elif board[row][col] == WATER:
        print("Miss!")
        board[row][col] = MISS

    else:
        print("Already tried there!")


# COMPUTER TURN
def computer_shot(board):

    while True:

        row = random.randint(0, 9)
        col = random.randint(0, 9)

        if board[row][col] == WATER or board[row][col] == SHIP:

            print(f"Computer shoots at {ROW_LETTERS[row]}{col+1}")

            if board[row][col] == SHIP:
                print("Computer hit your ship!")
                board[row][col] = HIT
            else:
                print("Computer missed!")
                board[row][col] = MISS

            break


# CHECK WIN
def check_win(board):

    for row in board:
        if SHIP in row:
            return False

    return True


# -----------------------------
# MAIN GAME STARTS HERE
# -----------------------------

# CREATE BOARDS
player_board = create_board()
computer_board = create_board()

# PLACE SHIPS
place_computer_ships(computer_board)
place_computer_ships(player_board)

# GAME LOOP
while True:

    print_boards(player_board, computer_board)

    # PLAYER TURN
    guess = input("Enter your shot (e.g. B7): ")

    result = parse_guess(guess)

    if result is None:
        print("Invalid input!")
        continue

    row, col = result

    take_shot(computer_board, row, col)

    # CHECK IF PLAYER WINS
    if check_win(computer_board):
        print("You win!")
        break

    # COMPUTER TURN
    computer_shot(player_board)

    # CHECK IF COMPUTER WINS
    if check_win(player_board):
        print("Computer wins!")
        break