# =====================================================================
# MAIN.PY
# THIS IS THE FILE YOU RUN TO PLAY THE GAME: python3 main.py
# IT IMPORTS FROM THE OTHER FILES AND TIES EVERYTHING TOGETHER
# INTO A TURN-BY-TURN GAME LOOP.
# =====================================================================

from board_display import create_board, print_boards, print_single_board
from ship_placement import place_ships
from game_logic import (
    parse_coordinate,
    take_shot,
    all_ships_sunk,
    computer_take_shot,
    format_coordinate,
)


def main():
    """
    THE MAIN GAME FUNCTION.
    SETS UP BOARDS, PLACES SHIPS, AND RUNS THE TURN LOOP
    UNTIL SOMEONE WINS.
    """

    # === SET UP THE BOARDS ===
    player_board = create_board()
    computer_board = create_board()

    # PLACE SHIPS ON BOTH BOARDS.
    # place_ships RETURNS A LIST OF SHIP DICTIONARIES
    # SO WE CAN TRACK HITS AND SINKING.
    player_ships = place_ships(player_board)
    computer_ships = place_ships(computer_board)

    # THE COMPUTER NEEDS TO REMEMBER WHERE IT HAS ALREADY SHOT.
    computer_previous_shots = []

    # === DEBUG: SHOW THE COMPUTER'S BOARD SO WE CAN TEST ===
    # REMOVE THIS LINE IN THE FINAL VERSION!
    print_single_board(computer_board, "DEBUG — Computer's Board (remove this later!)")

    # === SHOW THE STARTING BOARDS ===
    print("Starting positions (before any shots)")
    print_boards(player_board, computer_board)

    # === GAME LOOP ===
    turn_number = 1

    while True:
        print(f"--- Turn {turn_number} ---")
        print()

        # =============================================================
        # PLAYER'S TURN
        # KEEP ASKING UNTIL THEY GIVE A VALID, NEW COORDINATE.
        # =============================================================
        while True:
            user_input = input("Enter your shot (e.g. B7): ")

            # TRY TO PARSE THE INPUT.
            result, message = parse_coordinate(user_input)

            if result is None:
                # THE INPUT WAS INVALID — SHOW THE ERROR AND ASK AGAIN.
                print(f"  Error: {message}")
                continue

            # UNPACK THE VALID COORDINATE.
            row, col = result

            # FIRE THE SHOT.
            shot_result, ship_name = take_shot(
                computer_board, computer_ships, row, col
            )

            if shot_result == "already_shot":
                print(f"  You already shot at {format_coordinate(row, col)}! Try again.")
                continue

            # VALID SHOT — BREAK OUT OF THE INPUT LOOP.
            break

        # TELL THE PLAYER WHAT HAPPENED.
        coord_string = format_coordinate(row, col)

        if shot_result == "miss":
            print(f"  You: {coord_string} → MISS")

        elif shot_result == "hit":
            print(f"  You: {coord_string} → HIT (their {ship_name})")

        elif shot_result == "hit_and_sunk":
            # FIND THE SIZE OF THE SUNK SHIP FOR THE MESSAGE.
            sunk_size = 0
            for ship in computer_ships:
                if ship["name"] == ship_name:
                    sunk_size = ship["size"]
                    break
            print(f"  You: {coord_string} → HIT → You SANK their {ship_name}! (length {sunk_size})")

        print()

        # CHECK IF THE PLAYER HAS WON.
        if all_ships_sunk(computer_ships):
            print("============================================")
            print("  YOU WIN! All enemy ships have been sunk!")
            print("============================================")
            print_boards(player_board, computer_board)
            break

        # =============================================================
        # COMPUTER'S TURN
        # =============================================================
        comp_row, comp_col, comp_result, comp_ship_name = computer_take_shot(
            player_board, player_ships, computer_previous_shots
        )
        comp_coord = format_coordinate(comp_row, comp_col)

        if comp_result == "miss":
            print(f"  Computer: {comp_coord} → MISS")

        elif comp_result == "hit":
            print(f"  Computer: {comp_coord} → HIT (your {comp_ship_name})")

        elif comp_result == "hit_and_sunk":
            # FIND THE SIZE FOR THE MESSAGE.
            sunk_size = 0
            for ship in player_ships:
                if ship["name"] == comp_ship_name:
                    sunk_size = ship["size"]
                    break
            print(f"  Computer: {comp_coord} → HIT (your {comp_ship_name}) → {comp_ship_name} sunk (length {sunk_size})")

        print()

        # CHECK IF THE COMPUTER HAS WON.
        if all_ships_sunk(player_ships):
            print("============================================")
            print("  GAME OVER — The computer sank all your ships!")
            print("============================================")
            print_boards(player_board, computer_board)
            break

        # SHOW THE UPDATED BOARDS AFTER BOTH PLAYERS HAVE SHOT.
        print_boards(player_board, computer_board)

        turn_number = turn_number + 1


# THIS LINE MEANS: ONLY RUN main() IF WE RUN THIS FILE DIRECTLY.
# IF ANOTHER FILE IMPORTS THIS ONE, main() WON'T RUN AUTOMATICALLY.
if __name__ == "__main__":
    main()
