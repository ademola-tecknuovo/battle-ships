ROW_LETTERS = "ABCDEFGHIJ"
WATER = "~"
SHIP = "S"
HIT = "X"
MISS = "o"


def create_board():
    board = []
    for row in range(10):
        current_row = []
        for column in range(10):
            current_row.append(WATER)
        board.append(current_row)
    return board


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


def print_single_board(board, title):
    print()
    print(title)
    print("    1 2 3 4 5 6 7 8 9 10")
    for i in range(10):
        letter = ROW_LETTERS[i]
        row_string = " ".join(board[i])
        print(f"{letter} | {row_string}")
    print()
