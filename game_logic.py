# =====================================================================
# GAME_LOGIC.PY
# THIS FILE HANDLES ALL THE "RULES" OF THE GAME:
#   - PARSING THE PLAYER'S INPUT (E.G. "B7" → ROW 1, COL 6)
#   - FIRING SHOTS AND WORKING OUT HIT / MISS / SUNK
#   - THE COMPUTER'S AI (RANDOM SHOTS THAT DON'T REPEAT)
#   - CHECKING WHETHER ALL SHIPS HAVE BEEN SUNK (WIN CONDITION)
# =====================================================================

import random

# IMPORT THE CONSTANTS WE NEED FROM BOARD_DISPLAY.
# THIS WAY WE HAVE ONE SOURCE OF TRUTH FOR THESE VALUES.
from board_display import ROW_LETTERS, WATER, SHIP, HIT, MISS


# =====================================================================
# INPUT PARSING — TURNING PLAYER INPUT LIKE "B7" INTO (ROW, COL)
# =====================================================================

def parse_coordinate(user_input):
    """
    TAKES A STRING LIKE "B7" OR "J10" AND TURNS IT INTO A (ROW, COL)
    TUPLE THAT WE CAN USE TO ACCESS THE BOARD.

    FOR EXAMPLE:
        "A1"  → (0, 0)
        "B7"  → (1, 6)     — ROW B IS INDEX 1, COLUMN 7 IS INDEX 6
        "J10" → (9, 9)

    IF THE INPUT IS INVALID, WE RETURN NONE AND AN ERROR MESSAGE
    SO THE GAME LOOP CAN ASK THE PLAYER TO TRY AGAIN.

    RETURNS:
        A TUPLE OF (ROW_INDEX, COL_INDEX) IF VALID.
        NONE IF INVALID.
        AND A MESSAGE STRING EXPLAINING WHAT WENT WRONG (OR "OK").
    """

    # STRIP REMOVES ANY SPACES THE PLAYER MIGHT HAVE TYPED BY ACCIDENT.
    # UPPER CONVERTS LOWERCASE LETTERS TO UPPERCASE SO "b7" WORKS TOO.
    cleaned = user_input.strip().upper()

    # CHECK THE INPUT IS NOT EMPTY.
    if len(cleaned) == 0:
        return None, "You didn't type anything! Try something like B7."

    # THE FIRST CHARACTER SHOULD BE A LETTER FROM A TO J.
    letter = cleaned[0]

    if letter not in ROW_LETTERS:
        return None, f"'{letter}' is not a valid row. Use a letter from A to J."

    # EVERYTHING AFTER THE FIRST CHARACTER SHOULD BE A NUMBER (1–10).
    number_part = cleaned[1:]

    # CHECK THE NUMBER PART IS ACTUALLY A NUMBER.
    # ISDIGIT() RETURNS TRUE IF EVERY CHARACTER IS 0–9.
    if not number_part.isdigit():
        return None, f"'{number_part}' is not a valid column number. Use 1 to 10."

    # CONVERT THE STRING TO AN INTEGER SO WE CAN DO MATHS WITH IT.
    column_number = int(number_part)

    # CHECK THE COLUMN IS IN THE VALID RANGE.
    if column_number < 1 or column_number > 10:
        return None, f"Column {column_number} is out of range. Use 1 to 10."

    # CONVERT FROM HUMAN-FRIENDLY TO COMPUTER-FRIENDLY INDICES.
    # THE PLAYER SAYS "A" BUT PYTHON NEEDS 0.
    # THE PLAYER SAYS COLUMN "1" BUT PYTHON NEEDS 0.
    # .INDEX() FINDS WHERE THE LETTER SITS IN ROW_LETTERS.
    # "A" IS AT POSITION 0, "B" IS AT POSITION 1, ETC.
    row_index = ROW_LETTERS.index(letter)
    col_index = column_number - 1

    return (row_index, col_index), "OK"


# =====================================================================
# SHOT LOGIC — WHAT HAPPENS WHEN SOMEONE FIRES AT A COORDINATE
# =====================================================================

