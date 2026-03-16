import random
import time
import json

# DEFINE CONSTANTS FOR THE ROWS AND SYMBOLS
# USED CAPS TO MAKE IT CLEAR THAT THESE ARE THE CONSTANTS
ROW_LETTERS = "ABCDEFGHIJ"
WATER = "~"
SHIP = "S"
HIT = "X"
MISS = "o"

def create_board():
    # MAKE A 10X10 GRID FILLED WITH ~ FOR WATER

    # 'BOARD' STARTS AS AN EMPTY LIST — THINK OF IT LIKE AN EMPTY
    # BOOKSHELF WITH NO SHELVES YET. EACH "SHELF" WE ADD WILL BE
    # ONE ROW OF THE GRID.
    board = []

    # THIS OUTER LOOP RUNS 10 TIMES (ROW 0 TO ROW 9), ONCE FOR
    # EACH ROW OF THE BOARD. EACH TIME ROUND IT BUILDS ONE FULL
    # ROW AND ADDS IT TO THE BOARD.
    for row in range(10):

        # 'CURRENT_ROW' STARTS AS A FRESH EMPTY LIST — THIS IS ONE
        # SINGLE HORIZONTAL ROW THAT WE ARE ABOUT TO FILL WITH 10
        # WATER CELLS. WE MAKE A NEW LIST EACH TIME SO EVERY ROW
        # IS ITS OWN SEPARATE THING. IF WE REUSED THE SAME LIST,
        # CHANGING A CELL IN ROW 3 WOULD ALSO CHANGE ROW 5 BY
        # MISTAKE BECAUSE THEY WOULD POINT TO THE SAME DATA.
        current_row = []

        # THIS INNER LOOP RUNS 10 TIMES (COLUMN 0 TO COLUMN 9).
        # EACH TIME ROUND IT ADDS ONE WATER CELL TO THE ROW.
        for column in range(10):
            # .APPEND() STICKS WATER ("~") ONTO THE END OF CURRENT_ROW.
            # AFTER ALL 10 GOES, CURRENT_ROW LOOKS LIKE THIS:
            #   ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"]
            current_row.append(WATER)

        # NOW CURRENT_ROW IS A FINISHED ROW OF 10 WATER CELLS.
        # .APPEND() HERE ADDS THE WHOLE ROW (WHICH IS ITSELF A LIST)
        # ONTO THE END OF 'BOARD'. SO 'BOARD' BECOMES A LIST OF LISTS
        # — THAT IS HOW WE MAKE A 2D GRID:
        #
        #   BOARD[0] = ["~", "~", "~", ... ]   ← ROW A
        #   BOARD[1] = ["~", "~", "~", ... ]   ← ROW B
        #   ...
        #   BOARD[9] = ["~", "~", "~", ... ]   ← ROW J
        #
        # TO GET A SINGLE CELL LATER, USE: BOARD[ROW][COLUMN]
        # FOR EXAMPLE BOARD[3][6] MEANS ROW D, COLUMN 7.
        board.append(current_row)

    return board

def print_boards(player_board, computer_board):
    # THIS WILL MATCH THE EXAMPLE UI FROM CONFLUENCE
    print("Your Board                              Opponent Board (fog-of-war)")
    print("    1 2 3 4 5 6 7 8 9 10                 1 2 3 4 5 6 7 8 9 10")
    
    # ITERATE THROUGH EACH ROW TO PRINT BOTH BOARDS SIDE BY SIDE
    for i in range(10):
        # 'I' IS THE ROW NUMBER (0 TO 9). WE USE IT TO GRAB BOTH
        # THE ROW LETTER (A TO J) AND THE RIGHT ROW FROM EACH BOARD.
        letter = ROW_LETTERS[i]
        
        # JOIN THE PLAYER'S ROW WITH SPACES
        # .JOIN IS USED HERE TO TURN THE STRING INTO A LIST WHICH IS EASIER TO WORK WITH

        # SMALL CORRECTION: .JOIN() ACTUALLY DOES IT THE OTHER WAY ROUND —
        # IT TAKES A LIST AND TURNS IT INTO A SINGLE STRING.
        # PLAYER_BOARD[I] IS A LIST LIKE ["~", "S", "S", "~", ...]
        # AND " ".JOIN() GLUES ALL THE ITEMS TOGETHER WITH A SPACE
        # BETWEEN EACH ONE, GIVING US: "~ S S ~ ..."
        # THIS IS MUCH TIDIER THAN STICKING STRINGS TOGETHER WITH + IN A LOOP.
        player_row_string = " ".join(player_board[i])
        
        # PREPARE THE COMPUTER'S ROW WHILE HIDING THE SHIPS (FOG OF WAR)

        # WE BUILD A BRAND NEW LIST HERE RATHER THAN CHANGING
        # COMPUTER_BOARD[I] DIRECTLY. WHY? BECAUSE WE DO NOT WANT TO
        # PERMANENTLY RUB OUT THE COMPUTER'S SHIP POSITIONS — WE ONLY
        # WANT TO HIDE THEM ON SCREEN. THE REAL DATA STAYS SAFE.
        computer_row_display = []

        # LOOP THROUGH EVERY CELL IN THE COMPUTER'S ROW. 'CELL' WILL
        # BE ONE OF: "~" (WATER), "S" (SHIP), "X" (HIT), OR "O" (MISS).
        for cell in computer_board[i]:
            if cell == SHIP:
                # IF THE CELL IS A SHIP, PUT WATER IN THE DISPLAY LIST
                # INSTEAD — THIS IS THE "FOG OF WAR". THE PLAYER SHOULD
                # NOT BE ABLE TO SEE WHERE THE COMPUTER'S SHIPS ARE.
                computer_row_display.append(WATER)
            else:
                # HITS, MISSES, AND WATER ALL SHOW AS THEY ARE — THE
                # PLAYER IS ALLOWED TO SEE THESE.
                computer_row_display.append(cell)

        # AFTER THE LOOP, COMPUTER_ROW_DISPLAY IS A LIST LIKE
        # ["~", "~", "X", "~", ...] WITH ALL "S" VALUES SWAPPED FOR "~".
        # NOW .JOIN() TURNS THAT LIST INTO A SINGLE STRING FOR PRINTING.
        computer_row_string = " ".join(computer_row_display)
        
        # PRINT THE ALIGNED ROWS WITH THE ROW LETTER
        print(f'{letter} | {player_row_string}              {letter} | {computer_row_string}')

# CREATE THE BOARDS
player_board = create_board()
computer_board = create_board()

# PRINT THEM
print_boards(player_board, computer_board)