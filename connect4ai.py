import numpy as np
import pygame, sys

pygame.init()
SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2-5)

ROW_COUNT = 6
COLUMN_COUNT = 7

EMPTY = 0
PLAYER = 1
BOT = 2

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (203, 213, 225)

WINDOW_LENGTH = 4

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)
screen = pygame.display.set_mode(size)
myfont = pygame.font.SysFont("monospace", 18)


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, WHITE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, BLUE, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    pygame.display.update()

def gameBoard():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def printBoard(board):
    print(np.flip(board, 0))    


def drop_chip(board, row, col, chip):
    board[row][col] = chip


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0 


def get_next_open_row(board, col):
    for row in range(ROW_COUNT):
        if board[row][col] == 0:
            return row


def play():
    game_board = gameBoard()
    current_player = 1
    game_over = False
    draw_board(game_board)
    pygame.display.update()
    pygame.display.set_caption("CONNECT FOUR GAME")

    while not game_over:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = e.pos[0]

                if current_player == PLAYER:
                    pygame.draw.circle(screen, BLUE, (posx, int(SQUARESIZE/2)), RADIUS) 
 
            pygame.display.update()

            if e.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = e.pos[0]
                col = int(np.floor(posx/SQUARESIZE))
                # Player
                if is_valid_location(game_board, col):
                    row = get_next_open_row(game_board, col)
                    drop_chip(game_board, row, col, current_player)
                    
                    if player_win(game_board, current_player):
                        label = myfont.render(f"Yayy, you WON!!", 1, BLUE)
                        screen.blit(label, (40, 10))
                        game_over = True

                printBoard(game_board)
                draw_board(game_board)

                current_player = PLAYER if current_player == BOT else BOT
         # BOT
        if not game_over and current_player == BOT:
                col, minimax_score = minimax(game_board, 4, -np.inf, np.inf, True)

                if is_valid_location(game_board, col):
                    row = get_next_open_row(game_board, col)
                    drop_chip(game_board, row, col, current_player)

                    if player_win(game_board, current_player):
                        label = myfont.render(f"BOOMSHAKALAKA! You are LOSE!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True

                    current_player = PLAYER

                printBoard(game_board)     
                draw_board(game_board)

        if game_over: 
            pygame.time.wait(3000)


def player_win(board, chip):
    # check horizontal location for win
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if np.all(board[r, c:c+4] == [chip] * 4):
                return True
            
    # check vertical location for win
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT):
            if np.all(board[r:r+4, c] == chip):
                return True

    # check positively sloped diagonals
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            if all([board[r+i][c+i] == chip for i in range(4)]):
                return True
            
    # check negatively sloped diagonals
    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if all([board[r-i][c+i] == chip for i in range(4)]):
                return True
                        

def evaluate_window(window, chip):
    score = 0
    opponent_chip = PLAYER
    opponent_chip = PLAYER if chip == BOT else BOT

    if window.count(chip) == 4:
        score += 100
    elif window.count(chip) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(chip) == 2 and window.count(EMPTY) == 2:
        score += 2
    if window.count(chip) == 3 and window.count(EMPTY) == 1:
        score -= 80
    return score


def score_position(board, chip):
    score = 0

    # score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(chip)
    score += center_count * 3

    # score horizontal positions
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, chip)

    # score vertical positions
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, chip)

    # score positive diagonals
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, chip)

    # score negative diagonals
    for r in range(ROW_COUNT - 3): 
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, chip)

    return score

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def is_terminal_node(board):
    return player_win(board, PLAYER) or player_win(board, BOT) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if player_win(board, BOT):
                return (None, 9999999)
            # weight the player winning really low
            elif player_win(board, PLAYER):
                return (None, -9999999)
            else: # Game is over, no more valid moves
                return (None, 0)
            
        else: # return bot score
            return (None, score_position(board, BOT))
        
    if maximizingPlayer:
        value = -np.inf
        column = np.random.choice(valid_locations)
        
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy() 
            drop_chip(b_copy, row, col, BOT) 
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col 
            alpha = max(alpha, value)
            
            if alpha >= beta:
                break
        return column, value
    
    else: # minimizingplayer
        value = np.inf
        column = np.random.choice(valid_locations) 

        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy() 
            drop_chip(b_copy, row, col, PLAYER)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]

            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)

            if alpha >= beta:
                break
        return column, value        


play()

