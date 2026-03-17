import random
from board_display import ROW_LETTERS, WATER, SHIP, HIT, MISS


def parse_guess(guess):
    guess = guess.upper()

    if len(guess) < 2:
        return None

    if guess[0] not in ROW_LETTERS:
        return None

    try:
        col = int(guess[1:]) - 1
    except ValueError:
        return None

    row = ROW_LETTERS.index(guess[0])

    if col < 0 or col > 9:
        return None

    return row, col


def take_shot(board, ships, row, col):
    if board[row][col] == HIT or board[row][col] == MISS:
        print("Already tried there!")
        return "already_shot"

    if board[row][col] == WATER:
        board[row][col] = MISS
        print("Miss!")
        return "miss"

    if board[row][col] == SHIP:
        board[row][col] = HIT

        for ship in ships:
            if (row, col) in ship["coordinates"]:
                ship["hits"] = ship["hits"] + 1

                if ship["hits"] == ship["size"]:
                    print(f"Hit! You sank the {ship['name']}! (length {ship['size']})")
                    return "sunk"
                else:
                    print(f"Hit! ({ship['name']})")
                    return "hit"

    return "unknown"


def computer_shot(board, ships, previous_shots):
    while True:
        row = random.randint(0, 9)
        col = random.randint(0, 9)

        if (row, col) not in previous_shots:
            break

    previous_shots.append((row, col))

    coord = f"{ROW_LETTERS[row]}{col + 1}"

    if board[row][col] == SHIP:
        board[row][col] = HIT

        for ship in ships:
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
    for ship in ships:
        if ship["hits"] < ship["size"]:
            return False
    return True
