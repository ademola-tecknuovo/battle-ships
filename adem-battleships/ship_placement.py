# =====================================================================
# SHIP_PLACEMENT.PY
# THIS FILE HANDLES EVERYTHING TO DO WITH PLACING SHIPS ON A BOARD.
# IT KNOWS WHAT SHIPS EXIST, HOW BIG THEY ARE, AND HOW TO RANDOMLY
# PLACE THEM WITHOUT GOING OFF THE EDGE OR OVERLAPPING.
# =====================================================================

import random

WATER = "~"
SHIP = "S"

# THIS IS THE LIST OF SHIPS WITH THEIR NAMES AND SIZES.
# EACH SHIP IS A SMALL DICTIONARY WITH A "NAME" AND A "SIZE".
# WE USE A LIST OF DICTIONARIES INSTEAD OF JUST A LIST OF NUMBERS
# SO THAT LATER WE CAN TELL THE PLAYER *WHICH* SHIP WAS HIT OR SUNK.
SHIP_DATA = [
    {"name": "Carrier", "size": 5},
    {"name": "Battleship", "size": 4},
    {"name": "Cruiser", "size": 3},
    {"name": "Submarine", "size": 3},
    {"name": "Destroyer", "size": 2},
]


def place_ships(board):
    """
    PLACES ALL 5 SHIPS RANDOMLY ON THE GIVEN BOARD.

    HOW IT WORKS:
    - FOR EACH SHIP, WE KEEP TRYING RANDOM POSITIONS AND DIRECTIONS
      UNTIL WE FIND ONE THAT FITS (IN BOUNDS AND NO OVERLAP).
    - ONCE PLACED, WE RECORD THE COORDINATES OF EVERY CELL THE SHIP
      OCCUPIES SO WE CAN CHECK FOR HITS AND SINKING LATER.

    RETURNS:
        A LIST OF SHIP DICTIONARIES. EACH ONE LOOKS LIKE THIS:
        {
            "name": "Carrier",
            "size": 5,
            "coordinates": [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5)],
            "hits": 0
        }
    """

    # THIS LIST WILL HOLD ALL THE SHIP INFO WE NEED FOR THE GAME.
    # WE BUILD IT UP AS WE PLACE EACH SHIP.
    all_ships = []

    # LOOP THROUGH EACH SHIP IN OUR SHIP_DATA LIST.
    for ship_info in SHIP_DATA:

        # GRAB THE NAME AND SIZE FROM THE DICTIONARY FOR THIS SHIP.
        name = ship_info["name"]
        size = ship_info["size"]

        # THIS FLAG TELLS US WHETHER THE SHIP HAS BEEN PLACED YET.
        placed = False

        # KEEP TRYING RANDOM POSITIONS UNTIL WE FIND A VALID ONE.
        while not placed:

            # PICK A RANDOM ROW (0–9) AND COLUMN (0–9).
            row = random.randint(0, 9)
            col = random.randint(0, 9)

            # PICK A RANDOM DIRECTION: HORIZONTAL OR VERTICAL.
            direction = random.choice(["H", "V"])

            # --- TRY TO PLACE HORIZONTALLY ---
            if direction == "H" and col + size <= 10:

                # CHECK EVERY CELL THE SHIP WOULD OCCUPY IS WATER.
                if all(board[row][col + i] == WATER for i in range(size)):

                    # ALL CLEAR — PLACE THE SHIP ON THE BOARD AND
                    # COLLECT THE COORDINATES.
                    coordinates = []

                    for i in range(size):
                        board[row][col + i] = SHIP
                        coordinates.append((row, col + i))

                    # BUILD THE SHIP RECORD AND ADD IT TO OUR LIST.
                    ship_record = {
                        "name": name,
                        "size": size,
                        "coordinates": coordinates,
                        "hits": 0,
                    }
                    all_ships.append(ship_record)

                    placed = True

            # --- TRY TO PLACE VERTICALLY ---
            elif direction == "V" and row + size <= 10:

                # CHECK EVERY CELL THE SHIP WOULD OCCUPY IS WATER.
                if all(board[row + i][col] == WATER for i in range(size)):

                    # ALL CLEAR — PLACE THE SHIP ON THE BOARD AND
                    # COLLECT THE COORDINATES.
                    coordinates = []

                    for i in range(size):
                        board[row + i][col] = SHIP
                        coordinates.append((row + i, col))

                    # BUILD THE SHIP RECORD AND ADD IT TO OUR LIST.
                    ship_record = {
                        "name": name,
                        "size": size,
                        "coordinates": coordinates,
                        "hits": 0,
                    }
                    all_ships.append(ship_record)

                    placed = True

    return all_ships
