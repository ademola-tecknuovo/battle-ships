# =====================================================================
# BOARD_DISPLAY.PY
# THIS FILE HANDLES CREATING THE 10x10 GRIDS AND PRINTING THEM.
# IT KNOWS HOW TO SHOW THE PLAYER'S BOARD (WITH SHIPS VISIBLE)
# AND THE OPPONENT'S BOARD (WITH SHIPS HIDDEN — FOG OF WAR).
# =====================================================================

# THESE CONSTANTS ARE SHARED ACROSS FILES.
# WE DEFINE THEM HERE BECAUSE THIS FILE IS THE "HOME" FOR BOARD STUFF.
ROW_LETTERS = "ABCDEFGHIJ"
WATER = "~"
SHIP = "S"
HIT = "X"
MISS = "o"


def create_board():
    """
    MAKES A 10x10 GRID FILLED WITH "~" FOR WATER.
    RETURNS A LIST OF 10 LISTS, EACH CONTAINING 10 "~" STRINGS.
    """
    board = []

    for row in range(10):
        current_row = []

        for column in range(10):
            current_row.append(WATER)

        board.append(current_row)

    return board


def print_boards(player_board, computer_board):
    """
    PRINTS BOTH BOARDS SIDE BY SIDE.
    THE PLAYER'S BOARD SHOWS EVERYTHING (INCLUDING THEIR OWN SHIPS).
    THE COMPUTER'S BOARD HIDES SHIPS — ONLY HITS AND MISSES SHOW.
    """
    print()
    print("Your Board                              Opponent Board (fog-of-war)")
    print("    1 2 3 4 5 6 7 8 9 10                    1 2 3 4 5 6 7 8 9 10")

    for i in range(10):
        letter = ROW_LETTERS[i]

        # JOIN THE PLAYER'S ROW INTO A SINGLE STRING.
        player_row_string = " ".join(player_board[i])

        # BUILD THE COMPUTER'S ROW WITH FOG OF WAR.
        # WE MAKE A NEW LIST SO WE DON'T CHANGE THE ACTUAL BOARD DATA.
        computer_row_display = []

        for cell in computer_board[i]:
            if cell == SHIP:
                # HIDE THE SHIP — SHOW WATER INSTEAD.
                computer_row_display.append(WATER)
            else:
                # HITS, MISSES, AND WATER ALL SHOW AS THEY ARE.
                computer_row_display.append(cell)

        computer_row_string = " ".join(computer_row_display)

        print(f"{letter} | {player_row_string}              {letter} | {computer_row_string}")

    print()


def print_single_board(board, title):
    """
    PRINTS ONE BOARD ON ITS OWN WITH A TITLE.
    USEFUL FOR DEBUGGING — WE CAN SEE WHERE THE COMPUTER'S SHIPS ARE.
    IN THE FINAL VERSION, REMOVE CALLS TO THIS FUNCTION.
    """
    print()
    print(title)
    print("    1 2 3 4 5 6 7 8 9 10")

    for i in range(10):
        letter = ROW_LETTERS[i]
        row_string = " ".join(board[i])
        print(f"{letter} | {row_string}")

    print()
