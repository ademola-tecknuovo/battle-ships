import random

WATER = "~"
SHIP = "S"

SHIP_DATA = [
    {"name": "Carrier", "size": 5},
    {"name": "Battleship", "size": 4},
    {"name": "Cruiser", "size": 3},
    {"name": "Submarine", "size": 3},
    {"name": "Destroyer", "size": 2},
]


def place_ships(board):
    all_ships = []

    for ship_info in SHIP_DATA:
        name = ship_info["name"]
        size = ship_info["size"]
        placed = False

        while not placed:
            row = random.randint(0, 9)
            col = random.randint(0, 9)
            direction = random.choice(["H", "V"])

            if direction == "H" and col + size <= 10:
                if all(board[row][col + i] == WATER for i in range(size)):
                    coordinates = []
                    for i in range(size):
                        board[row][col + i] = SHIP
                        coordinates.append((row, col + i))
                    all_ships.append({"name": name, "size": size, "coordinates": coordinates, "hits": 0})
                    placed = True

            elif direction == "V" and row + size <= 10:
                if all(board[row + i][col] == WATER for i in range(size)):
                    coordinates = []
                    for i in range(size):
                        board[row + i][col] = SHIP
                        coordinates.append((row + i, col))
                    all_ships.append({"name": name, "size": size, "coordinates": coordinates, "hits": 0})
                    placed = True

    return all_ships
