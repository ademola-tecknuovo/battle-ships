#  IMPORTS FUNCTIONS FROM BOARD_DISPLAY, SHIP_PLACEMENT AND GAME_LOGIC

from board_display import create_board, print_boards, print_single_board
from ship_placement import place_ships
from game_logic import parse_guess, take_shot, computer_shot, check_win

# CREATES TO SEPARATE BOARDS. ONE FOR THE PLAYER AND ONE FOR THE COMPUTER (IMPORTED FUNCTION FROM BOARD_DISPLAY FILE)
player_board = create_board()
computer_board = create_board()

# CALLS THE SHIP_PLACEMENT FUNCTION AND PLACES THE SHIPS RANDOMLY ON BOTH THE COMPUTER AND USERS BOARDS
player_ships = place_ships(player_board)
computer_ships = place_ships(computer_board)

# THIS WILL STORE ALL SHOTS TAKEN BY THE COMPUTER. AVOIDS COMPUTER SHOOTING IN THE SAME PLACE TWICE
computer_previous_shots = []

# SHOW THE COMPUTERS BOARD FOR TESTING. NORMALLY THIS WILL BE HIDDEN 
# COMMENT THIS LINE OUT TO REMOVE THE COMPUTER BOARD
print_single_board(computer_board, "DEBUG - Computer's Board (remove this later!)")

# WHILE LOOP TO KEEP RUNNING UNTIL PLAYER OR COMPUTER WINS
# DISPLAYS BOTH BOARDS SIDE BY SIDE 
while True:
    print_boards(player_board, computer_board)

# ASKS THE USER TO ENTER COORDINATES 
# PARSE_GUESS CONVERTS THE INPUT INTO A ROW AND COLUMN
    guess = input("Enter your shot (e.g. B7): ")

    result = parse_guess(guess)

# INPUT VALIDATION - IF THE INPUT IS INVALID, IT ASKED THE PLAYER TO TRY AGAIN
    if result is None:
        print("Invalid input!")
        continue

# FUNCTION GETS THE ROW AND COLUMN FROM THE THE USERS INPUT
# THEN FIRES A SHOT AT THE POSITION ON THE COMPUTERS BOARD AND STORE THE RESULT
    row, col = result

    shot_result = take_shot(computer_board, computer_ships, row, col)

# PREVENTS DUPLICATE SHOTS - IF THE PLAYER SHOOTS IN THE SAME PLACE, IT SKIPS THE TURN AND ASKS FOR ANOTHER INPUT
    if shot_result == "already_shot":
        continue

# CHECKS IF ALL COMPUTER SHIPS HAVE BEEN DESTROYED - IF YES THE GAME WILL PRINT "YOU WIN" AND ENDS THE GAME
    if check_win(computer_ships):
        print("You win!")
        break

# COMPUTER WILL TAKE A RANDOM SHOT AT THE PLAYERS BOARD.
# IT USES THE PREVIOUS SHOTS LIST TO AVOID REPEATING THE SAME MOVE 
    computer_shot(player_board, player_ships, computer_previous_shots)

# CHECK IF ALL THE PLAYERS SHIPS ARE DESTROYED - IF YES THE GAME WILL PRINT "COMPUTER WINS" AND ENDS THE GAME
    if check_win(player_ships):
        print("Computer wins!")
        break
