# IMPORTS RANDOM
# WATER REPRESENTS THE EMPTY SPACES ON THE BOARD " ~ "
# SHIP REPRESENTS WHERE THE SHIPS ARE PLACED " S "

import random

WATER = "~"
SHIP = "S"

# THIS LIST OF DICTIONARIES FOR ALL THE SHIPS IN THE GAME
# EACH SHIP HAS A NAME AND SIZE
SHIP_DATA = [
    {"name": "Carrier", "size": 5},
    {"name": "Battleship", "size": 4},
    {"name": "Cruiser", "size": 3},
    {"name": "Submarine", "size": 3},
    {"name": "Destroyer", "size": 2},
]


# THE FUNCTION PLACES ALL SHIPS ONTO A THE USER AND COMPUTER BOARD
# ALL_SHIPS IS USED TO STORE WHERE ALL THE SHIPS HAVE BEEN PLACED
def place_ships(board):
    all_ships = []

# LOOPS THROUGH ALL THE SHIPS DEFINED ABOVE AND PLACES ONE AT A TIME
# "PLACED = FALSE" WAS USED SO THE CODE WOULD KEEP TRYING TO PLACE SHIPS UNTIL ALL 5 HAVE BEEN PLACED.
    for ship_info in SHIP_DATA:
        name = ship_info["name"]
        size = ship_info["size"]
        placed = False

        while not placed:

# USES THE RANDOM IMPORT MODULE TO RANDOMLY PLACE SHIPS H OR V            
            row = random.randint(0, 9)
            col = random.randint(0, 9)
            direction = random.choice(["H", "V"])

# PREVENTS SHIPS FROM GOING OFF THE 10 X 10 GRID HORIZONTALLY 
            if direction == "H" and col + size <= 10:

# CHECKS POSITIONS ARE FREE TO PLACE THE SHIPS. PREVENTS OVERLAPPING              
                if all(board[row][col + i] == WATER for i in range(size)):

# PLACES EACH SHIP ON THE BOARD
# SAVES THE POSITION TO THE COORDINATES LIST                    
                    coordinates = []
                    for i in range(size):
                        board[row][col + i] = SHIP
                        coordinates.append((row, col + i))

# STORES ALL INFORMATION ABOUT THE SHIP AND HOW MANY HITS ON EACH SHIP                        
                    all_ships.append({"name": name, "size": size, "coordinates": coordinates, "hits": 0})

# STOPS THE LOOP ONCE ALL SHIPS HAVE BEEN PLACED "H"                    
                    placed = True

# PREVENTS SHIPS FROM GOING OFF THE 10 X 10 GRID VERTICALLY 
            elif direction == "V" and row + size <= 10:

# CHECKS POSITIONS ARE FREE TO PLACE THE SHIPS. PREVENTS OVERLAPPING                
                if all(board[row + i][col] == WATER for i in range(size)):

# PLACES EACH SHIP ON THE BOARD
# SAVES THE POSITION TO THE COORDINATES LIST                    
                    coordinates = []
                    for i in range(size):
                        board[row + i][col] = SHIP
                        coordinates.append((row + i, col))

# STORES ALL INFORMATION ABOUT THE SHIP AND HOW MANY HITS ON EACH SHIP                         
                    all_ships.append({"name": name, "size": size, "coordinates": coordinates, "hits": 0})

# STOPS THE LOOP ONCE ALL SHIPS HAVE BEEN PLACED "V"                    
                    placed = True

# RETURNS A LIST OF ALL SHIPS IN THE "ALL-SHIPS" LIST
# USED LATER FOR DETECTING HITS AND WIN CHECKING
    return all_ships
