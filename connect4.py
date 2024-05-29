print('\tWelcome to Connect Four!')
print('——————————————————————————————————')

columnName = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
rowsNumber = [1, 2, 3, 4, 5, 6]

gameBoard = [
    ["", "", "", "", "", "", ""],
    ["", "", "", "", "", "", ""],
    ["", "", "", "", "", "", ""],
    ["", "", "", "", "", "", ""],
    ["", "", "", "", "", "", ""],
    ["", "", "", "", "", "", ""]
]

def printBoard():
    print(f'\n \t {"   ".join(columnName)}', end="")
    for r in range(len(rowsNumber)):
        print("\n   +———+———+———+———+———+———+———+")
        print(r, " |", end="")

        for c in range(len(columnName)):
            if gameBoard[r][c] == "🔵":
                print("🔵", end=" |")
            elif gameBoard[r][c] == "🔴":
                print("🔴", end=" |")
            else:
                print("   ", end="|")
    print("\n   +———+———+———+———+———+———+———+")

def playConnect4():
    currentPlayer = '🔵'
    # start an infinite loop that will run until one of the players wins or the game is a tie.
    while True:
        printBoard()
        print(f"it's {currentPlayer}'s turn.")
        col = input("enter the column letter (A-G) to drop a chip: ").upper()
        # Checks if the input is a valid column letter
        if col not in columnName:
            print('invalid input. Column letter must be between A-G.')
            continue

        colIndex = columnName.index(col)
        # loops through each row of the game board from the bottom to the top.
        for r in range(5, -1, -1):
            # checks if the current position is empty
            if gameBoard[r][colIndex] == "":
                # assigns the current player to the empty position
                gameBoard[r][colIndex] = currentPlayer
                if checkWin(currentPlayer):
                    printBoard()
                    print(currentPlayer + " wins!")
                    playAgain()
                    return # used to exit if there's a winner
                if isBoardFull():
                    printBoard()
                    print("It's a tie!")
                    playAgain()
                    return #  used to exit function early if the board is full and there's no winner
                currentPlayer = '🔵' if currentPlayer == '🔴' else "🔴"
                break
        else: print("That column is full. choose another column.")

def checkWin(chip):
    # check horizontal
    for r in range(len(rowsNumber)):
        for c in range(len(columnName) - 3):
            if gameBoard[r][c] == chip and gameBoard[r][c+1] == chip and gameBoard[r][c+2] == chip and gameBoard[r][c+3] == chip:
                return True
    # check vertical
    for r in range(len(rowsNumber) - 3):
        for c in range(len(columnName)):
            if gameBoard[r][c] == chip and gameBoard[r+1][c] == chip and gameBoard[r+2][c] == chip and gameBoard[r+3][c] == chip:
                return True
    # check diagonal (the top-left to the bottom-right)
    for r in range(len(rowsNumber) - 3):
        for c in range(len(columnName) - 3):
            if gameBoard[r][c] == chip and gameBoard[r+1][c+1] == chip and gameBoard[r+2][c+2] == chip and gameBoard[r+3][c+3] == chip:
                return True
    # # check diagonal (the top-right to the bottom-left)
    for r in range(len(rowsNumber) - 3):
        for c in range(3, len(columnName)):
            if gameBoard[r][c] == chip and gameBoard[r+1][c-1] == chip and gameBoard[r+2][c-2] == chip and gameBoard[r+3][c-3] == chip:
                return True

def isBoardFull():
    for row in gameBoard:
        for cell in row:
            if cell == "":
                return False
    return True

def playAgain():
    while True:
        askUser = input('Do you want to play again (y/n)? ').lower()
        if askUser == 'y':
            resetGameBoard()
            printBoard()
            playConnect4()
        if askUser == 'n':
            break
        else:
            print("please input a valid character, 'y' = yes or 'n' = no.")

def resetGameBoard():
    for r in range(len(gameBoard)):
        for c in range(len(gameBoard[0])):
            gameBoard[r][c] = ""
    currentPlayer = '🔵'

playConnect4()