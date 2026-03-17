# imports the random module. Randomly place ships on the board
import random

WATER = "~"
SHIP = "S"


# defines a function called "place computer ships"
def place_computer_ships(board):

# list of ships lengths 
    ships = [5, 4, 3, 3, 2]

# Loops through each ship size in the list     
    for ship in ships:

# checks if the ship has been placed and if not continues to try place the ship
        placed = False

# while loop to keep the loop running until ships are (placed = true)
# not placed means it will keep looping as long as it placed is "false"
        while not placed:
# picks a random row or column to place the ships

            row = random.randint(0, 9)
            col = random.randint(0, 9)

# picks a random dicection whether H or V. left to right or top to bottom            
            direction = random.choice(["H", "V"])
            
# check if the ship can fit H without going off the board 10 x 10 grid
#            
            if direction == "H" and col + ship <= 10:

# checks if the spaces on the borad are empty for the entire ship length 
#               
                if all(board[row][col+i] == WATER for i in range(ship)):

# places the ships on the board H.
# loops through the ship length and places ship on each cell. i.e. ships length 3, will take up 3 cells)                    
                    for i in range(ship):
                        board[row][col+i] = SHIP

# sets the placed boolean to true meaning the ship has been placed successfully                      
                    placed = True

# check if the ship can fit V without going off the board. 
# ####                   
            elif direction == "V" and row + ship <= 10:

# checks if the vertical space is empty for the length of the ship
                if all(board[row+i][col] == WATER for i in range(ship)):

# places the ship on the board vertically                    
                    for i in range(ship):
                        board[row+i][col] = SHIP

#  sets the placed boolean to true meaning the ship has been placed successfully                        
                    placed = True
