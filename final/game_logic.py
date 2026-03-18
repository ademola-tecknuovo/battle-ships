# GAME_LOGIC.PY
# THIS FILE HANDLES ALL THE "RULES" OF THE GAME

import random
from board_display import ROW_LETTERS, WATER, SHIP, HIT, MISS

def parse_guess(guess):
    """
    This function takes the player's input (e.g. "B7") and converts it into
    a row and column that Python can use to access the board.

    The letter becomes the row (A=0, B=1)
    The number becomes the column (1=0, 2=1)

    Returns a tuple of (row, col) if the input is valid.
    Returns None if the input is invalid.
    """
    guess = guess.upper()
    # INVALID INPUT
    if len(guess) < 2:
        return None
    # INVALID INPUT
    if guess[0] not in ROW_LETTERS:
        return None

    # THE TRY BLOCK IS USED TO STOP THE PROGRAM FROM CRASHING WHEN INVALID INPUT
    try:
        # guess[1:] means "everything from position 1 onwards" 
        # THE -1 CHOPS OFF THE 1ST CHARACTER
        # INT CONVERTS THE VALUE INTO A FORMAT THAT PYTHON CAN WORK WITH
        # THIS IS NEEDED BECAUSE VALID INPUTS CAN BE 2 OR 3 CHARACTERS E.G B5, B10
        col = int(guess[1:]) - 1
    except ValueError:
        # RETURN NONE PRODUCES AN ERROR MESSAGE BECAUSE OF THE IF STATEMENT IN MAIN
        return None
    # THE ROW VARIABLE IS USED TO MAP THE LETTER FROM ROW LETTERS TO A ROW ON THE BOARD
    row = ROW_LETTERS.index(guess[0])
    # INVALID INPUT
    if col < 0 or col > 9:
        return None
    # Returns a tuple of (row, col) if the input is valid.
    return row, col


def take_shot(board, ships, row, col):
    """
    Fires a shot at the given row and column on the board.
    Checks what is at that cell and returns a string describing
    what happened: "already_shot", "miss", "hit", or "sunk".
    If it's a hit, it finds which ship was hit using the ships parameter
    and updates that ship's hit count.
    """
    # indexing a list of lists - BOARD IS A LIST AND EVERY ITEM INSIDE IT IS A LIST
    # THIS IS TO CHECK FOR DUPLICATE INPUTS 
    if board[row][col] == HIT or board[row][col] == MISS:
        print("Already tried there!")
        # THIS STRING LINKS TO MAIN, AS AN IF STATEMENT
        return "already_shot"
    # THIS IS USED TO OUTPUT THE CASE FOR WHEN THERE ARE MISSES 
    if board[row][col] == WATER:
        board[row][col] = MISS
        print("Miss!")
        return "miss"
    # THIS HANDLES VALID HITS
    if board[row][col] == SHIP:
        board[row][col] = HIT
        # SHIPS IS JUST A PLACEHOLDER FOR EITHER THE USER SHIP OR COMPUTER SHIP 
        # PYTHON GETS THIS FROM THE SHIP_DATA DICTIONARY
        for ship in ships:
            # CHECK IF THE CELL WE JUST HIT BELONGS TO THIS SHIP
            # BY LOOKING THROUGH ITS LIST OF COORDINATES
            if (row, col) in ship["coordinates"]:
                # IT DOES BELONG TO THIS SHIP, SO ADD 1 TO ITS HIT COUNT
                ship["hits"] = ship["hits"] + 1
                # CHECK IF THE NUMBER OF HITS NOW EQUALS THE SHIP'S SIZE
                # IF SO, EVERY CELL OF THE SHIP HAS BEEN HIT — IT'S SUNK
                if ship["hits"] == ship["size"]:
                    print(f"Hit! You sank the {ship['name']}! (length {ship['size']})")
                    return "sunk"
                else:
                    # IF THIS THEN THE SHIP IS HIT BUT NOT SUNK YET
                    print(f"Hit! ({ship['name']})")
                    return "hit"
    # COULDNT USE NONE HERE AS I USED THIS AS AN IF STATEMENT IN MAIN
    return "unknown"


def computer_shot(board, ships, previous_shots):
    """
    The computer picks a random row and column it hasn't tried
    before and fires at the board. Uses the ships parameter to work
    out which ship was hit and whether it's been sunk.
    """
    while True:
        row = random.randint(0, 9)
        col = random.randint(0, 9)

        if (row, col) not in previous_shots:
            break

    previous_shots.append((row, col))
    # TURNS THE ROW AND COLUMN NUMBERS BACK INTO A READABLE COORDINATE LIKE "B7"
    coord = f"{ROW_LETTERS[row]}{col + 1}"

    if board[row][col] == SHIP:
        board[row][col] = HIT

        for ship in ships:
            # We used a tuple because that's what we stored when we placed the ships in the function place_ships()
            if (row, col) in ship["coordinates"]:
                ship["hits"] = ship["hits"] + 1

                if ship["hits"] == ship["size"]:
                    print(f"Computer shoots at {coord} - Hit! {ship['name']} sunk! (length {ship['size']})")
                else:
                    print(f"Computer shoots at {coord} - Hit! ({ship['name']})")
    else:
        board[row][col] = MISS
        print(f"Computer shoots at {coord} - Miss!")


def check_win(ships):
    """
    Checks if all ships in the list have been sunk.
    Returns True if every ship's hit count equals its size,
    otherwise returns False.
    """
    for ship in ships:
        if ship["hits"] < ship["size"]:
            return False
    return True
