from board_display import create_board, print_boards, print_single_board
from ship_placement import place_ships
from game_logic import parse_guess, take_shot, computer_shot, check_win

player_board = create_board()
computer_board = create_board()

player_ships = place_ships(player_board)
computer_ships = place_ships(computer_board)

computer_previous_shots = []

print_single_board(computer_board, "DEBUG - Computer's Board (remove this later!)")

while True:
    print_boards(player_board, computer_board)

    guess = input("Enter your shot (e.g. B7): ")

    result = parse_guess(guess)

    if result is None:
        print("Invalid input!")
        continue

    row, col = result

    shot_result = take_shot(computer_board, computer_ships, row, col)

    if shot_result == "already_shot":
        continue

    if check_win(computer_ships):
        print("You win!")
        break

    computer_shot(player_board, player_ships, computer_previous_shots)

    if check_win(player_ships):
        print("Computer wins!")
        break