def take_shot(board, ships, row, col):
    """
    FIRES A SHOT AT THE GIVEN (ROW, COL) ON THE BOARD.

    CHECKS WHAT IS AT THAT CELL AND UPDATES IT:
        - IF IT'S WATER ("~"), IT'S A MISS → MARK WITH "o".
        - IF IT'S A SHIP ("S"), IT'S A HIT → MARK WITH "X".
        - IF IT'S ALREADY "X" OR "o", THE PLAYER ALREADY SHOT THERE.

    AFTER A HIT, WE ALSO CHECK IF THAT SHIP HAS BEEN FULLY SUNK
    BY LOOKING THROUGH THE SHIPS LIST.

    PARAMETERS:
        board  — THE 10x10 GRID WE ARE SHOOTING AT.
        ships  — THE LIST OF SHIP DICTIONARIES FOR THAT BOARD.
        row    — THE ROW INDEX (0–9).
        col    — THE COLUMN INDEX (0–9).

    RETURNS:
        A STRING DESCRIBING WHAT HAPPENED:
        "miss", "hit", "hit_and_sunk", OR "already_shot".
        AND THE NAME OF THE SHIP THAT WAS HIT (OR NONE IF IT WAS A MISS).
    """

    cell = board[row][col]

    # --- ALREADY SHOT HERE ---
    if cell == HIT or cell == MISS:
        return "already_shot", None

    # --- MISS ---
    if cell == WATER:
        board[row][col] = MISS
        return "miss", None

    # --- HIT ---
    if cell == SHIP:
        board[row][col] = HIT

        # NOW WE NEED TO FIND WHICH SHIP WAS HIT.
        # WE LOOP THROUGH ALL THE SHIPS AND CHECK IF THE (ROW, COL)
        # IS IN THAT SHIP'S LIST OF COORDINATES.
        for ship in ships:
            if (row, col) in ship["coordinates"]:

                # INCREASE THE HIT COUNT FOR THIS SHIP.
                ship["hits"] = ship["hits"] + 1

                # CHECK IF THE SHIP IS NOW FULLY SUNK.
                # A SHIP IS SUNK WHEN THE NUMBER OF HITS EQUALS ITS SIZE.
                if ship["hits"] == ship["size"]:
                    return "hit_and_sunk", ship["name"]
                else:
                    return "hit", ship["name"]

    # THIS SHOULD NEVER HAPPEN, BUT JUST IN CASE:
    return "unknown", None


# =====================================================================
# CHECK IF ALL SHIPS ARE SUNK (WIN CONDITION)
# =====================================================================

def all_ships_sunk(ships):
    """
    CHECKS WHETHER EVERY SHIP IN THE LIST HAS BEEN FULLY SUNK.
    A SHIP IS SUNK WHEN ITS "HITS" COUNT EQUALS ITS "SIZE".

    WE LOOP THROUGH EVERY SHIP. IF WE FIND EVEN ONE THAT IS NOT
    SUNK, WE RETURN FALSE STRAIGHT AWAY. IF WE GET ALL THE WAY
    THROUGH WITHOUT FINDING AN UNSUNK SHIP, WE RETURN TRUE.
    """
    for ship in ships:
        if ship["hits"] < ship["size"]:
            return False

    return True


# =====================================================================
# COMPUTER'S TURN — RANDOM SHOT THAT DOESN'T REPEAT
# =====================================================================

def computer_take_shot(board, ships, previous_shots):
    """
    THE COMPUTER PICKS A RANDOM COORDINATE IT HASN'T TRIED BEFORE
    AND FIRES AT THE PLAYER'S BOARD.

    PARAMETERS:
        board           — THE PLAYER'S 10x10 GRID.
        ships           — THE PLAYER'S LIST OF SHIP DICTIONARIES.
        previous_shots  — A LIST OF (ROW, COL) TUPLES THE COMPUTER
                          HAS ALREADY FIRED AT. WE ADD THE NEW SHOT
                          TO THIS LIST SO IT WON'T BE PICKED AGAIN.

    RETURNS:
        row       — THE ROW THE COMPUTER SHOT AT.
        col       — THE COLUMN THE COMPUTER SHOT AT.
        result    — "miss", "hit", "hit_and_sunk", ETC.
        ship_name — THE NAME OF THE HIT SHIP (OR NONE).
    """

    # KEEP PICKING RANDOM COORDINATES UNTIL WE FIND ONE
    # THAT HASN'T BEEN SHOT AT BEFORE.
    while True:
        row = random.randint(0, 9)
        col = random.randint(0, 9)

        # CHECK IF THIS COORDINATE IS ALREADY IN OUR LIST.
        if (row, col) not in previous_shots:
            # IT'S A NEW SPOT — BREAK OUT OF THE WHILE LOOP.
            break

    # RECORD THIS SHOT SO WE DON'T PICK IT AGAIN.
    previous_shots.append((row, col))

    # FIRE THE SHOT USING OUR EXISTING TAKE_SHOT FUNCTION.
    result, ship_name = take_shot(board, ships, row, col)

    return row, col, result, ship_name


# =====================================================================
# HELPER — CONVERT (ROW, COL) BACK TO A HUMAN-READABLE STRING
# =====================================================================

def format_coordinate(row, col):
    """
    TURNS A (ROW, COL) TUPLE BACK INTO A STRING LIKE "B7".
    THIS IS USED WHEN TELLING THE PLAYER WHERE THE COMPUTER SHOT.

    FOR EXAMPLE:
        (0, 0) → "A1"
        (1, 6) → "B7"
        (9, 9) → "J10"
    """
    letter = ROW_LETTERS[row]
    number = col + 1
    return f"{letter}{number}"
