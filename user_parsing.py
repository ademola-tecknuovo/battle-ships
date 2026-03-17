

# defines a function 
def parse_guess(guess):

# converts the input to updatecase letters
    guess = guess.upper()

# check that user input is at least 2 characters (i.e. A4 etc)
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